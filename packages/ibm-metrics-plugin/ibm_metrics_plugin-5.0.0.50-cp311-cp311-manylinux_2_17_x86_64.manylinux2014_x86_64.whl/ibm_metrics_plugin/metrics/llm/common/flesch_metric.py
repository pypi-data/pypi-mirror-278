
import datasets
import evaluate


logger = evaluate.logging.get_logger(__name__)

_CITATION = "citation"
_DESCRIPTION = "description"
_KWARGS_DESCRIPTION = "description"

try:
    import textstat
except ImportError as e:
    print("Please install textstat package")
    pass

@evaluate.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Flesch(evaluate.Metric):
    def _info(self):

        return evaluate.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="homepage",
            inputs_description=_KWARGS_DESCRIPTION,
            features=
            [
                datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence")
                }
            ),
                datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence")
                }
            ),
            ],
        )

    def _download_and_prepare(self, dl_manager):

        pass
        
    def _compute(self, predictions):

        reading_ease = []
        kincaid_grade = []
        for pred in predictions:
            reading_ease.append(textstat.flesch_reading_ease(pred))
            kincaid_grade.append(textstat.flesch_kincaid_grade(pred))
        
        return {"flesch_reading_ease": reading_ease, "flesch_kincaid_grade":kincaid_grade}