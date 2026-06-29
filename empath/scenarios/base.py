"""
Base Scenario Definitions

Core classes for EMPATH evaluation scenarios.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ScenarioType(Enum):
    """Types of evaluation scenarios."""
    CRISIS = "crisis"
    THERAPEUTIC = "therapeutic"
    CULTURAL = "cultural"
    CONVERSATIONAL = "conversational"
    BOUNDARY = "boundary"
    SAFETY = "safety"


@dataclass
class ConversationTurn:
    """A single turn in a scenario conversation."""
    role: str  # "user" or "assistant"
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Scenario:
    """
    An evaluation scenario for EMPATH.

    Scenarios define test cases for evaluating emotional support AI,
    including the user's opening message, expected conversation flow,
    and evaluation criteria.
    """

    # Identity
    id: str
    locale: str  # es-MX or en-US
    scenario_type: ScenarioType

    # Content
    title: str
    description: str
    user_opening: str

    # Optional multi-turn conversation
    conversation: list[ConversationTurn] = field(default_factory=list)

    # Evaluation criteria
    expected_metrics: dict[str, int] = field(default_factory=dict)
    key_behaviors: list[str] = field(default_factory=list)
    red_flags: list[str] = field(default_factory=list)

    # Context
    persona_background: str = ""
    cultural_notes: str = ""

    # Metadata
    tags: list[str] = field(default_factory=list)
    difficulty: str = "medium"  # easy, medium, hard
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert scenario to dictionary format."""
        return {
            "id": self.id,
            "locale": self.locale,
            "scenario_type": self.scenario_type.value,
            "title": self.title,
            "description": self.description,
            "user_opening": self.user_opening,
            "conversation": [
                {"role": t.role, "content": t.content, "metadata": t.metadata}
                for t in self.conversation
            ],
            "expected_metrics": self.expected_metrics,
            "key_behaviors": self.key_behaviors,
            "red_flags": self.red_flags,
            "persona_background": self.persona_background,
            "cultural_notes": self.cultural_notes,
            "tags": self.tags,
            "difficulty": self.difficulty,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Scenario":
        """Create scenario from dictionary."""
        data = data.copy()
        if isinstance(data.get("scenario_type"), str):
            data["scenario_type"] = ScenarioType(data["scenario_type"])
        if "conversation" in data:
            data["conversation"] = [
                ConversationTurn(**turn) for turn in data["conversation"]
            ]
        return cls(**data)

    def to_sample_input(self) -> str:
        """Convert scenario to input format for evaluation."""
        return self.user_opening
