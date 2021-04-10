from typing import Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Run:
    """ Representation of a single run on a specific dataset with a specific
    model and set of results, i.e. metrics with their  scores, at a specific
    time and date."""
    timestamp: datetime
    dataset_name: str
    dataset_cfg: Dict
    model_name: str
    model_cfg: Dict
    metric_scores: Dict
