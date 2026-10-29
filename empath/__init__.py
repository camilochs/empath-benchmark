"""
EMPATH: Emotional Mental-health Protocol for AI Therapeutic Harm-prevention

A multilingual evaluation framework for emotional support and mental health chatbots.
Built on Inspect AI and Petri, designed for evaluating AI systems in therapeutic contexts.

Key Features:
- 14 consolidated metrics across 5 dimensions
- Multilingual support (es-MX, en-US)
- Crisis detection and safety evaluation
- Therapeutic quality assessment
- Cultural sensitivity metrics
- Dynamic scenario generation via Petri auditor

Architecture:
- Auditor (Claude Sonnet 4): Generates scenarios from seed instructions
- Target: the emotional-support chatbot under evaluation (pluggable provider)
- Judge (Claude Opus 4.5): Evaluates using EMPATH's 14 metrics
"""

__version__ = "0.1.0"

# Core exports (always available)
from empath.dimensions import EMPATH_DIMENSIONS

__all__ = [
    "EMPATH_DIMENSIONS",
    "__version__",
]

# Seed instructions for dynamic scenario generation
try:
    from empath.seeds import ALL_SEEDS, get_all_seeds_list
    __all__.extend(["ALL_SEEDS", "get_all_seeds_list"])
except ImportError:
    pass

# Optional exports that require inspect_ai
try:
    from empath.tasks.empath_task import empath_task
    from empath.judges.empath_judge import empath_judge

    __all__.extend(["empath_task", "empath_judge"])
except ImportError:
    # inspect_ai not installed - tasks and judges not available
    pass

# Auditor task (using built-in solvers from empath.solvers)
try:
    from empath.tasks.empath_auditor_task import (
        empath_auditor_task,
        empath_crisis_auditor_task,
        empath_single_metric_task,
    )
    __all__.extend([
        "empath_auditor_task",
        "empath_crisis_auditor_task",
        "empath_single_metric_task",
    ])
except ImportError:
    # inspect_ai not installed - auditor tasks not available
    pass

# Solvers (moved from Petri)
try:
    from empath.solvers import auditor_agent
    __all__.append("auditor_agent")
except ImportError:
    pass
