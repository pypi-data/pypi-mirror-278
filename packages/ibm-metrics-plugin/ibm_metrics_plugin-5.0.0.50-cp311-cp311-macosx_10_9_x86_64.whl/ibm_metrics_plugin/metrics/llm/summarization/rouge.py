
#----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2023  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by 
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import datasets
import evaluate


_CITATION = "citation"
_DESCRIPTION = "description"
_KWARGS_DESCRIPTION = "description"

try:
    from torchmetrics.text.rouge import ROUGEScore
    import torch
except ImportError as e:
    msg = "Please install torchmetrics package to compute rouge score"
    print(msg)
    
@evaluate.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class RougeTorchImplementation(evaluate.Metric):
    def _info(self):

        return evaluate.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="homepage",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                datasets.Features(
                    {
                        "predictions": datasets.Value("string", id="sequence"),
                        "references": datasets.Value("string", id="sequence"),
                    }
                )
            )
        )

    def _download_and_prepare(self, dl_manager):
        pass
        
    def _compute(self, predictions, references, use_aggregator = True, use_stemmer = False ):
        if use_aggregator:
            torchrouge = ROUGEScore(use_stemmer=use_stemmer, accumulate='avg')
        else:
            torchrouge = ROUGEScore(use_stemmer=use_stemmer)
                
        torchrouge_scores = torchrouge(predictions, references )
        return self.__get_torchmetrics_rouge_scores(torchrouge_scores)
        
    def __get_torchmetrics_rouge_scores(self,scores):
        results = {}
        for key in scores.keys():
            if key == 'rouge1_fmeasure':
                results['rouge1'] = round(self.__get_value(scores[key]),4)
            elif key == 'rouge2_fmeasure':
                results['rouge2'] = round(self.__get_value(scores[key]),4)
            elif key == 'rougeL_fmeasure': 
                results['rougeL'] = round(self.__get_value(scores[key]),4)
            elif key == 'rougeLsum_fmeasure': 
                results['rougeLsum'] = round(self.__get_value(scores[key]),4)
        return results   
    
    def __get_value(self, tensor):
        if isinstance(tensor, torch.Tensor):
            return tensor.item()
        return None
  
        
        