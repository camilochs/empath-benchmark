"""
Target Profile Base

Universal dataclass for declaring the capabilities and design of any
AI system being evaluated. This allows the judge to evaluate each target
within its declared design parameters — fairly and without bias.
"""

from dataclasses import dataclass, field


@dataclass
class TargetProfile:
    """
    Profile declared by the AI system being evaluated.

    Any target can provide one so the judge evaluates it in context.
    A target WITHOUT a profile is assumed to be a general-purpose LLM
    and is evaluated against generic best practices.
    """

    name: str
    description: str
    therapeutic_modalities: list[str] = field(default_factory=list)
    scientific_basis: list[str] = field(default_factory=list)
    crisis_protocol: str = ""
    crisis_resources: list[str] = field(default_factory=list)
    response_design: str = ""
    referral_paths: list[str] = field(default_factory=list)
    target_population: str = ""
    locale_support: list[str] = field(default_factory=list)

    def format_for_judge(self) -> str:
        """Format the profile as text to inject into the judge prompt."""
        sections = [
            f"**Name**: {self.name}",
            f"**Description**: {self.description}",
        ]

        if self.therapeutic_modalities:
            modalities = ", ".join(self.therapeutic_modalities)
            sections.append(f"**Therapeutic Modalities**: {modalities}")

        if self.scientific_basis:
            basis = ", ".join(self.scientific_basis)
            sections.append(f"**Scientific Basis**: {basis}")

        if self.crisis_protocol:
            sections.append(f"**Crisis Protocol**: {self.crisis_protocol}")

        if self.crisis_resources:
            resources = "\n".join(f"  - {r}" for r in self.crisis_resources)
            sections.append(f"**Crisis Resources**:\n{resources}")

        if self.response_design:
            sections.append(f"**Response Design**: {self.response_design}")

        if self.referral_paths:
            paths = "\n".join(f"  - {r}" for r in self.referral_paths)
            sections.append(f"**Referral Paths**:\n{paths}")

        if self.target_population:
            sections.append(f"**Target Population**: {self.target_population}")

        if self.locale_support:
            locales = ", ".join(self.locale_support)
            sections.append(f"**Locale Support**: {locales}")

        return "\n".join(sections)
