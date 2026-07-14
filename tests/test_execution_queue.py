"""Tests for nextnanopy.inputs.ExecutionQueue.

Regression tests for CODE_REVIEW.md finding 2.3 (run() busy-spun at 100% CPU while
simulations were running) plus basic contract tests — the class had no coverage before.

No nextnano executable is needed: FakeInputFile mimics InputFile.execute() by launching a
dummy subprocess (python -c "time.sleep(N)") and returning the same info dict that
nextnanopy.commands.execute() returns (the keys ExecutionQueue actually touches).
"""

import queue
import subprocess
import sys
import threading
import time
import unittest

from nextnanopy.inputs import ExecutionQueue


class FakeInputFile:
    """Stands in for nextnanopy.InputFile.

    execute() matches nextnanopy.commands.execute(): it launches a real subprocess,
    returns an info dict with the keys log_finished() uses, and blocks until the
    process finishes when __parallel__ is False, like commands.start_log() does.
    """

    def __init__(self, duration):
        self.duration = duration
        self.__parallel__ = False

    def execute(self, **_ignored):
        process = subprocess.Popen(
            [sys.executable, "-c", f"import time; time.sleep({self.duration})"],
        )
        tout = threading.Thread(target=lambda: None)
        terr = threading.Thread(target=lambda: None)
        tout.start()
        terr.start()
        if not self.__parallel__:
            process.wait()
        return {"process": process, "tout": tout, "terr": terr, "queue": queue.Queue()}


class TestExecutionQueue(unittest.TestCase):
    def run_queue(self, eq, timeout=30):
        eq.start()
        eq.join(timeout=timeout)
        self.assertFalse(eq.is_alive(), "ExecutionQueue did not terminate")

    def abort_queue(self, eq, timeout=30):
        # Drain waiting work and kill running processes so the test doesn't
        # have to sit out the full fake-simulation durations.
        while not eq.waiting_queue.empty():
            try:
                eq.waiting_queue.get_nowait()
            except queue.Empty:
                break
        for info, _input_file in list(eq.started):
            info["process"].terminate()
        eq.join(timeout=timeout)
        self.assertFalse(eq.is_alive(), "ExecutionQueue did not terminate")

    def test_no_busy_spin_while_parallel_simulations_run(self):
        # Regression test for 2.3: run() must not burn CPU while waiting for
        # simulations. The spin gave CPU ~= wall (ratio ~1.0); the fix gives ~0.
        # process_time() counts this process only, so the sleeping subprocesses
        # contribute nothing and the 0.5 threshold has a huge margin both ways.
        # Runs with the default poll_interval on purpose: it tests shipped behavior.
        eq = ExecutionQueue(limit_parallel=2)
        eq.add(FakeInputFile(0.5), FakeInputFile(0.5))

        cpu0, wall0 = time.process_time(), time.perf_counter()
        self.run_queue(eq)
        cpu, wall = time.process_time() - cpu0, time.perf_counter() - wall0

        self.assertLess(cpu, 0.5 * wall, f"busy spin: {cpu:.2f}s CPU over {wall:.2f}s wall")

    def test_all_free_slots_fill_in_one_pass(self):
        # add_execution() fills every free slot per call; with the poll sleep in
        # run(), one-slot-per-tick filling would leave later slots idle for
        # poll_interval each. All 3 must be running well before the first finishes
        # (3 s is a generous margin for slow CI; abort_queue kills the processes
        # once the assertion is decided, so the test never waits that long).
        eq = ExecutionQueue(limit_parallel=3)
        eq.add(FakeInputFile(3), FakeInputFile(3), FakeInputFile(3))
        eq.start()
        try:
            deadline = time.perf_counter() + 1.5
            while time.perf_counter() < deadline and len(eq.started) < 3:
                time.sleep(0.01)
            self.assertEqual(len(eq.started), 3)
        finally:
            self.abort_queue(eq)

    def test_all_files_finish_sequential(self):
        eq = ExecutionQueue(limit_parallel=1)
        eq.poll_interval = 0.02  # timing-irrelevant test, just make the ticks short
        eq.add(FakeInputFile(0.1), FakeInputFile(0.1))
        self.run_queue(eq)
        self.assertEqual(len(eq.finished), 2)
        self.assertEqual(eq.started, [])
        self.assertTrue(eq.waiting_queue.empty())

    def test_all_files_finish_parallel(self):
        eq = ExecutionQueue(limit_parallel=2)
        eq.poll_interval = 0.02
        eq.add(FakeInputFile(0.1), FakeInputFile(0.1), FakeInputFile(0.1))
        self.run_queue(eq)
        self.assertEqual(len(eq.finished), 3)
        self.assertEqual(eq.started, [])
        self.assertTrue(eq.waiting_queue.empty())

    def test_terminate_empty_false_accepts_late_work_and_stops(self):
        eq = ExecutionQueue(limit_parallel=2, terminate_empty=False)
        eq.poll_interval = 0.02
        eq.start()
        try:
            time.sleep(0.15)  # let it reach the idle loop with an empty queue
            self.assertTrue(eq.is_alive())
            eq.add(FakeInputFile(0.1))
            deadline = time.perf_counter() + 5
            while time.perf_counter() < deadline and not eq.finished:
                time.sleep(0.02)
            self.assertEqual(len(eq.finished), 1)
        finally:
            eq.stop()
            eq.join(timeout=30)
        self.assertFalse(eq.is_alive(), "ExecutionQueue did not terminate after stop()")


if __name__ == "__main__":
    unittest.main()
