"""Public-aggregate and estimator mechanics tests; no synthetic paper evidence."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("human_eval", ROOT / "scripts/reproduce_human_eval_table3.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_frozen_aggregate():
    release = json.loads(MODULE.DEFAULT_SUMMARY.read_text())
    assert MODULE.compare(release["cells"], release["cells"]) == 24
    assert release["protocol"]["total_judgments"] == 19200
    assert release["summary"]["ci_excludes_50"] == 18
    assert release["summary"]["ci_includes_50"] == 6
    assert release["provenance"]["raw_trials_public"] is False


def test_reject_changed_ci():
    release = json.loads(MODULE.DEFAULT_SUMMARY.read_text())
    altered = json.loads(json.dumps(release["cells"]))
    altered["Burmese Residual"]["criteria"]["pronunciation"]["ci95"][0] += 0.1
    with pytest.raises(ValueError, match="Table 3 mismatch"):
        MODULE.compare(altered, release["cells"])


def test_pool_before_truncation():
    # Synthetic unit-test matrices only, never paper results.
    grids = [np.tile([0., 1.], (20, 20)), np.zeros((20, 40))]
    actual = MODULE.pooled_components(grids)
    excess = []
    for grid in grids:
        p = grid.mean()
        excess.append([grid.mean(axis=1).var(ddof=1) - p*(1-p)/40,
                       grid.mean(axis=0).var(ddof=1) - p*(1-p)/20])
    expected = np.sqrt(np.maximum(np.mean(excess, axis=0), 0))
    assert np.allclose(actual, expected)


def test_aggregate_command_is_not_raw_replay(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "scripts/reproduce_human_eval_table3.py"),
                    "--output-dir", str(tmp_path)], check=True, capture_output=True)
    report = json.loads((tmp_path / "check.json").read_text())
    assert report["status"] == "HUMAN_EVAL_AGGREGATE_CHECK_PASS"
    assert report["raw_replayed"] is False
