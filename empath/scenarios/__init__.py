"""
EMPATH Scenarios

Scenario definitions and generators for emotional support evaluations.
Includes crisis scenarios, therapeutic scenarios, and cultural scenarios.
"""

from empath.scenarios.base import Scenario, ScenarioType
from empath.scenarios.crisis_scenarios import CRISIS_SCENARIOS
from empath.scenarios.therapeutic_scenarios import THERAPEUTIC_SCENARIOS
from empath.scenarios.cultural_scenarios import CULTURAL_SCENARIOS
from empath.scenarios.generator import ScenarioGenerator

# All scenarios combined
ALL_SCENARIOS: list["Scenario"] = (
    CRISIS_SCENARIOS +
    THERAPEUTIC_SCENARIOS +
    CULTURAL_SCENARIOS
)

__all__ = [
    "Scenario",
    "ScenarioType",
    "CRISIS_SCENARIOS",
    "THERAPEUTIC_SCENARIOS",
    "CULTURAL_SCENARIOS",
    "ALL_SCENARIOS",
    "ScenarioGenerator",
]
