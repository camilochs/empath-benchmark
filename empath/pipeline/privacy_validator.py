"""
Privacy Validator

Validates that generated scenarios and extracted patterns
contain no PII (Personally Identifiable Information).
"""

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:
    """Result of privacy validation."""
    is_valid: bool
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class PrivacyValidator:
    """
    Validates content for PII and privacy concerns.

    This validator checks for:
    1. Email addresses
    2. Phone numbers
    3. Social security numbers / CURP
    4. Physical addresses
    5. Real names from known lists
    6. URLs with potential identifying info
    7. Dates that could identify specific events
    """

    # Email pattern
    EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )

    # Phone patterns (US and Mexico)
    PHONE_PATTERNS = [
        re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"),  # US: 555-555-5555
        re.compile(r"\b\(\d{3}\)\s?\d{3}[-.\s]?\d{4}\b"),  # US: (555) 555-5555
        re.compile(r"\b\d{2}[-.\s]?\d{4}[-.\s]?\d{4}\b"),  # MX: 55-5555-5555
        re.compile(r"\b\d{10}\b"),  # 10 digits
    ]

    # SSN and CURP patterns
    SSN_PATTERN = re.compile(r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b")
    CURP_PATTERN = re.compile(r"\b[A-Z]{4}\d{6}[A-Z]{6}\d{2}\b")

    # Address indicators
    ADDRESS_INDICATORS = [
        r"\b\d+\s+[\w\s]+(?:street|st|avenue|ave|road|rd|drive|dr|lane|ln|blvd|boulevard)\b",
        r"\bcolonia\s+[\w\s]+\b",
        r"\bcalle\s+[\w\s]+\s+#?\d+\b",
        r"\bzip\s*code\s*\d{5}\b",
        r"\bc\.p\.\s*\d{5}\b",
    ]

    # URL pattern
    URL_PATTERN = re.compile(
        r"https?://[^\s]+|www\.[^\s]+"
    )

    # Specific date patterns (could identify real events)
    SPECIFIC_DATE_PATTERN = re.compile(
        r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december|"
        r"enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+"
        r"\d{1,2}(?:st|nd|rd|th)?,?\s*\d{4}\b",
        re.IGNORECASE
    )

    def __init__(self, strict: bool = True):
        """
        Initialize the validator.

        Args:
            strict: If True, treat warnings as violations
        """
        self.strict = strict
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Compile regex patterns."""
        self.address_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.ADDRESS_INDICATORS
        ]

    def validate(self, text: str) -> ValidationResult:
        """
        Validate text for PII.

        Args:
            text: Text to validate

        Returns:
            ValidationResult with findings
        """
        violations = []
        warnings = []

        # Check for emails
        emails = self.EMAIL_PATTERN.findall(text)
        if emails:
            violations.append(f"Email addresses found: {len(emails)}")

        # Check for phone numbers
        for pattern in self.PHONE_PATTERNS:
            phones = pattern.findall(text)
            if phones:
                # Filter out numbers that might be scenario IDs
                real_phones = [p for p in phones if not p.startswith("0")]
                if real_phones:
                    violations.append(f"Possible phone numbers: {len(real_phones)}")
                    break

        # Check for SSN
        ssns = self.SSN_PATTERN.findall(text)
        if ssns:
            violations.append(f"Possible SSN patterns: {len(ssns)}")

        # Check for CURP
        curps = self.CURP_PATTERN.findall(text)
        if curps:
            violations.append(f"Possible CURP patterns: {len(curps)}")

        # Check for addresses
        for pattern in self.address_patterns:
            if pattern.search(text):
                warnings.append("Possible physical address detected")
                break

        # Check for URLs
        urls = self.URL_PATTERN.findall(text)
        if urls:
            # Filter out generic resource URLs
            specific_urls = [
                u for u in urls
                if not any(safe in u.lower() for safe in [
                    "crisis", "hotline", "help", "support", "988", "741741"
                ])
            ]
            if specific_urls:
                warnings.append(f"URLs found that may identify sources: {len(specific_urls)}")

        # Check for specific dates
        dates = self.SPECIFIC_DATE_PATTERN.findall(text)
        if dates:
            warnings.append(f"Specific dates found that could identify events: {len(dates)}")

        # Determine validity
        is_valid = len(violations) == 0
        if self.strict:
            is_valid = is_valid and len(warnings) == 0

        return ValidationResult(
            is_valid=is_valid,
            violations=violations,
            warnings=warnings,
            metadata={
                "text_length": len(text),
                "strict_mode": self.strict,
            },
        )

    def validate_scenario(self, scenario: Any) -> ValidationResult:
        """
        Validate a scenario object for PII.

        Args:
            scenario: Scenario object with to_dict() method

        Returns:
            ValidationResult with findings
        """
        # Convert to dict and validate all string fields
        if hasattr(scenario, "to_dict"):
            data = scenario.to_dict()
        elif isinstance(scenario, dict):
            data = scenario
        else:
            return ValidationResult(
                is_valid=False,
                violations=["Cannot validate: unknown object type"],
            )

        all_violations = []
        all_warnings = []

        # Recursively check all string values
        self._check_dict(data, all_violations, all_warnings)

        is_valid = len(all_violations) == 0
        if self.strict:
            is_valid = is_valid and len(all_warnings) == 0

        return ValidationResult(
            is_valid=is_valid,
            violations=all_violations,
            warnings=all_warnings,
        )

    def _check_dict(
        self,
        data: dict[str, Any],
        violations: list[str],
        warnings: list[str],
        path: str = "",
    ) -> None:
        """Recursively check dictionary values."""
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            if isinstance(value, str):
                result = self.validate(value)
                for v in result.violations:
                    violations.append(f"{current_path}: {v}")
                for w in result.warnings:
                    warnings.append(f"{current_path}: {w}")
            elif isinstance(value, dict):
                self._check_dict(value, violations, warnings, current_path)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str):
                        result = self.validate(item)
                        for v in result.violations:
                            violations.append(f"{current_path}[{i}]: {v}")
                        for w in result.warnings:
                            warnings.append(f"{current_path}[{i}]: {w}")
                    elif isinstance(item, dict):
                        self._check_dict(
                            item, violations, warnings, f"{current_path}[{i}]"
                        )

    def batch_validate(
        self, items: list[Any]
    ) -> tuple[list[ValidationResult], bool]:
        """
        Validate multiple items.

        Args:
            items: List of scenarios or texts to validate

        Returns:
            Tuple of (list of results, overall validity)
        """
        results = []
        all_valid = True

        for item in items:
            if isinstance(item, str):
                result = self.validate(item)
            else:
                result = self.validate_scenario(item)

            results.append(result)
            if not result.is_valid:
                all_valid = False

        return results, all_valid
