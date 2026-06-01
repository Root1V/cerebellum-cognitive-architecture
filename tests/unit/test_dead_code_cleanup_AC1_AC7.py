"""
Unit tests for spec 002: Remove Dead Code & Fix Production Issues.

Implements: memory/specs/002-remove-dead-code-fix-production-issues.md — AC-1 through AC-7
"""
from __future__ import annotations

import importlib
import logging
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# AC-1: event_loop.py is deleted
# ---------------------------------------------------------------------------


def test_event_loop_file_does_not_exist_AC1() -> None:
    """AC-1: cognition/runtime/event_loop.py must not exist in the repository."""
    path = Path("src/cerebellum/cognition/runtime/event_loop.py")
    assert not path.exists(), f"Dead file still present: {path}"


def test_event_loop_module_is_not_importable_AC1() -> None:
    """AC-1: importing the dead module must raise ModuleNotFoundError."""
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("cerebellum.cognition.runtime.event_loop")


# ---------------------------------------------------------------------------
# AC-2: cognition/runtime/rules.py is deleted
# ---------------------------------------------------------------------------


def test_runtime_rules_file_does_not_exist_AC2() -> None:
    """AC-2: cognition/runtime/rules.py must not exist."""
    path = Path("src/cerebellum/cognition/runtime/rules.py")
    assert not path.exists(), f"Dead file still present: {path}"


def test_runtime_rules_module_is_not_importable_AC2() -> None:
    """AC-2: importing the dead module must raise ModuleNotFoundError."""
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("cerebellum.cognition.runtime.rules")


# ---------------------------------------------------------------------------
# AC-3: multimodal_perception.py is deleted
# ---------------------------------------------------------------------------


def test_multimodal_perception_file_does_not_exist_AC3() -> None:
    """AC-3: cognition/perception/multimodal_perception.py must not exist."""
    path = Path("src/cerebellum/cognition/perception/multimodal_perception.py")
    assert not path.exists(), f"Dead file still present: {path}"


def test_multimodal_perception_module_is_not_importable_AC3() -> None:
    """AC-3: importing the dead module must raise ModuleNotFoundError."""
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("cerebellum.cognition.perception.multimodal_perception")


# ---------------------------------------------------------------------------
# AC-4: task_graph_planner.py is deleted
# ---------------------------------------------------------------------------


def test_task_graph_planner_file_does_not_exist_AC4() -> None:
    """AC-4: cognition/planners/task_graph_planner.py must not exist."""
    path = Path("src/cerebellum/cognition/planners/task_graph_planner.py")
    assert not path.exists(), f"Dead file still present: {path}"


def test_task_graph_planner_module_is_not_importable_AC4() -> None:
    """AC-4: importing the dead module must raise ModuleNotFoundError."""
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("cerebellum.cognition.planners.task_graph_planner")


# ---------------------------------------------------------------------------
# AC-5: tools/code_executor.py is deleted
# ---------------------------------------------------------------------------


def test_code_executor_file_does_not_exist_AC5() -> None:
    """AC-5: tools/code_executor.py must not exist."""
    path = Path("src/cerebellum/tools/code_executor.py")
    assert not path.exists(), f"Dead file still present: {path}"


def test_code_executor_module_is_not_importable_AC5() -> None:
    """AC-5: importing the dead module must raise ModuleNotFoundError."""
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("cerebellum.tools.code_executor")


# ---------------------------------------------------------------------------
# AC-6: Tracer.trace() uses logger.debug, not print()
# ---------------------------------------------------------------------------


def test_tracer_uses_logger_debug_not_print_AC6(caplog: pytest.LogCaptureFixture) -> None:
    """AC-6: Tracer.trace() must emit to logger at DEBUG level, not stdout."""
    from cerebellum.infraestructure.observability.tracer import Tracer

    tracer = Tracer()
    with caplog.at_level(logging.DEBUG, logger="cerebellum.observability.tracer"):
        tracer.trace("test_event", {"key": "value"})

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.DEBUG
    assert "test_event" in record.getMessage()
    assert record.name == "cerebellum.observability.tracer"


def test_tracer_does_not_write_to_stdout_AC6(capsys: pytest.CaptureFixture[str]) -> None:
    """AC-6: Tracer.trace() must produce no stdout output."""
    from cerebellum.infraestructure.observability.tracer import Tracer

    tracer = Tracer()
    tracer.trace("silent_event", "payload")
    captured = capsys.readouterr()
    assert captured.out == "", "Tracer must not write to stdout"


# ---------------------------------------------------------------------------
# AC-7: No print() in production source tree
# ---------------------------------------------------------------------------


def test_no_print_statements_in_src_AC7() -> None:
    """AC-7: No print() call exists anywhere under src/cerebellum/."""
    src_root = Path("src/cerebellum")
    violations: list[str] = []
    for py_file in src_root.rglob("*.py"):
        lines = py_file.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            # Exclude commented-out lines
            if stripped.startswith("#"):
                continue
            if "print(" in line:
                violations.append(f"{py_file}:{i}: {line.rstrip()}")
    assert violations == [], "print() found in production source:\n" + "\n".join(violations)


# ---------------------------------------------------------------------------
# AC-2 (import safety): package-level import still works after deletions
# ---------------------------------------------------------------------------


def test_cerebellum_package_imports_cleanly_AC2() -> None:
    """AC-2: `import cerebellum` must succeed with no ImportError after deletions."""
    import cerebellum  # noqa: F401
