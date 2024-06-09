""""Pipeline Manager class. This class is responsible for storing all generation pipelines in a PipelineOrchestrator instance."""

from typing import Dict, Optional
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline


class PipelineManager(Dict[str, Optional[MultiEstimatorPipeline]]):
    """Pipeline Manager class. This class is responsible for storing all generation pipelines in a PipelineOrchestrator instance."""

    def __init__(self):
        super().__init__(
            {
                "base": None,
                "stacked": None,
                "evolved": None,
            }
        )

    def __getitem__(self, key: str) -> Optional[MultiEstimatorPipeline]:
        if key not in {"base", "stacked", "evolved"}:
            raise KeyError(
                f"The pipeline '{key}' does not exist. Available pipelines are 'base', 'stacked', and 'evolved'."
            )
        if key not in self:
            raise KeyError(
                f"Key '{key}' does not exist, meaning the pipeline '{key}' was not robust enough after using PipelineOrchestrator.fortify()."
            )

        value = self.get(key, None)

        if value is None:
            raise ValueError(f"Value of '{key}' is None, meaning the pipeline '{key}' has not been built yet.")

        return value

    def __repr__(self):
        return str(dict(self))
