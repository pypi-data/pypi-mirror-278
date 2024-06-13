import os
import sys
import unittest

from useckit.paradigms.anomaly_detection.anomaly_paradigm import AnomalyParadigm
from useckit.paradigms.anomaly_detection.evaluation_methods.identification import \
    IdentificationOnly as AnomalyIdentification
from useckit.paradigms.anomaly_detection.evaluation_methods.identification_with_reject import \
    IdentificationWithReject as AnomalyIdentificationWithReject
from useckit.paradigms.anomaly_detection.evaluation_methods.verification import \
    Verification as AnomalyVerification
from useckit.paradigms.anomaly_detection.prediction_models.scikit_anomaly_prediction_model import \
    ScikitAnomalyPredictionModel
from useckit.paradigms.binary_verification.binary_verification_paradigm import BinaryVerificationParadigm
from useckit.paradigms.binary_verification.evaluation_methods.binary_verification_evaluation_method_scoring import \
    BinaryScoringVerification
from useckit.paradigms.binary_verification.prediction_models.verification_scikit_prediction_model import \
    VerificationSkLearnPredictionModel
from useckit.paradigms.distance_learning.distance_paradigm import DistanceMetricParadigm
from useckit.paradigms.distance_learning.evaluation_methods.identification import \
    IdentificationOnly as DistanceIdentification
from useckit.paradigms.distance_learning.evaluation_methods.identification_with_reject import \
    IdentificationWithReject as DistanceIdentificationWithReject
from useckit.paradigms.distance_learning.evaluation_methods.verification import \
    Verification as DistanceVerification
from useckit.paradigms.distance_learning.prediction_models.scikit_distance_model import ScikitDistancePredictionModel
from useckit.paradigms.time_series_classification.evaluation_methods.identification import \
    IdentificationOnly as TSCIdentification
from useckit.paradigms.time_series_classification.prediction_models.classification_scikit_prediction_model import \
    ClassificationScikitPredictionModel
from useckit.paradigms.time_series_classification.tsc_paradigm import TSCParadigm
from useckit.tests.test_utils import make_dataset, make_windowsliced_dataset

