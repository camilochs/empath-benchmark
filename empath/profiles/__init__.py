"""
EMPATH Target Profiles

Universal system for declaring the capabilities and design of AI systems
being evaluated. Allows the judge to evaluate each target fairly within
its declared design parameters.
"""

from empath.profiles.base import TargetProfile
from empath.profiles.generic_llm import GENERIC_LLM_PROFILE

# Registry of known profiles by provider name
_PROFILE_REGISTRY: dict[str, TargetProfile] = {}


def load_profile(provider: str) -> TargetProfile:
    """
    Load a target profile by provider name.

    Unknown providers get the generic LLM profile.

    Args:
        provider: The provider name (e.g., "openai", "anthropic").

    Returns:
        The corresponding TargetProfile.
    """
    return _PROFILE_REGISTRY.get(provider, GENERIC_LLM_PROFILE)


__all__ = [
    "TargetProfile",
    "GENERIC_LLM_PROFILE",
    "load_profile",
]
