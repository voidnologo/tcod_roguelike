#!/usr/bin/env python
"""Test runner entry point for the tcod roguelike test suite.

This script provides a convenient way to run the test suite with various options.

Usage:
    # Run all tests
    python run_tests.py

    # Run with verbose output
    python run_tests.py -v

    # Run specific test module
    python run_tests.py test_entity

    # Run specific test class
    python run_tests.py test_entity.TestEntityBasics

    # Run specific test method
    python run_tests.py test_entity.TestEntityBasics.test_entity_has_position

    # Run with coverage (requires coverage package)
    coverage run run_tests.py
    coverage report

Examples:
    $ python run_tests.py
    .......................................................
    ----------------------------------------------------------------------
    Ran 57 tests in 0.234s
    OK

    $ python run_tests.py -v test_actions
    test_bump_attacks_not_moves_through_enemy (test_actions.TestBumpAction) ... ok
    test_bump_into_empty_space_moves (test_actions.TestBumpAction) ... ok
    ...
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))


def discover_tests(pattern: str = 'test_*.py') -> unittest.TestSuite:
    """Discover all tests in the tests directory.

    Args:
        pattern: Glob pattern for test files

    Returns:
        TestSuite containing all discovered tests
    """
    tests_dir = Path(__file__).parent / 'tests'
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(tests_dir),
        pattern=pattern,
        top_level_dir=str(Path(__file__).parent),
    )
    return suite


def run_specific_tests(test_spec: str) -> unittest.TestSuite:
    """Load specific tests by module, class, or method name.

    Args:
        test_spec: Test specification (e.g., 'test_entity',
                   'test_entity.TestEntityBasics',
                   'test_entity.TestEntityBasics.test_entity_has_position')

    Returns:
        TestSuite containing the specified tests
    """
    loader = unittest.TestLoader()

    # Add tests prefix if not present
    if not test_spec.startswith('tests.'):
        test_spec = f'tests.{test_spec}'

    try:
        suite = loader.loadTestsFromName(test_spec)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error loading tests: {e}")
        print(f"Make sure the test specification is correct: {test_spec}")
        sys.exit(1)

    return suite


def main() -> int:
    """Main entry point for the test runner.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Run the tcod roguelike test suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        'tests',
        nargs='?',
        help='Specific test module, class, or method to run',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=1,
        help='Increase verbosity (can be repeated)',
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Minimal output',
    )
    parser.add_argument(
        '-f', '--failfast',
        action='store_true',
        help='Stop on first failure',
    )
    parser.add_argument(
        '-b', '--buffer',
        action='store_true',
        help='Buffer stdout and stderr during tests',
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available tests without running them',
    )

    args = parser.parse_args()

    # Adjust verbosity
    verbosity = 0 if args.quiet else args.verbose

    # Load tests
    if args.tests:
        suite = run_specific_tests(args.tests)
    else:
        suite = discover_tests()

    # List tests if requested
    if args.list:
        print("Available tests:")
        print("=" * 60)
        for test_group in suite:
            for test_case in test_group:
                if hasattr(test_case, '__iter__'):
                    for test in test_case:
                        print(f"  {test}")
                else:
                    print(f"  {test_case}")
        return 0

    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=verbosity,
        failfast=args.failfast,
        buffer=args.buffer,
    )

    print(f"Running tests from: {Path(__file__).parent / 'tests'}")
    print("=" * 60)

    result = runner.run(suite)

    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