# resolves issues with gitlab runner
sys.setrecursionlimit(10000)
# disable gpu training for unittests
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class TestUseckit(unittest.TestCase):

    def test_anomaly_prediction(self):
        data = make_dataset(shape=(100, 100), noisiness=0)
        encoder = AnomalyParadigm(verbose=True, prediction_model=ScikitAnomalyPredictionModel(),
                                  evaluation_methods=[AnomalyVerification(), AnomalyIdentification(),
                                                      AnomalyIdentificationWithReject()])
        encoder.evaluate(data)

    def test_time_series_classification(self):
        data = make_dataset(shape=(100, 100), noisiness=0)
        tsc = TSCParadigm(
            prediction_model=ClassificationScikitPredictionModel(),
            verbose=True, evaluation_methods=[TSCIdentification()])
        tsc.evaluate(data)

    def test_distance_metric(self):
        data = make_dataset(shape=(100, 100), noisiness=0)
        siamese = DistanceMetricParadigm(verbose=True, prediction_model=ScikitDistancePredictionModel(),
                                         evaluation_methods=[
                                             DistanceVerification(tradeoff_computation_speed_for_memory=True),
                                             DistanceIdentification(tradeoff_computation_speed_for_memory=True),
                                             DistanceIdentificationWithReject(
                                                 tradeoff_computation_speed_for_memory=True)])
        siamese.evaluate(data)
        siamese = DistanceMetricParadigm(verbose=True, prediction_model=ScikitDistancePredictionModel(),
                                         evaluation_methods=[
                                             DistanceVerification(tradeoff_computation_speed_for_memory=False),
                                             DistanceIdentification(tradeoff_computation_speed_for_memory=False),
                                             DistanceIdentificationWithReject(
                                                 tradeoff_computation_speed_for_memory=False)])
        siamese.evaluate(data)

    def test_anomaly_prediction_windowsliced(self):
        data = make_windowsliced_dataset(5, 10, shape=(20, 100), noisiness=0)
        encoder = AnomalyParadigm(verbose=True, prediction_model=ScikitAnomalyPredictionModel(),
                                  evaluation_methods=[AnomalyVerification(), AnomalyIdentification(),
                                                      AnomalyIdentificationWithReject()])
        encoder.evaluate(data)

    def test_time_series_classification_windowsliced(self):
        data = make_windowsliced_dataset(5, 10, shape=(20, 100), noisiness=0)
        tsc = TSCParadigm(
            prediction_model=ClassificationScikitPredictionModel(),
            verbose=True, evaluation_methods=[TSCIdentification()])
        tsc.evaluate(data)

    def test_distance_metric_windowsliced(self):
        data = make_windowsliced_dataset(5, 10, shape=(20, 100), noisiness=0)
        siamese = DistanceMetricParadigm(verbose=True, prediction_model=ScikitDistancePredictionModel(),
                                         evaluation_methods=[DistanceVerification(), DistanceIdentification(),
                                                             DistanceIdentificationWithReject()])
        siamese.evaluate(data)

    def test_binary_verification_ovr(self):
        # ovr = one vs rest case
        data = make_dataset(shape=(100, 100), noisiness=0)
        verif = BinaryVerificationParadigm(verbose=True,
                                           prediction_model=VerificationSkLearnPredictionModel(),
                                           evaluation_methods=[BinaryScoringVerification()],
                                           multiclass_classification_strategy='ovr')
        verif.evaluate(data)

    def test_binary_verification_ovo(self):
        # ovo = one vs one case
        data = make_dataset(shape=(100, 100), noisiness=0)
        verif = BinaryVerificationParadigm(verbose=True,
                                           prediction_model=VerificationSkLearnPredictionModel(),
                                           evaluation_methods=[BinaryScoringVerification()],
                                           multiclass_classification_strategy='ovo')
        verif.evaluate(data)

    def test_pupilbiomvr_dataset_majority_voting(self):
        """This test raised the following stack exception:

        ---------------------------------------------------------------------------
        IndexError                                Traceback (most recent call last)
        Cell In[39], line 29
             13 others = False
             14 tsc = TSCEvaluator(useckit_dataset,
             15                    epochs=500,
             16                    verbose=True,
           (...)
             27                    enable_mcdcnn=others,
             28                    experiment_description_name=output_dir)
        ---> 29 tsc.evaluate()

        File /usr/local/lib/python3.11/dist-packages/useckit/Evaluators.py:119, in TSCEvaluator.evaluate(self)
            106     TSCParadigm(
            107         prediction_model=ClassificationKerasPredictionModel(verbose=self.verbose, nb_epochs=self.epochs,
            108                                                             model_description=dl4tsc_mlp),
            109         verbose=self.verbose,
            110         experiment_description_name=self.experiment_description_name,
            111         seed=self.seed).evaluate(self.dataset)
            113 if self.enable_fcn:
            114     TSCParadigm(
            115         prediction_model=ClassificationKerasPredictionModel(verbose=self.verbose, nb_epochs=self.epochs,
            116                                                             model_description=dl4tsc_fcn),
            117         verbose=self.verbose,
            118         experiment_description_name=self.experiment_description_name,
        --> 119         seed=self.seed).evaluate(self.dataset)
            121 if self.enable_resnet:
            122     TSCParadigm(
            123         prediction_model=ClassificationKerasPredictionModel(verbose=self.verbose, nb_epochs=self.epochs,
            124                                                             model_description=dl4tsc_resnet),
            125         verbose=self.verbose,
            126         experiment_description_name=self.experiment_description_name,
            127         seed=self.seed).evaluate(self.dataset)

        File /usr/local/lib/python3.11/dist-packages/useckit/paradigms/_paradigm_base.py:195, in ParadigmBase.evaluate(self, dataset)
            190     print(
            191         f'useckit info: finished fitting model of type {type(self.prediction_model).__name__} ' +
            192         f'after {round((time.time() - start_time), 2)} seconds.')
            193     print(f'useckit info: running evaluation methods')
        --> 195 self.run_evaluation_methods(dataset)
            197 with open(os.path.join(self.output_dir, 'timing.txt'), 'a') as f:
            198     now = time.time()

        File /usr/local/lib/python3.11/dist-packages/useckit/paradigms/_paradigm_base.py:219, in ParadigmBase.run_evaluation_methods(self, dataset)
            217 def run_evaluation_methods(self, dataset: Dataset):
            218     for eval_method in self.evalution_methods:
        --> 219         eval_method.evaluate(dataset, self.prediction_model, **self.base_kwargs)

        File /usr/local/lib/python3.11/dist-packages/useckit/paradigms/time_series_classification/evaluation_methods/identification.py:30, in IdentificationOnly.evaluate(self, dataset, prediction_model, **kwargs)
             29 def evaluate(self, dataset: Dataset, prediction_model: TSCBasePredictionModel, **kwargs):
        ---> 30     perform_identification_evaluation(TSCIdentificationModel(dataset, prediction_model), dataset,
             31                                       self.output_dir)

        File /usr/local/lib/python3.11/dist-packages/useckit/evaluation/identification.py:32, in perform_identification_evaluation(identification_model, dataset, output_folder)
             29 _output_results(model_predictions, true_labels_reverse_transformed, output_folder, dataset, filename_prefix)
             31 if isinstance(dataset, WindowslicedDataset):
        ---> 32     _perform_identification_evaluation_windowsliced(model_predictions, true_labels_reverse_transformed,
             33                                                     dataset, output_folder)

        File /usr/local/lib/python3.11/dist-packages/useckit/evaluation/identification.py:40, in _perform_identification_evaluation_windowsliced(model_prediction, true_labels_reverse_transformed, dataset, output_folder)
             36 def _perform_identification_evaluation_windowsliced(model_prediction: np.ndarray,
             37                                                     true_labels_reverse_transformed: np.ndarray,
             38                                                     dataset: WindowslicedDataset, output_folder: str):
             39     sample_predictions, sample_labels = \
        ---> 40         dataset.apply_voting_for_testset_matching_slices(model_prediction, true_labels_reverse_transformed)
             41     _output_results(sample_predictions, sample_labels, output_folder, dataset, '')

        File /usr/local/lib/python3.11/dist-packages/useckit/util/dataset_windowsliced.py:161, in WindowslicedDataset.apply_voting_for_testset_matching_slices(self, predictions_slices, ground_truth_slices)
            158 predictions = np.zeros((len(self.testset_matching_sliceorigin_mask),), dtype=predictions_slices.dtype)
            160 for sample_id, sample_mask in enumerate(self.testset_matching_sliceorigin_mask):
        --> 161     predictions[sample_id] = self.voting_function(predictions_slices[sample_mask])
            162     ground_truth[sample_id] = ground_truth_slices[sample_mask][0]  # don't need to vote
            163     # as the labels of all slices of one sample should be equal

        File /usr/local/lib/python3.11/dist-packages/useckit/util/dataset_windowsliced.py:13, in _majority_vote_over(array)
             11 def _majority_vote_over(array: np.ndarray):
             12     c = Counter(array)
        ---> 13     return c.most_common(1)[0][0]

        IndexError: list index out of range
        """

        import numpy as np
        from useckit.util.dataset_windowsliced import WindowslicedDataset
        from useckit.Evaluators import TSCEvaluator

        try:
            # local paths on e.g., pycharm
            x_train_np = np.load("resources/x_train_np_pupilbiomvr.npy")
            x_test_np = np.load("resources/x_test_np_pupilbiomvr.npy")
        except FileNotFoundError:
            # paths for gitlab ci/cd
            x_train_np = np.load("useckit/tests/resources/x_train_np_pupilbiomvr.npy")
            x_test_np = np.load("useckit/tests/resources/x_test_np_pupilbiomvr.npy")

        print("x_train_np.shape", x_train_np.shape)
        print("x_test_np.shape", x_test_np.shape)

        y_train = np.array([1, 10, 13, 14, 15, 18, 2, 22, 23, 24, 25, 26, 27, 3, 4, 5, 6, 7, 8, 9])
        y_test = np.array([1, 10, 13, 14, 15, 18, 2, 22, 23, 24, 25, 26, 27, 3, 4, 5, 6, 7, 8, 9])

        print("y_train.shape", y_train.shape)
        print("y_test.shape", y_test.shape)

        useckit_dataset = WindowslicedDataset(window_slicing_stride=45,
                                              window_slicing_size=90,
                                              trainset_data=x_train_np,
                                              trainset_labels=y_train,
                                              testset_enrollment_data=x_train_np,
                                              testset_enrollment_labels=y_train,
                                              testset_matching_data=x_test_np,
                                              testset_matching_labels=y_test)

        others = False
        tsc = TSCEvaluator(useckit_dataset,
                           epochs=5,
                           verbose=True,
                           enable_mlp=False,
                           enable_resnet=True,
                           enable_fcn=True,
                           enable_encoder=others,
                           enable_cnn_valid=True,
                           enable_cnn_same=others,
                           enable_mcnn=others,
                           enable_tlenet=others,
                           enable_twiesn=others,
                           enable_inception=True,
                           enable_mcdcnn=others)
        tsc.evaluate()

    def test_binary_verification_windowsliced_ovr(self):
        return  # test currently disabled
        # ovo = one vs one case
        data = make_windowsliced_dataset(5, 10, shape=(20, 100), noisiness=0)
        verif = BinaryVerificationParadigm(verbose=True,
                                           prediction_model=VerificationSkLearnPredictionModel(),
                                           evaluation_methods=[BinaryScoringVerification()],
                                           multiclass_classification_strategy='ovr')
        verif.evaluate(data)

    def test_binary_verification_windowsliced_ovo(self):
        return  # test currently disabled
        # ovo = one vs one case
        data = make_windowsliced_dataset(5, 10, shape=(20, 100), noisiness=0)
        verif = BinaryVerificationParadigm(verbose=True,
                                           prediction_model=VerificationSkLearnPredictionModel(),
                                           evaluation_methods=[BinaryScoringVerification()],
                                           multiclass_classification_strategy='ovo')
        verif.evaluate(data)


if __name__ == '__main__':
    unittest.main()
