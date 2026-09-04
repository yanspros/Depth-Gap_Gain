"""Retrospective comparator diagnostics (not DGG replacements)."""

from .gradient import normalized_gradient_score
from .displacement import relative_displacement
from .representation import cosine_drift

__all__ = ["normalized_gradient_score", "relative_displacement", "cosine_drift"]
