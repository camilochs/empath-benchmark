"""
EMPATH Evaluation Dimensions

19 metrics across 5 dimensions for evaluating
emotional support and mental health AI chatbots.
"""

from empath.dimensions.crisis import CRISIS_DIMENSIONS
from empath.dimensions.therapeutic import THERAPEUTIC_DIMENSIONS
from empath.dimensions.conversational import CONVERSATIONAL_DIMENSIONS
from empath.dimensions.emotional_safety import EMOTIONAL_SAFETY_DIMENSIONS
from empath.dimensions.cultural import CULTURAL_DIMENSIONS

# All 19 EMPATH dimensions consolidated
EMPATH_DIMENSIONS: dict[str, str] = {
    **CRISIS_DIMENSIONS,
    **THERAPEUTIC_DIMENSIONS,
    **CONVERSATIONAL_DIMENSIONS,
    **EMOTIONAL_SAFETY_DIMENSIONS,
    **CULTURAL_DIMENSIONS,
}

__all__ = [
    "EMPATH_DIMENSIONS",
    "CRISIS_DIMENSIONS",
    "THERAPEUTIC_DIMENSIONS",
    "CONVERSATIONAL_DIMENSIONS",
    "EMOTIONAL_SAFETY_DIMENSIONS",
    "CULTURAL_DIMENSIONS",
]
