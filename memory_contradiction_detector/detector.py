"""Core Memory Contradiction Detector implementation."""
import time
from typing import Dict, List, Optional, Tuple, Any


class BeliefFact:
    def __init__(self, subject: str, attribute: str, value: Any, timestamp: float = 0.0):
        self.subject = subject.lower().strip()
        self.attribute = attribute.lower().strip()
        self.value = value
        self.timestamp = timestamp if timestamp > 0 else time.time()

    @property
    def key(self) -> str:
        return f"{self.subject}::{self.attribute}"


class ContradictionReport:
    def __init__(self, has_conflict: bool, existing_fact: Optional[BeliefFact], new_fact: BeliefFact, action: str):
        self.has_conflict = has_conflict
        self.existing_fact = existing_fact
        self.new_fact = new_fact
        self.action = action  # "SUPERSEDED", "IDENTICAL", "INSERTED"


class MemoryContradictionDetector:
    def __init__(self):
        self.beliefs: Dict[str, BeliefFact] = {}  # key -> BeliefFact

    def register_fact(self, subject: str, attribute: str, value: Any, timestamp: float = 0.0) -> ContradictionReport:
        new_fact = BeliefFact(subject, attribute, value, timestamp)
        k = new_fact.key

        if k not in self.beliefs:
            self.beliefs[k] = new_fact
            return ContradictionReport(False, None, new_fact, "INSERTED")

        existing = self.beliefs[k]
        if existing.value == new_fact.value:
            return ContradictionReport(False, existing, new_fact, "IDENTICAL")

        # Conflict detected! Values differ for the same subject & attribute.
        # Resolve by timestamp (newer wins)
        if new_fact.timestamp >= existing.timestamp:
            self.beliefs[k] = new_fact
            return ContradictionReport(True, existing, new_fact, "SUPERSEDED")
        else:
            return ContradictionReport(True, existing, new_fact, "REJECTED_STALE")

    def get_belief(self, subject: str, attribute: str) -> Optional[Any]:
        k = f"{subject.lower().strip()}::{attribute.lower().strip()}"
        fact = self.beliefs.get(k)
        return fact.value if fact else None
