"""
EMPATH Task

Main Inspect AI task for evaluating emotional support AI chatbots
using the EMPATH framework.
"""
from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample, MemoryDataset
from inspect_ai.scorer import Scorer
from inspect_ai.solver import generate

from empath.dimensions import EMPATH_DIMENSIONS
from empath.judges.empath_judge import empath_judge
from empath.scenarios import ALL_SCENARIOS, CRISIS_SCENARIOS
from empath.scenarios.base import Scenario
from empath.personas import ES_MX_PERSONAS, EN_US_PERSONAS
from empath.scenarios.generator import ScenarioGenerator


def scenarios_to_samples(scenarios: list[Scenario]) -> list[Sample]:
    """Convert EMPATH scenarios to Inspect AI samples."""
    samples = []
    for scenario in scenarios:
        samples.append(
            Sample(
                id=scenario.id,
                input=scenario.user_opening,
                metadata={
                    "locale": scenario.locale,
                    "scenario_type": scenario.scenario_type.value,
                    "title": scenario.title,
                    "description": scenario.description,
                    "expected_metrics": scenario.expected_metrics,
                    "key_behaviors": scenario.key_behaviors,
                    "red_flags": scenario.red_flags,
                    "tags": scenario.tags,
                    "difficulty": scenario.difficulty,
                },
            )
        )
    return samples


def personas_to_samples(personas: list, generator: ScenarioGenerator) -> list[Sample]:
    """Convert EMPATH personas to Inspect AI samples via scenarios."""
    scenarios = generator.generate_batch(personas)
    return scenarios_to_samples(scenarios)


@task
def empath_task(
    locale: str | None = None,
    scenario_type: str | None = None,
    include_personas: bool = True,
    judge_model: str | None = None,
    max_samples: int | None = None,
) -> Task:
    """
    EMPATH evaluation task for emotional support AI chatbots.

    This task evaluates AI chatbots on the EMPATH framework's 14 metrics
    across crisis detection, therapeutic quality, conversational ability,
    emotional safety, and cultural sensitivity.

    Args:
        locale: Filter scenarios by locale (es-MX, en-US). If None, includes all.
        scenario_type: Filter by scenario type (crisis, therapeutic, cultural).
        include_personas: If True, also generates scenarios from personas.
        judge_model: Model to use for judging. Defaults to Claude Opus 4.5.
        max_samples: Maximum number of samples to evaluate.

    Returns:
        Inspect AI Task configured for EMPATH evaluation.

    Example:
        ```python
        from inspect_ai import eval
        from empath import empath_task

        # Evaluate a target model on all scenarios
        eval(empath_task(), model="openai/gpt-4o-mini")

        # Evaluate only Spanish crisis scenarios
        eval(empath_task(locale="es-MX", scenario_type="crisis"), model="openai/gpt-4o-mini")
        ```
    """
    # Collect scenarios
    scenarios = list(ALL_SCENARIOS)

    # Add persona-generated scenarios if requested
    if include_personas:
        generator = ScenarioGenerator()

        # Add from Spanish personas
        scenarios.extend(generator.generate_batch(ES_MX_PERSONAS))

        # Add from English personas
        scenarios.extend(generator.generate_batch(EN_US_PERSONAS))

    # Filter by locale
    if locale:
        scenarios = [s for s in scenarios if s.locale == locale]

    # Filter by scenario type
    if scenario_type:
        scenarios = [s for s in scenarios if s.scenario_type.value == scenario_type]

    # Limit samples
    if max_samples and len(scenarios) > max_samples:
        scenarios = scenarios[:max_samples]

    # Convert to samples
    samples = scenarios_to_samples(scenarios)

    # Create dataset
    dataset = MemoryDataset(samples=samples, name="empath")

    # Create the judge scorer
    scorer: Scorer = empath_judge(
        dimensions=EMPATH_DIMENSIONS,
        model=judge_model,
    )

    return Task(
        dataset=dataset,
        solver=generate(),
        scorer=scorer,
        name="empath",
        metadata={
            "framework": "EMPATH",
            "version": "0.1.0",
            "dimensions": list(EMPATH_DIMENSIONS.keys()),
            "locale_filter": locale,
            "scenario_type_filter": scenario_type,
            "total_scenarios": len(scenarios),
        },
    )


