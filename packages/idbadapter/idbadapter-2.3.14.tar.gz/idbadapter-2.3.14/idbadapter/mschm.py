from typing import Type, Union
import json
from contextlib import contextmanager
from sqlalchemy.exc import ResourceClosedError

import pandas as pd

from sqlalchemy.orm import scoped_session

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, delete, update, text as sql_text

from sqlalchemy import create_engine
from .models import BasicResource, BasicWork, Precalculation, MSCHMModel
from .models import S7Model, MSModel


from functools import lru_cache

class MschmAdapter:
    def __init__(self, url, echo=False):
        self.engine = create_engine(url, echo=echo)
        self.session_factory = sessionmaker(bind=self.engine)

        self.mschm_models = {}
        self.mro_models = {}

        self.basic_objects_for_insert = {
            BasicWork: [],
            BasicResource: [],
        }

        self.works: list[BasicWork] = []
        self.resources: list[BasicResource] = []
        self.precalculations: list[Precalculation] = []


        self.basic_collections = {
            BasicWork: self.__get_basic_objects(BasicWork),
            BasicResource: self.__get_basic_objects(BasicResource),
        }

    def save_precalculation_to_db(self, data: dict) -> None:
        for work_name, work_data in data.items():
            work = self.__handle_basic_name(BasicWork, work_name)
            self.delete_precalculation(work)
            self.__parse_work_data(work_data_dict=work_data, work=work)

        self.__save(self.basic_objects_for_insert.values())
        self.__save([self.precalculations])
        self.__update()

    def delete_precalculation(self, work):
        self.__execute_query(delete(Precalculation).where(Precalculation.id_basic_work == work.id), True)

    def save_model_to_db(self, model, measurement_type=None):
        models_to_write = []
        for work_name, work_data in model.items():
            current = self.get_model(work_name, measurement_type)
            if current is not None:
                self.__execute_query(delete(MSModel).where(MSModel.name == work_name,
                                                           MSModel.measurement_type == measurement_type), True)
            data = json.dumps(work_data)
            models_to_write.append(MSModel(name=work_name,
                                           data=data,
                                           measurement_type=measurement_type))
        self.__save([models_to_write])

    def get_precalculation(self, name_of_works: list[str]) -> dict:
        result = {}
        self.__update()
        basic_resources_ids_dict = {o.id: o for o in self.basic_collections[BasicResource].values()}
        basic_works_ids_dict = {o.id: o for o in self.basic_collections[BasicWork].values() if o.name in name_of_works}

        precalculation_data = self.__execute_query(
            select(Precalculation
                   ).where(Precalculation.id_basic_work.in_(basic_works_ids_dict))
                   )

        if len(precalculation_data) == 0:
            return result

        df = pd.DataFrame([o.__dict__ for o in precalculation_data]).drop("_sa_instance_state", axis=1)
        df["basic_work_name"] = df["id_basic_work"].apply(lambda x: basic_works_ids_dict[x].name)
        df["basic_resource_name"] = df["id_basic_resource"].apply(lambda x: basic_resources_ids_dict[x].name)

        for row in df.to_dict(orient="records"):
            work_name = row["basic_work_name"]
            prob = row["work_value_probability"]
            work_value = row["work_value"]
            res_name = row["basic_resource_name"]
            res_value = row["res_value"]
            res_prob = f'{row["probability"]}%'

            if work_name not in result:
                result[work_name] = {}
            if work_value not in result[work_name]:
                result[work_name][work_value] = {}
            if res_prob not in result[work_name][work_value]:
                result[work_name][work_value][res_prob] = {}
            result[work_name][work_value][res_prob][res_name] = res_value
            result[work_name][work_value]["Prob"] = prob

        return result

    def get_model(self, name, measurement_type=None):
        key = (name, measurement_type)
        if key in self.mschm_models:
            return self.mschm_models[key]
        elif len(self.mschm_models) == 0:
            result: list[MSModel] = self.__execute_query(
                select(MSModel))
            self.mschm_models = {(k.name, k.measurement_type): json.loads(k.data) for k in result}
            try:
                return self.mschm_models[key]
            except KeyError:
                return None
        else:
            print(f"model with name {name} not found!")
            return

    def save_s7_model(self, model, measurement_type=None):
        models_to_write = []
        for name, data in model.items():
            # check if model in database
            current = self.get_s7_model(name)
            if current is not None:
                self.__execute_query(delete(S7Model).where(S7Model.name==name), True)
            data = json.dumps(data)
            models_to_write.append(S7Model(name=name,
                                           data=data))
        self.__save([models_to_write])


    def get_s7_model(self, name):
        if name in self.mro_models:
            return self.mro_models[name]
        elif len(self.mro_models) == 0:
            result: list[S7Model] = self.__execute_query(
                select(S7Model))
            self.mro_models = {k.name: json.loads(k.data) for k in result}
            return self.mro_models[name]

    def __update(self):
        self.precalculations = []
        self.resources = []
        self.basic_collections = {
            BasicWork: self.__get_basic_objects(BasicWork),
            BasicResource: self.__get_basic_objects(BasicResource),
        }

    def __parse_work_data(self, work_data_dict: dict[str, dict], work: BasicWork):
        for work_value, prob_data in work_data_dict.items():
            work_value_prob = prob_data["Prob"]
            for probability, res_data in prob_data.items():
                if isinstance(res_data, dict):
                    for res_name, res_value in res_data.items():
                        resource = self.__handle_basic_name(BasicResource, res_name)

                        self.precalculations.append(
                            Precalculation(
                                id=self.__get_last_id(self.precalculations, Precalculation)+1,
                                id_basic_work=work.id,
                                id_basic_resource=resource.id,
                                work_value=float(work_value),
                                res_value=float(res_value),
                                probability=int(probability[:-1]),
                                work_value_probability=work_value_prob,
                            )
                        )

    def __handle_basic_name(self, basic_cls: Union[Type[BasicWork], Type[BasicResource]],
                            name: str) -> Union[BasicWork, Type]:
        collection = self.basic_collections[basic_cls]
        if name in collection:
            return collection[name]
        obj = basic_cls(
                        id=self.__get_last_id(list(collection.values()), basic_cls) + 1,
                        name=name
                )
        collection[name] = obj
        self.basic_objects_for_insert[basic_cls].append(obj)
        self.basic_collections[basic_cls][name] = obj
        return obj

    def __get_last_id_from_db(self, cls: Type[MSCHMModel]):
        query = sql_text(f"select max(id) from {cls.__tablename__}")
        last_id = self.__execute_query(query)
        last_id = last_id[0]
        if last_id is None:
            return 0
        return last_id

    def __get_basic_objects(self, cls):
        query = select(cls)
        result = self.__execute_query(query)
        return {o.name: o for o in result}

    def __save(self, collections: list[list]):
        for collection in collections:
            self.__save_to_database(collection)

    def __save_to_database(self, collection):
        with self.__get_session() as context:
            context.add_all(collection)
            context.commit()

    def __get_last_id(self, collection: list, cls: Type[MSCHMModel]):
        if len(collection):
            return max([o.id for o in collection])
        else:
            last_id = self.__get_last_id_from_db(cls)
            return 0 if last_id is None else last_id

    def __execute_query(self, query, commit=False) -> list:
        with self.__get_session() as context:
            result = context.execute(query)
            try:
                result = result.scalars().all()
            except ResourceClosedError:
                pass
            if commit:
                context.commit()

        return result

    @contextmanager
    def __get_session(self):
        session = scoped_session(self.session_factory)
        try:
            yield session
        finally:
            session.close()
