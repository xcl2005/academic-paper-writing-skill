#!/usr/bin/env python3
"""Compatibility entrypoint for the comprehensive stage-gate regression suite."""
import unittest
import test_evidence_gates

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_evidence_gates.StageGateTests)
    raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
