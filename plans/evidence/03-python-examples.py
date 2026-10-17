"""Checks the package 03 guide examples and synthetic consumer outcomes."""

import asyncio
import io
from pathlib import Path
import re
import runpy
from types import SimpleNamespace
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
GUIDE = ROOT / "reference" / "python.md"
EXAMPLES = {}
for index, source in enumerate(re.findall(r"```python\n(.*?)\n```", GUIDE.read_text(), re.S)):
    exec(compile(source, f"{GUIDE}:example-{index + 1}", "exec"), EXAMPLES)


class PythonGuideExamples(unittest.TestCase):
    def test_reads_utf8_first_line(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.txt"
            path.write_text("café\nsecond\n", encoding="utf-8")
            self.assertEqual(EXAMPLES["read_first_line"](path), "café")

    def test_closes_stream_when_read_fails(self):
        class FailingReader(io.StringIO):
            def readline(self):
                raise OSError("synthetic read failure")

        stream = FailingReader("content")
        path = SimpleNamespace(open=lambda **kwargs: stream)
        with self.assertRaisesRegex(OSError, "synthetic read failure"):
            EXAMPLES["read_first_line"](path)
        self.assertTrue(stream.closed)

    def test_default_accumulators_are_independent(self):
        append = EXAMPLES["append_value"]
        first = append(1)
        second = append(2)
        self.assertEqual(first, [1])
        self.assertEqual(second, [2])
        self.assertIsNot(first, second)

    def test_explicit_empty_accumulator_is_preserved(self):
        values = []
        result = EXAMPLES["append_value"](3, values)
        self.assertIs(result, values)
        self.assertEqual(values, [3])

    def test_accepts_one_shot_iterator(self):
        self.assertEqual(EXAMPLES["total"](iter([1, 2, 3])), 6)
        self.assertEqual(EXAMPLES["total"](iter([])), 0)

    def test_existing_path_rejects_traversal_sibling_and_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "uploads"
            sibling = parent / "uploads-backup"
            root.mkdir()
            sibling.mkdir()
            (root / "inside.txt").write_text("inside")
            outside = sibling / "outside.txt"
            outside.write_text("outside")
            (root / "link.txt").symlink_to(outside)
            resolve = EXAMPLES["existing_child"]
            self.assertEqual(resolve(root, "inside.txt"), root / "inside.txt")
            for name in ["../uploads-backup/outside.txt", str(outside), "link.txt"]:
                with self.subTest(name=name), self.assertRaises(ValueError):
                    resolve(root, name)
            with self.assertRaises(FileNotFoundError):
                resolve(root, "missing.txt")

    def test_implicit_exception_context_is_retained(self):
        try:
            try:
                raise ValueError("original")
            except ValueError:
                raise RuntimeError("translated")
        except RuntimeError as error:
            self.assertIsInstance(error.__context__, ValueError)
            self.assertIsNone(error.__cause__)
            self.assertFalse(error.__suppress_context__)
        else:
            self.fail("The translated exception was not raised")

    def test_from_none_keeps_context_but_suppresses_display(self):
        try:
            try:
                raise ValueError("original")
            except ValueError:
                raise RuntimeError("translated") from None
        except RuntimeError as error:
            self.assertIsInstance(error.__context__, ValueError)
            self.assertTrue(error.__suppress_context__)
        else:
            self.fail("The translated exception was not raised")

    def test_fetch_all_generator_still_materialises_source(self):
        fetched = []

        def fetch_all():
            fetched.extend([1, 2, 3])
            return fetched

        def rows():
            for row in fetch_all():
                yield row

        iterator = rows()
        self.assertEqual(next(iterator), 1)
        self.assertEqual(fetched, [1, 2, 3])

    def test_consumer_append_requirement_detects_truncation(self):
        fixture = ROOT / "plans" / "evidence" / "fixtures" / "03-consumer"
        before = runpy.run_path(str(fixture / "writer-before.py"))["record_event"]
        after = runpy.run_path(str(fixture / "writer-after.py"))["record_event"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.txt"
            path.write_text("old\n", encoding="utf-8")
            before(path, "new")
            self.assertEqual(path.read_text(encoding="utf-8"), "old\nnew\n")
            path.write_text("old\n", encoding="utf-8")
            after(path, "new")
            self.assertEqual(path.read_text(encoding="utf-8"), "new\n")


class AsyncExamples(unittest.IsolatedAsyncioTestCase):
    async def test_worker_propagates_cancellation_and_cleans_up(self):
        started = asyncio.Event()
        cleaned = []
        task = asyncio.create_task(EXAMPLES["worker"](started, cleaned))
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(cleaned, ["released"])

    async def test_await_only_loop_can_be_cancelled(self):
        started = asyncio.Event()

        async def do_work():
            started.set()
            await asyncio.Event().wait()

        async def inherited_worker():
            while True:
                await do_work()

        task = asyncio.create_task(inherited_worker())
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task

    async def test_queue_sentinel_needs_completion_accounting(self):
        queue = asyncio.Queue()
        await queue.put(None)
        self.assertIsNone(await queue.get())
        joiner = asyncio.create_task(queue.join())
        await asyncio.sleep(0)
        self.assertFalse(joiner.done())
        queue.task_done()
        await asyncio.wait_for(joiner, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
