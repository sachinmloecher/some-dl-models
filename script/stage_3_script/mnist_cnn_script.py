import os
from code.base_class.artifacts import artifactConfig
from code.base_class.dataset import datasetConfig
from code.base_class.evaluate import EvaluateConfig
from code.base_class.method import methodConfig
from code.base_class.result import resultConfig
from code.base_class.setting import SettingConfig
from code.lib.comet_listeners import CometConfig, CometExperimentTracker
from code.lib.encoding.Artifacts_Saver import Artifacts_Saver
from code.lib.encoding.onnx_encoder import ONNX
from code.lib.notifier import (
    DatasetNotifier,
    EvaluateNotifier,
    MethodNotifier,
    MLEventType,
    ResultNotifier,
    SettingNotifier,
)
from code.lib.notifier.artifacts_notifier import ArtifactsNotifier

# from code.lib.util.device import get_device
from code.stage_3_code.Dataset_Loader import ValidatedPickleLoader
from code.stage_3_code.Evaluate_F1 import Evaluate_F1
from code.stage_3_code.Method_CNN_MNIST import MethodCNN
from code.stage_3_code.Result_Saver import Result_Saver
from code.stage_3_code.Setting_Train_Test_Split_MNIST import (
    Setting_Train_Test_Split,
)

import numpy as np
import torch
from torchmetrics import MetricCollection
from torchmetrics.classification import (
    MulticlassAccuracy,
    MulticlassF1Score,
    MulticlassPrecision,
    MulticlassRecall,
)

# --- Convolutional - Neural - Network script ----


def main():
    # ---- parameter section -------------------------------
    np.random.seed(2)
    torch.manual_seed(2)
    # ------------------------------------------------------
    # ---- objection initialization setction ---------------

    device: torch.device = torch.device("cpu")

    algorithm_type = "CNN"
    dataset_name = "MNIST"

    config = CometConfig(
        {
            "api_key": os.environ["COMET_API_KEY"],
            "project_name": "some-dl-models",
            "workspace": "ecs189g",
        }
    )

    experiment_tracker = CometExperimentTracker(config, dry_run=True)

    d_config = datasetConfig(
        {
            "name": dataset_name,
            "description": "Training set size: 60,000, testing set size: 10,000, number of classes: 10. Each instance is a 28x28 gray image, and will have one single class label denoted by an integer from {0, 1, …, 9}.",
            "source_folder_path": "data/stage_3_data/",
            "source_file_name": dataset_name,
            "device": device,
        }
    )

    r_config = resultConfig(
        {
            "name": f"{dataset_name}-{algorithm_type}-result",
            "description": "Training set size: 60,000, testing set size: 10,000, number of classes: 10. Each instance is a 28x28 gray image, and will have one single class label denoted by an integer from {0, 1, …, 9}.",
            "destination_folder_path": f"result/stage_3_result/{algorithm_type}_",
            "destination_file_name": "prediction_result",
        }
    )
    m_config = methodConfig(
        {
            "name": f"{algorithm_type}-method",
            "description": "This is a convolutional neural network",
            "hyperparameters": {
                "max_epoch": 49,
                "learning_rate": 1e-3,
                "conv_channels_in_dim": 1,
                "conv_channels_out_dim_0": 3,
                "conv_channels_out_dim_1": 9,
                "conv_kernel_size": 5,
                "pool_kernel_size": 2,
                "pool_stride": 1,
                "batch_size": 50,
                "output_dim_0": 20,
                "output_dim_1": 10,
                "image_size": 28,
            },
        }
    )
    s_config = SettingConfig(
        {
            "name": "Setting_Train_Test_Split_MNIST",
            "description": "This setting enables us to divide our data in sections",
            "device": device,
        }
    )

    e_config = EvaluateConfig(
        {"name": "recall", "description": "This is my recall object evaluator"}
    )

    a_config = artifactConfig(
        {
            "folder_path": "result/stage_3_artifacts/",
            "model_name": "MNIST_CNN",
            "batch_size": (50),
            "output_dim": 10,
            "input_dim": (1, 28, 28),
        }
    )

    d_notifier = DatasetNotifier()
    d_notifier.subscribe(experiment_tracker.dataset_listener, MLEventType("load"))
    data_obj = ValidatedPickleLoader(d_config, d_notifier)

    m_notifier = MethodNotifier()
    m_notifier.subscribe(experiment_tracker.method_listener, MLEventType("method"))
    batch_metrics = MetricCollection(
        [
            MulticlassAccuracy(num_classes=m_config["hyperparameters"]["output_dim_1"]).to(device),
            MulticlassF1Score(num_classes=m_config["hyperparameters"]["output_dim_1"]).to(device),
            MulticlassPrecision(num_classes=m_config["hyperparameters"]["output_dim_1"]).to(device),
            MulticlassRecall(num_classes=m_config["hyperparameters"]["output_dim_1"]).to(device),
        ]
    )

    method_obj = MethodCNN(m_config, m_notifier, batch_metrics)

    r_notifier = ResultNotifier()
    r_notifier.subscribe(experiment_tracker.result_listener, MLEventType("save"))
    result_obj = Result_Saver(r_config, r_notifier)

    s_notifier = SettingNotifier()
    s_notifier.subscribe(experiment_tracker.setting_listener, MLEventType("setting"))
    setting_obj = Setting_Train_Test_Split(s_config, s_notifier)

    e_notifier = EvaluateNotifier()
    e_notifier.subscribe(experiment_tracker.evaluation_listener, MLEventType("evaluate"))
    final_evaluation = Evaluate_F1(e_config, e_notifier)

    a_notifier = ArtifactsNotifier()
    a_notifier.subscribe(experiment_tracker.artifacts_listener, MLEventType("save_artifacts"))
    # Uses the ONNX format for encoding our model artifacts
    artifact_encoder = ONNX(a_config, method_obj)
    # Wraps the encoder object for comet integration
    artifact_obj = Artifacts_Saver(artifact_encoder, a_notifier)
    # ------------------------------------------------------

    # ---- running section ---------------------------------
    print("************ Start ************")
    setting_obj.prepare(data_obj, method_obj, result_obj, final_evaluation, artifact_obj)
    setting_obj.print_setup_summary()
    mean_score, std_score = setting_obj.load_run_save_evaluate()
    print("************ Overall Performance ************")
    print(f"{algorithm_type} Accuracy: " + str(mean_score) + " +/- " + str(std_score))
    print("************ Finish ************")
    # ------------------------------------------------------


if __name__ == "__main__":
    main()
