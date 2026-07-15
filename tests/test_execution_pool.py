"""Tests for nextnanopy.inputs.ExecutionPool.

ExecutionPool is the ThreadPoolExecutor-based candidate replacement for
ExecutionQueue (CODE_REVIEW.md 2.16). Same testing approach as
test_execution_queue.py: no nextnano executable is needed — FakeInputFile
launches a dummy subprocess and returns the info dict commands.execute() would.
FakeInputFile.execute() blocks until the process exits when __parallel__ is
False, which is exactly the blocking path ExecutionPool workers use.
"""

import time
import unittest

from nextnanopy.inputs import ExecutionPool

try:
    from tests.test_execution_queue import FakeInputFile
except ImportError:  # so `python tests/test_execution_pool.py` also works
    from test_execution_queue import FakeInputFile


class FailingInputFile:
    """execute() raises, like a bad executable path does in commands.execute()."""

    def execute(self, **_ignored):
        raise ValueError("simulated launch failure")


class TestExecutionPool(unittest.TestCase):
    def run_pool(self, pool, timeout=30):
        pool.start()
        pool.join(timeout=timeout)
        self.assertFalse(pool.is_alive(), "ExecutionPool did not finish in time")

    def test_all_files_finish_parallel(self):
        pool = ExecutionPool(parallel_limit=2)
        pool.add(FakeInputFile(0.1), FakeInputFile(0.1), FakeInputFile(0.1))
        self.run_pool(pool)
        self.assertEqual(len(pool.finished), 3)
        self.assertEqual(pool.errors, [])

    def test_all_files_finish_sequential(self):
        pool = ExecutionPool(parallel_limit=1)
        pool.add(FakeInputFile(0.1), FakeInputFile(0.1))
        self.run_pool(pool)
        self.assertEqual(len(pool.finished), 2)

    def test_runs_concurrently_not_sequentially(self):
        # 3 x 0.5 s with 3 workers: concurrent is ~0.5 s plus subprocess
        # startup, sequential would be >= 1.5 s plus 3 startups (~2 s+).
        pool = ExecutionPool(parallel_limit=3)
        pool.add(FakeInputFile(0.5), FakeInputFile(0.5), FakeInputFile(0.5))
        t0 = time.perf_counter()
        self.run_pool(pool)
        wall = time.perf_counter() - t0
        self.assertLess(wall, 1.4, f"3 x 0.5s took {wall:.2f}s -- ran sequentially?")

    def test_no_busy_wait(self):
        # Counterpart of the queue's 2.3 regression test, same thresholds:
        # waiting must not burn CPU. Workers block in process.wait(), so the
        # Python process should be essentially idle.
        pool = ExecutionPool(parallel_limit=2)
        pool.add(FakeInputFile(0.5), FakeInputFile(0.5))
        cpu0, wall0 = time.process_time(), time.perf_counter()
        self.run_pool(pool)
        cpu, wall = time.process_time() - cpu0, time.perf_counter() - wall0
        self.assertLess(cpu, 0.5 * wall, f"busy wait: {cpu:.2f}s CPU over {wall:.2f}s wall")

    def test_add_after_start(self):
        # ExecutionQueue needed terminate_empty=False plus stop() for this;
        # the pool just accepts work until stop().
        pool = ExecutionPool(parallel_limit=2)
        pool.add(FakeInputFile(0.1))
        pool.start()
        pool.add(FakeInputFile(0.1))
        pool.join(timeout=30)
        self.assertFalse(pool.is_alive())
        self.assertEqual(len(pool.finished), 2)

    def test_worker_exception_is_raised_by_join(self):
        # The ExecutionQueue failure mode this design removes: there, an
        # exception in execute() killed the scheduler thread and join()
        # returned as if the run had completed (silent queue death).
        pool = ExecutionPool(parallel_limit=2)
        pool.add(FakeInputFile(0.1), FailingInputFile(), FakeInputFile(0.1))
        pool.start()
        with self.assertRaises(ValueError):
            pool.join(timeout=30)
        self.assertEqual(len(pool.finished), 2)  # healthy files still ran
        self.assertEqual(len(pool.errors), 1)

    def test_join_before_start_raises(self):
        pool = ExecutionPool()
        with self.assertRaises(RuntimeError):
            pool.join()

    def test_stop_rejects_new_work(self):
        pool = ExecutionPool(parallel_limit=1)
        pool.add(FakeInputFile(0.05))
        pool.start()
        pool.stop()
        self.assertEqual(len(pool.finished), 1)
        with self.assertRaises(RuntimeError):
            pool.add(FakeInputFile(0.05))


if __name__ == "__main__":
    unittest.main()
