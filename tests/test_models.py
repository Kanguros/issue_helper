import pytest

from issue_helper.models import AnalysisResult


@pytest.mark.parametrize(
    "data",
    [
        {
            "incident_id": "1",
            "agent_name": "a",
            "findings": [],
            "recommendations": [],
            "confidence": 1.0,
        },
    ],
)
def test_minimum_analysis_results(data):
    assert AnalysisResult(**data)
