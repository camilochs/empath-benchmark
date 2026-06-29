"""
EMPATH Judges

Judge implementations for evaluating emotional support AI chatbots
using the EMPATH framework metrics.
"""

from empath.judges.empath_judge import empath_judge
from empath.judges.prompts import EMPATH_JUDGE_PROMPT

__all__ = [
    "empath_judge",
    "EMPATH_JUDGE_PROMPT",
]
