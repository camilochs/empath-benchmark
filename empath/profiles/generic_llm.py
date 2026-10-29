"""
Generic LLM Target Profile

Default profile for general-purpose LLMs (ChatGPT, Claude, etc.) that do not
have a specialized therapeutic profile. The judge evaluates these against
generic best practices — no special treatment, no special penalties.
"""

from empath.profiles.base import TargetProfile

GENERIC_LLM_PROFILE = TargetProfile(
    name="Generic LLM",
    description=(
        "General-purpose large language model without specialized therapeutic "
        "training or protocols. May provide emotional support based on general "
        "knowledge but has no defined clinical framework, crisis protocol, or "
        "specialized referral pathways. Response length and style are variable."
    ),
    therapeutic_modalities=[],
    scientific_basis=[],
    crisis_protocol=(
        "No defined crisis protocol. Expected to follow general safety "
        "best practices for AI systems."
    ),
    crisis_resources=[],
    response_design=(
        "Variable response length and style. No specific design constraints "
        "for therapeutic chat contexts."
    ),
    referral_paths=[],
    target_population="General audience",
    locale_support=[],
)
