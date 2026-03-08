from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_relevancy,
    context_recall,
)
from datasets import Dataset
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGASEvaluator:
    def __init__(self):
        self.metrics = [
            faithfulness,
            answer_relevancy,
            context_relevancy,
            context_recall,
        ]

    def evaluate_response(
        self,
        question: str,
        answer: str,
        contexts: List[str],
        ground_truth: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {
            "question": [question],
            "answer": [answer],
            "contexts": [contexts],
        }

        if ground_truth:
            data["ground_truth"] = [ground_truth]

        dataset = Dataset.from_dict(data)

        try:
            results = evaluate(dataset, metrics=self.metrics)
            return {
                "faithfulness": results.get("faithfulness", None),
                "answer_relevancy": results.get("answer_relevancy", None),
                "context_relevancy": results.get("context_relevancy", None),
                "context_recall": results.get("context_recall", None),
            }
        except Exception as e:
            logger.error(f"RAGAS evaluation failed: {e}")
            return {"error": str(e)}

    def log_evaluation(self, evaluation: Dict[str, Any], query: str):
        logger.info(f"RAGAS Evaluation for query: {query[:50]}...")
        for metric, value in evaluation.items():
            if value is not None:
                logger.info(f"  {metric}: {value:.4f}")


evaluator = RAGASEvaluator()
