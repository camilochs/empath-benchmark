"""
Intent Extractor

Extracts abstract intent patterns from real conversation data
for synthetic scenario generation while preserving privacy.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractedIntent:
    """
    An abstract intent pattern extracted from conversation data.

    Contains no PII - only abstract patterns that can be used
    to generate synthetic scenarios.
    """

    # Intent classification
    category: str  # e.g., "crisis", "anxiety", "relationship"
    subcategory: str  # e.g., "suicidal_ideation", "work_stress"
    locale: str

    # Abstract patterns (no PII)
    emotional_themes: list[str] = field(default_factory=list)
    situational_elements: list[str] = field(default_factory=list)
    linguistic_patterns: list[str] = field(default_factory=list)

    # Risk assessment
    crisis_indicators: list[str] = field(default_factory=list)
    crisis_level: int = 0  # 0-3

    # Metadata
    frequency: int = 1  # How often this pattern appears
    metadata: dict[str, Any] = field(default_factory=dict)


class IntentExtractor:
    """
    Extracts abstract intent patterns from real conversation data.

    This extractor is designed to:
    1. Identify emotional and situational patterns
    2. Extract crisis indicators
    3. Capture linguistic patterns by locale
    4. Never store or output any PII

    The output is abstract patterns that can be used to generate
    synthetic scenarios without any connection to real users.
    """

    # Crisis keywords by locale
    CRISIS_KEYWORDS = {
        "es-MX": {
            "high": [
                "suicidio", "matarme", "acabar con mi vida", "ya no quiero vivir",
                "plan para", "he decidido", "esta noche", "tengo las pastillas"
            ],
            "medium": [
                "no puedo más", "quiero desaparecer", "estaría mejor muerto",
                "no le veo sentido", "quiero morirme", "sería mejor si no existiera"
            ],
            "low": [
                "cansada de vivir", "agotado", "sin esperanza", "vacío",
                "no tiene caso", "¿para qué?"
            ],
        },
        "en-US": {
            "high": [
                "suicide", "kill myself", "end my life", "don't want to live",
                "plan to", "decided to", "tonight", "have the pills"
            ],
            "medium": [
                "can't take it anymore", "want to disappear", "better off dead",
                "see no point", "want to die", "better if I didn't exist"
            ],
            "low": [
                "tired of living", "exhausted", "hopeless", "empty",
                "what's the point", "why bother"
            ],
        },
    }

    # Emotional themes to detect
    EMOTIONAL_THEMES = {
        "es-MX": {
            "anxiety": ["ansiedad", "nervios", "preocupación", "miedo", "pánico", "angustia"],
            "depression": ["tristeza", "vacío", "sin ganas", "deprimido", "abatido"],
            "anger": ["enojo", "coraje", "rabia", "frustración", "impotencia"],
            "shame": ["vergüenza", "culpa", "fracaso", "decepción"],
            "loneliness": ["solo", "soledad", "aislado", "nadie me entiende"],
            "grief": ["pérdida", "duelo", "extraño", "murió", "falleció"],
        },
        "en-US": {
            "anxiety": ["anxiety", "nervous", "worried", "scared", "panic", "anxious"],
            "depression": ["sad", "empty", "no motivation", "depressed", "down"],
            "anger": ["angry", "mad", "furious", "frustrated", "helpless"],
            "shame": ["ashamed", "guilty", "failure", "disappointed"],
            "loneliness": ["alone", "lonely", "isolated", "no one understands"],
            "grief": ["loss", "grieving", "miss", "died", "passed away"],
        },
    }

    # Situational patterns
    SITUATIONAL_PATTERNS = {
        "es-MX": {
            "work": ["trabajo", "jefe", "oficina", "despido", "estrés laboral"],
            "family": ["familia", "papás", "mamá", "hermanos", "hijos"],
            "relationship": ["pareja", "novio", "esposo", "relación", "ruptura"],
            "academic": ["escuela", "examen", "universidad", "reprobar", "calificaciones"],
            "financial": ["dinero", "deudas", "economía", "no alcanza", "gastos"],
            "health": ["enfermedad", "diagnóstico", "dolor", "síntomas", "médico"],
        },
        "en-US": {
            "work": ["work", "boss", "office", "fired", "job stress"],
            "family": ["family", "parents", "mom", "dad", "siblings", "kids"],
            "relationship": ["partner", "boyfriend", "girlfriend", "spouse", "breakup"],
            "academic": ["school", "exam", "college", "failing", "grades"],
            "financial": ["money", "debt", "bills", "can't afford", "expenses"],
            "health": ["illness", "diagnosis", "pain", "symptoms", "doctor"],
        },
    }

    def __init__(self, locale: str = "es-MX"):
        """
        Initialize the intent extractor.

        Args:
            locale: Default locale for extraction
        """
        self.locale = locale

    def extract(self, text: str, locale: str | None = None) -> ExtractedIntent:
        """
        Extract abstract intent patterns from text.

        Args:
            text: The text to analyze (will not be stored)
            locale: Locale override

        Returns:
            ExtractedIntent with abstract patterns only
        """
        locale = locale or self.locale
        text_lower = text.lower()

        # Extract emotional themes
        emotional_themes = self._extract_themes(
            text_lower, self.EMOTIONAL_THEMES.get(locale, {})
        )

        # Extract situational elements
        situational_elements = self._extract_themes(
            text_lower, self.SITUATIONAL_PATTERNS.get(locale, {})
        )

        # Assess crisis level
        crisis_level, crisis_indicators = self._assess_crisis(text_lower, locale)

        # Extract linguistic patterns (abstract, no content)
        linguistic_patterns = self._extract_linguistic_patterns(text, locale)

        # Determine category
        category = self._determine_category(
            crisis_level, emotional_themes, situational_elements
        )

        return ExtractedIntent(
            category=category,
            subcategory=self._determine_subcategory(
                emotional_themes, situational_elements
            ),
            locale=locale,
            emotional_themes=emotional_themes,
            situational_elements=situational_elements,
            linguistic_patterns=linguistic_patterns,
            crisis_indicators=crisis_indicators,
            crisis_level=crisis_level,
        )

    def _extract_themes(
        self, text: str, theme_dict: dict[str, list[str]]
    ) -> list[str]:
        """Extract themes present in text."""
        found_themes = []
        for theme, keywords in theme_dict.items():
            if any(kw in text for kw in keywords):
                found_themes.append(theme)
        return found_themes

    def _assess_crisis(
        self, text: str, locale: str
    ) -> tuple[int, list[str]]:
        """
        Assess crisis level from text.

        Returns:
            Tuple of (crisis_level 0-3, list of abstract indicators)
        """
        keywords = self.CRISIS_KEYWORDS.get(locale, {})
        indicators = []

        # Check high severity
        if any(kw in text for kw in keywords.get("high", [])):
            indicators.append("explicit_intent")
            return 3, indicators

        # Check medium severity
        if any(kw in text for kw in keywords.get("medium", [])):
            indicators.append("passive_ideation")
            return 2, indicators

        # Check low severity
        if any(kw in text for kw in keywords.get("low", [])):
            indicators.append("hopelessness")
            return 1, indicators

        return 0, []

    def _extract_linguistic_patterns(
        self, text: str, locale: str
    ) -> list[str]:
        """
        Extract abstract linguistic patterns (no content).

        Patterns like sentence structure, formality level, etc.
        """
        patterns = []

        # Detect formality
        if locale == "es-MX":
            if "usted" in text.lower():
                patterns.append("formal_register")
            elif "tú" in text.lower():
                patterns.append("informal_register")
        else:
            # Could add English formality detection
            pass

        # Detect question density
        question_count = text.count("?")
        if question_count > 2:
            patterns.append("high_question_density")
        elif question_count > 0:
            patterns.append("contains_questions")

        # Detect sentence length patterns
        sentences = re.split(r"[.!?]+", text)
        avg_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if avg_length > 15:
            patterns.append("long_sentences")
        elif avg_length < 6:
            patterns.append("short_sentences")

        return patterns

    def _determine_category(
        self,
        crisis_level: int,
        emotional_themes: list[str],
        situational_elements: list[str],
    ) -> str:
        """Determine primary category."""
        if crisis_level >= 2:
            return "crisis"

        if "depression" in emotional_themes:
            return "depression"
        if "anxiety" in emotional_themes:
            return "anxiety"
        if "grief" in emotional_themes:
            return "grief"
        if "relationship" in situational_elements:
            return "relationship"
        if "family" in situational_elements:
            return "family"
        if "work" in situational_elements:
            return "work_stress"

        return "general_support"

    def _determine_subcategory(
        self,
        emotional_themes: list[str],
        situational_elements: list[str],
    ) -> str:
        """Determine subcategory from themes and elements."""
        if emotional_themes and situational_elements:
            return f"{situational_elements[0]}_{emotional_themes[0]}"
        elif emotional_themes:
            return emotional_themes[0]
        elif situational_elements:
            return situational_elements[0]
        return "unspecified"

    def batch_extract(
        self, texts: list[str], locale: str | None = None
    ) -> list[ExtractedIntent]:
        """
        Extract intents from multiple texts.

        Args:
            texts: List of texts to analyze
            locale: Locale override

        Returns:
            List of ExtractedIntent objects
        """
        return [self.extract(text, locale) for text in texts]

    def aggregate_patterns(
        self, intents: list[ExtractedIntent]
    ) -> dict[str, Any]:
        """
        Aggregate patterns across multiple intents for analysis.

        Args:
            intents: List of extracted intents

        Returns:
            Aggregated pattern statistics
        """
        stats = {
            "total": len(intents),
            "by_category": {},
            "by_crisis_level": {0: 0, 1: 0, 2: 0, 3: 0},
            "emotional_themes": {},
            "situational_elements": {},
        }

        for intent in intents:
            # Category counts
            stats["by_category"][intent.category] = (
                stats["by_category"].get(intent.category, 0) + 1
            )

            # Crisis level counts
            stats["by_crisis_level"][intent.crisis_level] += 1

            # Theme counts
            for theme in intent.emotional_themes:
                stats["emotional_themes"][theme] = (
                    stats["emotional_themes"].get(theme, 0) + 1
                )

            # Situational counts
            for element in intent.situational_elements:
                stats["situational_elements"][element] = (
                    stats["situational_elements"].get(element, 0) + 1
                )

        return stats
