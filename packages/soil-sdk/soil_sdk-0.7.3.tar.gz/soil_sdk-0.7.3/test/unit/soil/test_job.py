import unittest
from dataclasses import dataclass
from datetime import UTC, datetime
from json import dumps, loads
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlparse

from soil import job
from soil.job import _Job
from soil.types import Experiment


class TestJob(unittest.TestCase):
    @patch("soil.job.create_experiment")
    def test_job_create(self, mock_create_experiment: Mock):
        mock_create_experiment.return_value = Experiment(
            _id="my_experiment",
            status={"my_output": "DONE"},
            experiment_status="DONE",
            app_id="my_app",
            outputs={"my_datastructure": "my_output"},
            created_at=1640995200 * 1000,
        )
        my_job = job(data_object=Mock(sym_id="my_datastructure"), group="job_group1")
        self.assertEqual(
            my_job,
            _Job(  # pyright:ignore[reportAbstractUsage]
                experiment_id="my_experiment",
                result_id="my_output",
                _group="job_group1",
                _created_at=datetime.fromtimestamp(1640995200, tz=UTC).isoformat(),
            ),
        )


@dataclass
class MockHttpResponse:
    """Soil configuration class"""

    status_code: int
    text: str

    def json(self) -> dict:
        return loads(self.text)


# pylint: disable=unused-argument
def mock_http_patch(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    timeout: int,
) -> MockHttpResponse:
    assert url == "http://test_host.test/v2/states/mock_id/"
    assert json == {"name": "backtest", "state": {}}
    return MockHttpResponse(status_code=200, text=dumps({"hello": json}))


# pylint: disable=unused-argument
def mock_http_post(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    timeout: int,
) -> MockHttpResponse:
    url_parts = urlparse(url)
    assert url_parts.path == "/v2/states/"
    assert json == {"name": "backtest", "state": {}}
    return MockHttpResponse(status_code=200, text=dumps({}))


# pylint: disable=unused-argument
def mock_http_get(
    url: str, *, headers: dict[str, str] | None = None, timeout: int
) -> MockHttpResponse:
    url_parts = urlparse(url)
    query_params = parse_qs(url_parts.query)
    if url_parts.path == "/v2/states/" and query_params["name"][0] == "backtest":
        return MockHttpResponse(
            status_code=200,
            text=dumps([{"_id": "mock_id", "name": "backtest", "state": "mock_state"}]),
        )
    raise Exception("mock http case not found")
