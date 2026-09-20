"""Wait for the latest Kaggle submission to finish scoring and print the public LB score.

Usage: uv run python tools/check_submission.py --comp titanic [--interval 30]
"""

import os
import time
from dataclasses import dataclass
from typing import Any

import tyro
from kagglesdk.competitions.types.submission_status import SubmissionStatus


def latest(api: Any, comp: str) -> Any:
    subs = api.competition_submissions(comp)
    if not subs:
        raise RuntimeError(f"no submissions found for {comp}")
    return subs[0]


def wait_until_complete(api: Any, comp: str, ref: Any, interval: float) -> Any:
    """Poll until submission `ref` leaves PENDING. Raise when Kaggle reports an error."""
    while True:
        matches = [s for s in api.competition_submissions(comp) if s.ref == ref]
        if not matches:
            raise RuntimeError(f"submission {ref} disappeared from {comp}")
        sub = matches[0]
        if sub.status == SubmissionStatus.COMPLETE:
            return sub
        if sub.status == SubmissionStatus.ERROR:
            raise RuntimeError(f"submission {ref} failed: {sub.error_description}")
        time.sleep(interval)


@dataclass
class Args:
    comp: str = os.environ.get("COMP", "")
    interval: float = 30.0


def main(args: Args) -> None:
    from kaggle.api.kaggle_api_extended import KaggleApi

    if not args.comp:
        raise SystemExit("--comp is required (or set COMP in .env)")
    api = KaggleApi()
    api.authenticate()
    sub = latest(api, args.comp)
    print(f"waiting for submission {sub.ref} ({sub.status.name}) ...")
    done = wait_until_complete(api, args.comp, sub.ref, args.interval)
    print(f"public LB: {done.public_score}")


if __name__ == "__main__":
    main(tyro.cli(Args))
