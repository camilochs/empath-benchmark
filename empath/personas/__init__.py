"""
EMPATH Personas

Multilingual persona definitions for generating realistic
emotional support scenarios.
"""

from empath.personas.base import Persona, PersonaCategory
from empath.personas.es_mx import ES_MX_PERSONAS
from empath.personas.en_us import EN_US_PERSONAS

__all__ = [
    "Persona",
    "PersonaCategory",
    "ES_MX_PERSONAS",
    "EN_US_PERSONAS",
]
