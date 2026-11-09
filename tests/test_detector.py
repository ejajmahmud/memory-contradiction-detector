"""Unit tests for memory-contradiction-detector."""
import unittest
from memory_contradiction_detector.detector import MemoryContradictionDetector


class TestMemoryContradictionDetector(unittest.TestCase):
    def setUp(self):
        self.detector = MemoryContradictionDetector()

    def test_conflict_supersession(self):
        self.detector.register_fact("agent", "status", "idle", timestamp=10.0)
        rep = self.detector.register_fact("agent", "status", "busy", timestamp=20.0)
        self.assertTrue(rep.has_conflict)
        self.assertEqual(rep.action, "SUPERSEDED")
        self.assertEqual(self.detector.get_belief("agent", "status"), "busy")
