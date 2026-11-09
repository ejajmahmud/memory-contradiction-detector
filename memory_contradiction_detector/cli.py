"""CLI for memory-contradiction-detector."""
import sys
import argparse
from .detector import MemoryContradictionDetector


def main():
    parser = argparse.ArgumentParser(description="Memory Contradiction Detector CLI")
    parser.add_argument("--demo", action="store_true", help="Run memory contradiction detection demo")
    args = parser.parse_args()

    if args.demo:
        detector = MemoryContradictionDetector()
        r1 = detector.register_fact("user", "favorite_language", "Python", timestamp=100.0)
        print(f"Fact 1 Registered: Action={r1.action} | Value={r1.new_fact.value}")

        # Register conflicting newer fact
        r2 = detector.register_fact("user", "favorite_language", "Rust", timestamp=200.0)
        print(f"Fact 2 Registered: Conflict={r2.has_conflict} | Action={r2.action} | Old='{r2.existing_fact.value}' -> New='{r2.new_fact.value}'")
        print("Active Belief in Memory:", detector.get_belief("user", "favorite_language"))
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
