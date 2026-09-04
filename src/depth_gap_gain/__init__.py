"""Depth-Gap Gain reference utilities.

The package implements the frozen DGG/Q16 decision logic and lightweight
diagnostic helpers.  Model-specific OmniVoice loading remains an integration
task because checkpoints, audio, and evaluators are deliberately not shipped.
"""

from .dgg import analyze_dgg, decide_depth, evaluate_q16

__all__ = ["analyze_dgg", "decide_depth", "evaluate_q16"]
__version__ = "0.1.0"
