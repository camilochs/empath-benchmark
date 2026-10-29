"""
Base Persona Definitions

Core classes and types for EMPATH personas used in scenario generation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PersonaCategory(Enum):
    """Categories of emotional support scenarios."""
    CRISIS = "crisis"
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    RELATIONSHIP = "relationship"
    GRIEF = "grief"
    WORK_STRESS = "work_stress"
    SELF_ESTEEM = "self_esteem"
    FAMILY = "family"
    LIFE_TRANSITION = "life_transition"
    GENERAL_SUPPORT = "general_support"


@dataclass
class Persona:
    """
    A persona for emotional support scenario generation.

    Personas represent realistic users seeking emotional support,
    with culturally-appropriate backgrounds and concerns.
    """

    # Identity
    name: str
    age: int
    gender: str
    locale: str  # es-MX or en-US

    # Context
    category: PersonaCategory
    background: str
    current_situation: str
    emotional_state: str

    # Conversation elements
    opening_message: str
    follow_up_topics: list[str] = field(default_factory=list)

    # Risk indicators
    crisis_level: int = 0  # 0-3: none, low, moderate, high
    risk_factors: list[str] = field(default_factory=list)

    # Cultural elements
    cultural_context: str = ""
    language_style: str = ""  # formal, informal, mixed

    # Writing style (for realistic message generation)
    writing_style_description: str = ""
    sample_phrases: list[str] = field(default_factory=list)
    socioeconomic_context: str = ""

    # Metadata
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert persona to dictionary format."""
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "locale": self.locale,
            "category": self.category.value,
            "background": self.background,
            "current_situation": self.current_situation,
            "emotional_state": self.emotional_state,
            "opening_message": self.opening_message,
            "follow_up_topics": self.follow_up_topics,
            "crisis_level": self.crisis_level,
            "risk_factors": self.risk_factors,
            "cultural_context": self.cultural_context,
            "language_style": self.language_style,
            "writing_style_description": self.writing_style_description,
            "sample_phrases": self.sample_phrases,
            "socioeconomic_context": self.socioeconomic_context,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Persona":
        """Create persona from dictionary."""
        data = data.copy()
        if isinstance(data.get("category"), str):
            data["category"] = PersonaCategory(data["category"])
        return cls(**data)
