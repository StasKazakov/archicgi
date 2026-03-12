import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from services.models import HealthReport
from services.monitor import check_endpoint
from services.logger import logger
from services.notifier import send_slack_alert
from services.load_endpoints import load_endpoints
from services.cla import parse_args
from services.database import init_db, save_report

load_dotenv()

async def main(args):
    """Main function for starting the health monitor"""
    endpoints = load_endpoints()
    tasks = [check_endpoint(ep) for ep in endpoints]
    results = await asyncio.gather(*tasks)

    total = len(results)
    failed = sum(1 for r in results if r.status == "failed")
    ok = total - failed

    report = HealthReport(
        checked_at=datetime.now(timezone.utc).isoformat(),
        summary={"total": total, "ok": ok, "failed": failed},
        results=list(results)
    )

    logger.info(f"Summary - total: {total}, ok: {ok}, failed: {failed}")

    os.makedirs("data", exist_ok=True)
    with open(os.path.join("data", "health_report.json"), "w") as f:
        f.write(report.model_dump_json(indent=2))
    logger.info("Report saved health_report.json")

    save_report(report)
    logger.info("Report saved history.db")

    if not args.quiet:
        await send_slack_alert(report)


if __name__ == "__main__":
    args = parse_args()
    init_db()

    if args.watch:

        logger.info("Health monitor started — watch mode (every 60 seconds)")

        async def watch_loop():
            try:
                while True:
                    await main(args)
                    logger.info("Next check in 60 seconds...")
                    await asyncio.sleep(60)
            except asyncio.CancelledError:
                logger.info("Health monitor stopped.")

        try:
            asyncio.run(watch_loop())
        except KeyboardInterrupt:
            pass
    else:
        asyncio.run(main(args))