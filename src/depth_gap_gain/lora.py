"""Canonical LoRA allocation metadata; PEFT itself is a dependency."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


TARGET_PROJECTIONS = (
    "attn_q_proj", "attn_k_proj", "attn_v_proj", "attn_o_proj",
    "mlp_gate_proj", "mlp_up_proj", "mlp_down_proj",
)


@dataclass(frozen=True)
class LoRAAllocation:
    name: str
    active_layers: tuple[int, ...]
    rank: int
    alpha: int
    dropout: float = 0.0
    target_modules: tuple[str, ...] = TARGET_PROJECTIONS

    def peft_config_kwargs(self) -> dict[str, object]:
        return {
            "r": self.rank,
            "lora_alpha": self.alpha,
            "target_modules": list(self.target_modules),
            "lora_dropout": self.dropout,
            "bias": "none",
        }


FULL_28_LORA = LoRAAllocation("Full-28", tuple(range(28)), rank=12, alpha=12)
LATE_16_LORA = LoRAAllocation("Late-16", tuple(range(12, 28)), rank=21, alpha=21)


def lora_parameter_count(named_shapes: Mapping[str, Sequence[int]], allocation: LoRAAllocation) -> int:
    """Calculate LoRA A/B parameters from actual selected projection shapes.

    ``named_shapes`` must map ``llm.layers.<i>.<target>`` to a two-dimensional
    (out_features, in_features) shape.  This prevents the invalid shortcut of
    equating rank products without inspecting real projection geometry.
    """
    total = 0
    expected = {f"llm.layers.{layer}.{target}" for layer in allocation.active_layers for target in allocation.target_modules}
    absent = sorted(expected - set(named_shapes))
    if absent:
        raise ValueError(f"missing selected LoRA projection shapes: {absent[:3]}")
    for name in expected:
        shape = tuple(int(x) for x in named_shapes[name])
        if len(shape) != 2 or min(shape) <= 0:
            raise ValueError(f"invalid linear projection shape for {name}: {shape}")
        out_features, in_features = shape
        total += allocation.rank * (in_features + out_features)
    return total
