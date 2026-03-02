# 🐛 Bugs — Intentionally Buggy Python Project

A test repository for validating the **RepoMind** autonomous DevOps agent.

This project contains Python modules with **intentional bugs** at 5 difficulty levels,
each with comprehensive test suites that expose the bugs.

## Bug Difficulty Levels

| Level | Module | Bugs | Description |
|-------|--------|------|-------------|
| 🟢 Easy | `src/calculator.py` | 2 | Reversed subtraction, missing zero guard |
| 🟡 Medium | `src/string_utils.py` | 2 | Off-by-one in truncate, case-sensitivity |
| 🔴 Hard | `src/algorithms.py` | 2 | Binary search infinite loop, merge sort error |
| 🟣 Very Hard | `src/cache.py` | 2 | LRU eviction reversed, access order not tracked |
| 💀 Extreme | `src/scheduler.py` | 4 | Topo sort, priority overflow, parallel groups, completion |

## Running Tests

```bash
# All tests (expect ~15 failures)
python -m pytest tests/ -v

# By difficulty level
python -m pytest tests/test_calculator.py -v     # Easy
python -m pytest tests/test_string_utils.py -v   # Medium
python -m pytest tests/test_algorithms.py -v     # Hard
python -m pytest tests/test_cache.py -v          # Very Hard
python -m pytest tests/test_scheduler.py -v      # Extreme
```