@task
def empath_crisis_task(
    locale: str | None = None,
    judge_model: str | None = None,
) -> Task:
    """
    EMPATH crisis-focused evaluation task.

    A subset of the full EMPATH task focusing specifically on crisis
    scenarios to evaluate safety-critical behaviors.

    Args:
        locale: Filter by locale (es-MX, en-US). If None, includes all.
        judge_model: Model to use for judging.

    Returns:
        Inspect AI Task configured for crisis evaluation.
    """
    scenarios = list(CRISIS_SCENARIOS)

    if locale:
        scenarios = [s for s in scenarios if s.locale == locale]

    samples = scenarios_to_samples(scenarios)
    dataset = MemoryDataset(samples=samples, name="empath-crisis")

    # Use only crisis-relevant dimensions
    crisis_dimensions = {
        "crisis_detection": EMPATH_DIMENSIONS["crisis_detection"],
        "crisis_resource_provision": EMPATH_DIMENSIONS["crisis_resource_provision"],
        "harmful_response": EMPATH_DIMENSIONS["harmful_response"],
        "clinical_appropriateness": EMPATH_DIMENSIONS["clinical_appropriateness"],
        "empathy_vs_manipulation": EMPATH_DIMENSIONS["empathy_vs_manipulation"],
    }

    scorer: Scorer = empath_judge(
        dimensions=crisis_dimensions,
        model=judge_model,
    )

    return Task(
        dataset=dataset,
        solver=generate(),
        scorer=scorer,
        name="empath-crisis",
        metadata={
            "framework": "EMPATH",
            "version": "0.1.0",
            "focus": "crisis",
            "dimensions": list(crisis_dimensions.keys()),
            "locale_filter": locale,
            "total_scenarios": len(scenarios),
        },
    )


@task
def empath_cultural_task(
    locale: str = "es-MX",
    judge_model: str | None = None,
) -> Task:
    """
    EMPATH cultural sensitivity evaluation task.

    Focuses on cultural scenarios to evaluate the AI's cultural
    competence and sensitivity.

    Args:
        locale: Locale to evaluate (es-MX or en-US).
        judge_model: Model to use for judging.

    Returns:
        Inspect AI Task configured for cultural evaluation.
    """
    from empath.scenarios import CULTURAL_SCENARIOS

    scenarios = [s for s in CULTURAL_SCENARIOS if s.locale == locale]
    samples = scenarios_to_samples(scenarios)
    dataset = MemoryDataset(samples=samples, name=f"empath-cultural-{locale}")

    # Use cultural-relevant dimensions
    cultural_dimensions = {
        "cultural_sensitivity": EMPATH_DIMENSIONS["cultural_sensitivity"],
        "boundary_maintenance": EMPATH_DIMENSIONS["boundary_maintenance"],
        "professional_referral": EMPATH_DIMENSIONS["professional_referral"],
        "empathy_vs_manipulation": EMPATH_DIMENSIONS["empathy_vs_manipulation"],
        "sycophancy": EMPATH_DIMENSIONS["sycophancy"],
    }

    scorer: Scorer = empath_judge(
        dimensions=cultural_dimensions,
        model=judge_model,
    )

    return Task(
        dataset=dataset,
        solver=generate(),
        scorer=scorer,
        name=f"empath-cultural-{locale}",
        metadata={
            "framework": "EMPATH",
            "version": "0.1.0",
            "focus": "cultural",
            "locale": locale,
            "dimensions": list(cultural_dimensions.keys()),
            "total_scenarios": len(scenarios),
        },
    )
