from pydantic import BaseModel

class Endpoint(BaseModel):
    name: str
    url: str
    method: str
    expected_status: int

class CheckResult(BaseModel):
    name: str
    url: str
    status: str
    http_code: int | None
    response_time_ms: int | None
    error: str | None

class HealthReport(BaseModel):
    checked_at: str
    summary: dict
    results: list[CheckResult]