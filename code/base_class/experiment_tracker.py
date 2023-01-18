
from code.base_class.notifier import MLEventListener
from code.lib.method_notifier import MethodNotification 
from code.lib.dataset_notifier import DatasetNotification 
from code.lib.evaluate_notifier import EvaluateNotification 
from code.lib.setting_notifier import SettingNotification
from code.lib.result_notifier import ResultNotification


from typing import Protocol, runtime_checkable



@runtime_checkable
class ExperimentTracker(Protocol):
    method_listener: MLEventListener
    evaluate_listener: MLEventListener
    result_listener: MLEventListener
    setting_listener: MLEventListener
    dataset_listener: MLEventListener


    def log_model(self) -> None:
        ...  # Empty method body (explicit '...')


    def log_method(self, data: MethodNotification) -> None:
        ...  # Empty method body (explicit '...')


    def log_evaluation(self, data: EvaluateNotification) -> None:
        ...  # Empty method body (explicit '...')


    def log_dataset(self, data: DatasetNotification) -> None:
        ...  # Empty method body (explicit '...')


    def log_setting(self, data: SettingNotification) -> None:
        ...  # Empty method body (explicit '...')


    def log_results(self, data: ResultNotification) -> None:
        ...  # Empty method body (explicit '...')