from depth_gap_gain.adapters import FULL_28_RESIDUAL, LATE_16_RESIDUAL
from depth_gap_gain.lora import FULL_28_LORA, LATE_16_LORA, TARGET_PROJECTIONS, lora_parameter_count


def projection_shapes():
    # Synthetic shape registry whose per-layer input+output sum is 22,528.
    dims = {
        "attn_q_proj": (1024, 1024), "attn_k_proj": (1024, 1024),
        "attn_v_proj": (1024, 1024), "attn_o_proj": (1024, 1024),
        "mlp_gate_proj": (3754, 1024), "mlp_up_proj": (3754, 1024),
        "mlp_down_proj": (3756, 1024),
    }
    return {f"llm.layers.{layer}.{target}": dims[target] for layer in range(28) for target in TARGET_PROJECTIONS}


def test_residual_budget_matches_canonical_contract():
    assert FULL_28_RESIDUAL.trainable_parameters == 7_400_988
    assert LATE_16_RESIDUAL.trainable_parameters == 7_409_184


def test_lora_budget_is_calculated_from_projection_shapes():
    shapes = projection_shapes()
    assert lora_parameter_count(shapes, FULL_28_LORA) == 7_569_408
    assert lora_parameter_count(shapes, LATE_16_LORA) == 7_569_408
