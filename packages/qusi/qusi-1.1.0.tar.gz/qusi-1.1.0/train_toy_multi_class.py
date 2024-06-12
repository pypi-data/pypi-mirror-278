from functools import partial

from qusi.experimental.metric import CrossEntropyAlt, MulticlassAccuracyAlt, MulticlassAUROCAlt
from qusi.experimental.model import HadryssMultiClassEndModule
from qusi.data import LightCurveDataset
from qusi.transform import default_light_curve_observation_post_injection_transform
from qusi.internal.toy_light_curve_collection import get_toy_flat_light_curve_observation_collection, \
    get_toy_sine_wave_light_curve_observation_collection, \
    get_square_wave_light_curve_observation_collection
from qusi.model import Hadryss
from qusi.session import TrainHyperparameterConfiguration, train_session


def get_toy_multi_class_light_curve_dataset() -> LightCurveDataset:
    return LightCurveDataset.new(
        standard_light_curve_collections=[
            get_toy_flat_light_curve_observation_collection(),
            get_toy_sine_wave_light_curve_observation_collection(),
            get_square_wave_light_curve_observation_collection(),
        ],
        post_injection_transform=partial(default_light_curve_observation_post_injection_transform,
                                         length=100)
    )


def main():
    train_light_curve_dataset = get_toy_multi_class_light_curve_dataset()
    validation_light_curve_dataset = get_toy_multi_class_light_curve_dataset()
    model = Hadryss.new(input_length=100, end_module=HadryssMultiClassEndModule(number_of_classes=3))
    train_hyperparameter_configuration = TrainHyperparameterConfiguration.new(
        batch_size=100, cycles=20, train_steps_per_cycle=100, validation_steps_per_cycle=10)
    loss_function = CrossEntropyAlt()
    metric_functions = [CrossEntropyAlt(), MulticlassAccuracyAlt(number_of_classes=3),
                        MulticlassAUROCAlt(number_of_classes=3)]
    train_session(train_datasets=[train_light_curve_dataset], validation_datasets=[validation_light_curve_dataset],
                  model=model, loss_function=loss_function, metric_functions=metric_functions,
                  hyperparameter_configuration=train_hyperparameter_configuration)


if __name__ == '__main__':
    main()
