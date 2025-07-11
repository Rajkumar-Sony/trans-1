"""
Validation Interface

Abstract interface for validation operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class ValidationSeverity(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationResult:
    """Result of a validation operation."""
    
    def __init__(self, is_valid: bool = True, severity: ValidationSeverity = ValidationSeverity.INFO,
                 message: str = "", code: str = "", details: Optional[Dict[str, Any]] = None):
        self.is_valid = is_valid
        self.severity = severity
        self.message = message
        self.code = code
        self.details = details or {}
    
    @property
    def is_error(self) -> bool:
        """Check if this is an error result."""
        return self.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
    
    @property
    def is_warning(self) -> bool:
        """Check if this is a warning result."""
        return self.severity == ValidationSeverity.WARNING


class ValidationReport:
    """Collection of validation results."""
    
    def __init__(self):
        self.results: List[ValidationResult] = []
    
    def add_result(self, result: ValidationResult) -> None:
        """Add a validation result."""
        self.results.append(result)
    
    def add_error(self, message: str, code: str = "", details: Optional[Dict[str, Any]] = None) -> None:
        """Add an error result."""
        self.results.append(ValidationResult(
            is_valid=False, severity=ValidationSeverity.ERROR,
            message=message, code=code, details=details
        ))
    
    def add_warning(self, message: str, code: str = "", details: Optional[Dict[str, Any]] = None) -> None:
        """Add a warning result."""
        self.results.append(ValidationResult(
            is_valid=True, severity=ValidationSeverity.WARNING,
            message=message, code=code, details=details
        ))
    
    def add_info(self, message: str, code: str = "", details: Optional[Dict[str, Any]] = None) -> None:
        """Add an info result."""
        self.results.append(ValidationResult(
            is_valid=True, severity=ValidationSeverity.INFO,
            message=message, code=code, details=details
        ))
    
    @property
    def is_valid(self) -> bool:
        """Check if all validations passed."""
        return all(result.is_valid for result in self.results)
    
    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return any(result.is_error for result in self.results)
    
    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return any(result.is_warning for result in self.results)
    
    def get_errors(self) -> List[ValidationResult]:
        """Get all error results."""
        return [result for result in self.results if result.is_error]
    
    def get_warnings(self) -> List[ValidationResult]:
        """Get all warning results."""
        return [result for result in self.results if result.is_warning]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        return {
            'total_checks': len(self.results),
            'passed': sum(1 for r in self.results if r.is_valid),
            'failed': sum(1 for r in self.results if not r.is_valid),
            'errors': len(self.get_errors()),
            'warnings': len(self.get_warnings()),
            'is_valid': self.is_valid
        }


class ValidationInterface(ABC):
    """Interface for validation operations."""
    
    @abstractmethod
    async def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """Validate data and return validation report."""
        pass
    
    @abstractmethod
    def get_validation_rules(self) -> List[str]:
        """Get list of validation rules applied by this validator."""
        pass
    
    @abstractmethod
    def get_supported_types(self) -> List[type]:
        """Get list of data types supported by this validator."""
        pass
