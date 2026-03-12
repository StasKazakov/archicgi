import os
import httpx
from datetime import datetime
from services.models import HealthReport
from services.logger import logger

async def send_slack_alert(report: HealthReport) -> None:
    """Function to send a Slack alert"""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.warning("SLACK_WEBHOOK_URL not set - printing to console instead")
        print(report.model_dump_json(indent=2))
        return
    
    # Make human format date
    checked_at = datetime.fromisoformat(report.checked_at).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    failed = [r for r in report.results if r.status == "failed"]

    if failed:
        blocks = [f"❌ *{r.name}*\n URL: {r.url}\n Error: {r.error}\n Response time: {r.response_time_ms}ms" for r in failed]
        text = f"🚨 *Health Check Alert*\nChecked at: {checked_at}\nFailed: {report.summary['failed']} of {report.summary['total']}\n\n" + "\n\n".join(blocks)
    else:
        text = f"✅ Health Check OK - all {report.summary['total']} endpoints are up ({checked_at})"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json={"text": text})
            logger.info(f"Slack alert sent - status: {response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Failed to send Slack alert - {str(e)}")