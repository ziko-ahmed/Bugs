"""
🐛 Extremely Difficult Bug: Task scheduler with dependency resolution.

This is a multi-class system with cascading bugs across components.

Bug 1: Topological sort doesn't detect ALL cycles (misses cycles in disconnected components).
Bug 2: Priority calculation overflows when tasks have deep dependency chains.
Bug 3: Parallel execution groups are computed wrong — tasks with shared deps end up in same group.
Bug 4: Task completion doesn't properly propagate to dependents' readiness state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    name: str
    priority: int = 0
    dependencies: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None


class CycleError(Exception):
    """Raised when a dependency cycle is detected."""
    pass


class TaskScheduler:
    """
    Schedules tasks with dependency resolution and priority ordering.
    Supports parallel execution group computation.
    """

    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def add_task(self, name: str, priority: int = 0, dependencies: list[str] | None = None) -> Task:
        """Add a task to the scheduler."""
        task = Task(name=name, priority=priority, dependencies=dependencies or [])
        self._tasks[name] = task
        return task

    def get_task(self, name: str) -> Task | None:
        return self._tasks.get(name)

    def get_execution_order(self) -> list[str]:
        """
        Return tasks in valid execution order (topological sort).
        Raises CycleError if circular dependencies exist.
        """
        visited: set[str] = set()
        in_stack: set[str] = set()
        order: list[str] = []

        def dfs(name: str):
            if name in in_stack:
                raise CycleError(f"Cycle detected involving task: {name}")
            if name in visited:
                return

            in_stack.add(name)
            task = self._tasks.get(name)
            if task:
                for dep in task.dependencies:
                    dfs(dep)

            in_stack.remove(name)
            visited.add(name)
            order.append(name)

        # 🐛 BUG 1: Only starts DFS from tasks that have dependencies
        # Tasks with no dependencies but that ARE dependencies of others
        # may never be visited — and cycles in isolated subgraphs are missed
        for name, task in self._tasks.items():
            if task.dependencies:  # Should be: if name not in visited
                dfs(name)

        return order

    def calculate_effective_priority(self, name: str) -> int:
        """
        Calculate effective priority: task's own priority + sum of dependent priorities.
        Higher = more important.
        """
        visited: set[str] = set()
        return self._calc_priority(name, visited)

    def _calc_priority(self, name: str, visited: set[str]) -> int:
        task = self._tasks.get(name)
        if not task:
            return 0

        # 🐛 BUG 2: Doesn't add the task to visited BEFORE recursing
        # This means in a diamond dependency (A->B->D, A->C->D),
        # D's priority is counted MULTIPLE TIMES, inflating the result
        total = task.priority
        for dep in task.dependencies:
            if dep not in visited:
                total += self._calc_priority(dep, visited)

        visited.add(name)  # Should be BEFORE the loop, not after
        return total

    def get_parallel_groups(self) -> list[list[str]]:
        """
        Group tasks into parallel execution levels.
        Tasks in the same group can execute simultaneously (no inter-dependencies).
        """
        # Calculate depth for each task
        depths: dict[str, int] = {}

        def get_depth(name: str) -> int:
            if name in depths:
                return depths[name]

            task = self._tasks.get(name)
            if not task or not task.dependencies:
                depths[name] = 0
                return 0

            # 🐛 BUG 3: Uses max instead of max+1
            # This puts a task at the SAME level as its deepest dependency
            # instead of one level AFTER it
            max_dep_depth = max(get_depth(dep) for dep in task.dependencies)
            depths[name] = max_dep_depth  # Should be max_dep_depth + 1

            return depths[name]

        for name in self._tasks:
            get_depth(name)

        # Group by depth
        groups: dict[int, list[str]] = {}
        for name, depth in depths.items():
            groups.setdefault(depth, []).append(name)

        return [groups[d] for d in sorted(groups.keys())]

    def complete_task(self, name: str, result: Any = None) -> list[str]:
        """
        Mark a task as completed and return names of tasks that are now ready.
        """
        task = self._tasks.get(name)
        if not task:
            raise ValueError(f"Unknown task: {name}")

        task.status = TaskStatus.COMPLETED
        task.result = result

        # Find tasks that are now ready (all deps completed)
        newly_ready = []
        for t_name, t in self._tasks.items():
            if t.status != TaskStatus.PENDING:
                continue

            # 🐛 BUG 4: Checks if ANY dependency is completed instead of ALL
            # This means a task becomes "ready" as soon as ONE dep finishes,
            # not when ALL deps are done
            if any(
                self._tasks[dep].status == TaskStatus.COMPLETED
                for dep in t.dependencies
                if dep in self._tasks
            ):  # Should be `all(...)` not `any(...)`
                t.status = TaskStatus.READY
                newly_ready.append(t_name)

        return newly_ready
