import unittest

from main import Queue, QueueEmptyError


class TestQueue(unittest.TestCase):
    def test_queue_add_and_pop(self):
        queue = Queue[int]()
        queue.add(1)
        queue.add(2)

        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.pop(), 2)

    def test_empty_queue_pop(self):
        queue = Queue[int]()
        with self.assertRaises(QueueEmptyError):
            queue.pop()

    def test_sequence_add_and_pop(self):
        queue = Queue[str]()
        elements = ["apple", "banana", "cherry"]
        for elem in elements:
            queue.add(elem)

        for elem in elements:
            self.assertEqual(queue.pop(), elem)


if __name__ == "__main__":
    unittest.main()
