import httpx
import time

from services.models import Endpoint, CheckResult
from services.logger import logger


async def check_endpoint(ep: Endpoint) -> CheckResult:
    """Check an endpoint and return a CheckResult"""
    try:
        async with httpx.AsyncClient() as client:
            start = time.monotonic()
            response = await client.request(method=ep.method, url=ep.url, timeout=5.0)
            response_time = int((time.monotonic() - start) * 1000)

            if response_time > 2000:
                logger.warning(f"{ep.name} - SLOW | {response_time}ms exceeds 2000ms threshold")
                return CheckResult(
                    name=ep.name,
                    url=ep.url,
                    status="failed",
                    http_code=response.status_code,
                    response_time_ms=response_time,
                    error=f"Response too slow: {response_time}ms, threshold: 2000ms"
                )

            if response.status_code == ep.expected_status:
                logger.info(f"{ep.name} - OK | {response.status_code} | {response_time}ms")
                return CheckResult(
                    name=ep.name,
                    url=ep.url,
                    status="ok",
                    http_code=response.status_code,
                    response_time_ms=response_time,
                    error=None
                )
            else:
                logger.error(f"{ep.name} - FAILED | got {response.status_code}, expected {ep.expected_status} | {response_time}ms")
                return CheckResult(
                    name=ep.name,
                    url=ep.url,
                    status="failed",
                    http_code=response.status_code,
                    response_time_ms=response_time,
                    error=f"Expected status {ep.expected_status}, got {response.status_code}"
                )

    except httpx.TimeoutException:
        logger.error(f"{ep.name} - FAILED | Timeout after 5 seconds")
        return CheckResult(
            name=ep.name,
            url=ep.url,
            status="failed",
            http_code=None,
            response_time_ms=None,
            error="Timeout after 5 seconds"
        )

    except httpx.RequestError as e:
        logger.error(f"{ep.name} - FAILED | Network error: {str(e)}")
        return CheckResult(
            name=ep.name,
            url=ep.url,
            status="failed",
            http_code=None,
            response_time_ms=None,
            error=f"Network error: {str(e)}"
        )

    except Exception as e:
        logger.error(f"{ep.name} - FAILED | Unexpected error: {str(e)}")
        return CheckResult(
            name=ep.name,
            url=ep.url,
            status="failed",
            http_code=None,
            response_time_ms=None,
            error=f"Unexpected error: {str(e)}"
        )