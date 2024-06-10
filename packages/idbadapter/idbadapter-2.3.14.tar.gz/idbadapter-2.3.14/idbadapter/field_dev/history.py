from abc import ABC, abstractmethod

from pandas import DataFrame


class FieldDevHistoryAdapter(ABC):
    @abstractmethod
    def get_journal_mapped(self) -> dict:
        ...

    @abstractmethod
    def get_links_history_messoyakha_with_new_granular_v2(self) -> DataFrame:
        ...

    @abstractmethod
    def get_precalculated_brave_coefficients(self) -> DataFrame:
        ...

    @abstractmethod
    def get_work_defect_res_data_no_nan_new2(self) -> DataFrame:
        ...

    @abstractmethod
    def get_work_res_data_no_nan_new2(self) -> DataFrame:
        ...
