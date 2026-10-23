#!/usr/bin/env python3
"""Compatibility command: synchronize the entire installable runtime, not just playbooks."""

import argparse
import sys

from runtime_bundle import ROOT, check_runtime, write_runtime
from lens_contract import projection_errors, sync_projections


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check every runtime resource without writing files")
    args = parser.parse_args()
    destination = ROOT / "skills/shared"
    if not args.check:
        sync_projections()
        write_runtime(destination)
    errors = projection_errors() + check_runtime(destination)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Complete runtime bundle is in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
