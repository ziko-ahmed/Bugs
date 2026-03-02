"""Tests for Extremely Difficult Bug: Task Scheduler"""

import pytest
from src.scheduler import TaskScheduler, TaskStatus, CycleError


class TestExecutionOrder:
    def test_simple_chain(self):
        """A -> B -> C should execute A, B, C in order."""
        s = TaskScheduler()
        s.add_task("C")
        s.add_task("B", dependencies=["C"])
        s.add_task("A", dependencies=["B"])

        order = s.get_execution_order()
        assert order.index("C") < order.index("B") < order.index("A")

    def test_independent_tasks_included(self):
        """All tasks must appear in execution order, even those with no dependencies."""
        s = TaskScheduler()
        s.add_task("standalone")
        s.add_task("dep_task", dependencies=["standalone"])

        order = s.get_execution_order()
        assert "standalone" in order      # Will fail: skipped because it has no dependencies
        assert "dep_task" in order

    def test_cycle_detection(self):
        """Circular dependency A -> B -> C -> A should raise CycleError."""
        s = TaskScheduler()
        s.add_task("A", dependencies=["C"])
        s.add_task("B", dependencies=["A"])
        s.add_task("C", dependencies=["B"])

        with pytest.raises(CycleError):
            s.get_execution_order()

    def test_disconnected_cycle_detection(self):
        """Cycle in a disconnected component should still be detected."""
        s = TaskScheduler()
        # Connected component (no cycle)
        s.add_task("X")
        s.add_task("Y", dependencies=["X"])
        # Disconnected cycle
        s.add_task("A", dependencies=["B"])
        s.add_task("B", dependencies=["A"])

        with pytest.raises(CycleError):
            s.get_execution_order()   # Will fail: disconnected cycle not detected


class TestPriority:
    def test_simple_priority(self):
        s = TaskScheduler()
        s.add_task("A", priority=10)
        assert s.calculate_effective_priority("A") == 10

    def test_chain_priority(self):
        s = TaskScheduler()
        s.add_task("C", priority=5)
        s.add_task("B", priority=3, dependencies=["C"])
        s.add_task("A", priority=1, dependencies=["B"])

        # A(1) + B(3) + C(5) = 9
        assert s.calculate_effective_priority("A") == 9

    def test_diamond_priority_no_double_count(self):
        """
        Diamond: A -> B -> D, A -> C -> D
        D's priority should only be counted once.
        """
        s = TaskScheduler()
        s.add_task("D", priority=10)
        s.add_task("B", priority=2, dependencies=["D"])
        s.add_task("C", priority=3, dependencies=["D"])
        s.add_task("A", priority=1, dependencies=["B", "C"])

        # A(1) + B(2) + C(3) + D(10) = 16 (D counted once)
        assert s.calculate_effective_priority("A") == 16  # Will fail: D counted twice = 26


class TestParallelGroups:
    def test_independent_tasks(self):
        """Tasks with no dependencies should all be in group 0."""
        s = TaskScheduler()
        s.add_task("A")
        s.add_task("B")
        s.add_task("C")

        groups = s.get_parallel_groups()
        assert len(groups) == 1
        assert set(groups[0]) == {"A", "B", "C"}

    def test_chain_groups(self):
        """A -> B -> C should produce 3 separate groups."""
        s = TaskScheduler()
        s.add_task("C")
        s.add_task("B", dependencies=["C"])
        s.add_task("A", dependencies=["B"])

        groups = s.get_parallel_groups()
        assert len(groups) == 3        # Will fail: tasks end up in same groups
        assert "C" in groups[0]
        assert "B" in groups[1]
        assert "A" in groups[2]

    def test_parallel_deps(self):
        """
        D depends on both B and C (independent).
        Groups: [B, C], [D]
        """
        s = TaskScheduler()
        s.add_task("B")
        s.add_task("C")
        s.add_task("D", dependencies=["B", "C"])

        groups = s.get_parallel_groups()
        assert len(groups) == 2
        assert set(groups[0]) == {"B", "C"}
        assert groups[1] == ["D"]


class TestTaskCompletion:
    def test_single_dependency(self):
        s = TaskScheduler()
        s.add_task("A")
        s.add_task("B", dependencies=["A"])

        newly_ready = s.complete_task("A")
        assert "B" in newly_ready
        assert s.get_task("B").status == TaskStatus.READY

    def test_multiple_dependencies_all_required(self):
        """B depends on both A and C. B should only be ready when BOTH are done."""
        s = TaskScheduler()
        s.add_task("A")
        s.add_task("C")
        s.add_task("B", dependencies=["A", "C"])

        # Complete only A — B should NOT be ready yet
        newly_ready = s.complete_task("A")
        assert "B" not in newly_ready     # Will fail: any() triggers ready too early
        assert s.get_task("B").status == TaskStatus.PENDING

        # Complete C — NOW B should be ready
        newly_ready = s.complete_task("C")
        assert "B" in newly_ready
