"""The paper's linear residual adapter and exact parameter-budget helpers."""

from __future__ import annotations

from dataclasses import dataclass


def residual_parameters_per_block(hidden_size: int, bottleneck_dim: int) -> int:
    """RMSNorm gamma + Down W/b + Up W/b + one scalar scale."""
    if hidden_size <= 0 or bottleneck_dim <= 0:
        raise ValueError("hidden_size and bottleneck_dim must be positive")
    return 2 * hidden_size * bottleneck_dim + bottleneck_dim + 2 * hidden_size + 1


def residual_parameter_count(hidden_size: int, bottleneck_dim: int, active_blocks: int) -> int:
    return residual_parameters_per_block(hidden_size, bottleneck_dim) * active_blocks


@dataclass(frozen=True)
class ResidualAllocation:
    name: str
    active_layers: tuple[int, ...]
    bottleneck_dim: int
    hidden_size: int = 1024

    @property
    def trainable_parameters(self) -> int:
        return residual_parameter_count(self.hidden_size, self.bottleneck_dim, len(self.active_layers))


FULL_28_RESIDUAL = ResidualAllocation("Full-28", tuple(range(28)), 128)
LATE_16_RESIDUAL = ResidualAllocation("Late-16", tuple(range(12, 28)), 225)


def build_linear_residual_adapter(hidden_size: int, bottleneck_dim: int, eps: float = 1e-6):
    """Build the canonical no-activation adapter when PyTorch is installed.

    The formal residual baseline is ``RMSNorm -> Down -> Up -> scale ->
    residual add``.  It deliberately does *not* use the legacy SiLU capsule.
    """
    try:
        import torch
        import torch.nn as nn
    except ImportError as error:  # pragma: no cover - exercised by docs only
        raise RuntimeError("PyTorch is required for model integration; install depth-gap-gain[training].") from error

    class LinearResidualAdapter(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.norm = nn.RMSNorm(hidden_size, eps=eps)
            self.down_proj = nn.Linear(hidden_size, bottleneck_dim, bias=True)
            self.up_proj = nn.Linear(bottleneck_dim, hidden_size, bias=True)
            self.scale = nn.Parameter(torch.ones(()))
            nn.init.zeros_(self.up_proj.weight)
            nn.init.zeros_(self.up_proj.bias)

        def forward(self, hidden_states):
            delta = self.up_proj(self.down_proj(self.norm(hidden_states)))
            return hidden_states + self.scale.to(dtype=delta.dtype) * delta

    return LinearResidualAdapter()
