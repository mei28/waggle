import pytest
from kagglesdk.competitions.types.submission_status import SubmissionStatus

from tools import check_submission


class _Sub:
    def __init__(self, ref, status, public_score="", error_description=""):
        self.ref = ref
        self.status = status
        self.public_score = public_score
        self.error_description = error_description
        self.date = None


class _Api:
    def __init__(self, pages):
        self.pages = list(pages)

    def competition_submissions(self, competition):
        return self.pages.pop(0)


def test_wait_until_complete_returns_the_completed_submission():
    api = _Api([[_Sub(1, SubmissionStatus.PENDING)], [_Sub(1, SubmissionStatus.COMPLETE, public_score="0.77")]])
    sub = check_submission.wait_until_complete(api, "titanic", ref=1, interval=0)
    assert sub.public_score == "0.77"


def test_wait_until_complete_raises_on_error_status():
    api = _Api([[_Sub(1, SubmissionStatus.ERROR, error_description="bad file")]])
    with pytest.raises(RuntimeError, match="bad file"):
        check_submission.wait_until_complete(api, "titanic", ref=1, interval=0)


def test_wait_until_complete_ignores_other_submissions():
    api = _Api(
        [
            [
                _Sub(2, SubmissionStatus.COMPLETE, public_score="0.1"),
                _Sub(1, SubmissionStatus.COMPLETE, public_score="0.9"),
            ]
        ]
    )
    assert check_submission.wait_until_complete(api, "titanic", ref=1, interval=0).public_score == "0.9"
