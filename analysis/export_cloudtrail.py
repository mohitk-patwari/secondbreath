"""
Export CloudTrail evidence of every AWS API call made during the build.

Uses CloudTrail Event history (lookup-events): management events only, last
90 days, no trail needed. Filtered to the build principal. Writes:

    evidence/cloudtrail-raw.json       every matching event, unmodified
    evidence/cloudtrail-timeline.md    per-service counts + full UTC timeline

Usage
-----
    python analysis/export_cloudtrail.py [--since 2026-09-28T00:00:00Z]
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "evidence"

# The human/terminal user, and the scoped user the AWS MCP server signs as.
USERNAMES = ["MohitkPatwari@2005", "secondbreath-dev"]
# ap-south-1 holds the stack; us-east-1 is where global services (IAM, STS,
# billing alarms) record their events.
REGIONS = ["ap-south-1", "us-east-1"]


def lookup(region: str, since: str, username: str) -> list[dict]:
    # The CLI paginates for us; each event's CloudTrailEvent is a JSON string.
    cmd = ["aws", "cloudtrail", "lookup-events", "--region", region, "--output", "json",
           "--start-time", since,
           "--lookup-attributes", f"AttributeKey=Username,AttributeValue={username}"]
    raw = json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)
    return [json.loads(e["CloudTrailEvent"]) for e in raw.get("Events", [])]


def redact(ev: dict) -> dict:
    """Mask the caller's home IP and access key ID before this goes into a
    public repo. Neither proves anything the rest of the record does not."""
    if "sourceIPAddress" in ev and not ev["sourceIPAddress"].endswith("amazonaws.com"):
        ev["sourceIPAddress"] = "REDACTED"
    if "accessKeyId" in ev.get("userIdentity", {}):
        ev["userIdentity"]["accessKeyId"] = "REDACTED"
    return ev


def caller(ev: dict) -> str:
    """Who drove the call. The console and the coding agent share one IAM
    user, so userAgent is the only thing that separates them."""
    ua = ev.get("userAgent", "")
    if ev.get("sessionCredentialFromConsole") == "true" or "console" in ua or ua.startswith("Mozilla"):
        return "console"
    # The AWS MCP server calls AWS on the agent's behalf and stamps itself as
    # invokedBy, like a service would; it is the agent, not AWS, driving it.
    if ev.get("userIdentity", {}).get("invokedBy") == "aws-mcp.amazonaws.com":
        return "aws-mcp"
    # The MCP session itself (tools/call, session/destroy), sent by the local
    # proxy; its userAgent names the client, e.g. claude-code/2.1.284.
    if "mcp-proxy-for-aws" in ua:
        return "mcp-proxy"
    if ev.get("userIdentity", {}).get("invokedBy"):
        return "service:" + ev["userIdentity"]["invokedBy"].split(".")[0]
    if "sam-cli" in ua.lower():
        return "sam-cli"
    if "aws-cli" in ua:
        return "aws-cli"
    return ua.split("/")[0] or "unknown"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-09-28T00:00:00Z")
    args = ap.parse_args()

    events = []
    for region in REGIONS:
        for username in USERNAMES:
            events += lookup(region, args.since, username)
    # lookup-events is regional, but a global event can surface in both.
    events = [redact(e) for e in {e["eventID"]: e for e in events}.values()]
    events.sort(key=lambda e: e["eventTime"])

    OUT.mkdir(exist_ok=True)
    (OUT / "cloudtrail-raw.json").write_text(json.dumps(events, indent=1) + "\n")

    by_service = Counter(e["eventSource"].split(".")[0] for e in events)
    by_caller = Counter(caller(e) for e in events)
    errors = sum(1 for e in events if e.get("errorCode"))
    arns = sorted({e["userIdentity"].get("arn", "?") for e in events})
    exported = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines = [
        "# CloudTrail timeline",
        "",
        f"Exported {exported} by `analysis/export_cloudtrail.py` from CloudTrail Event history "
        f"({', '.join(REGIONS)}), filtered to `Username` in {', '.join(f'`{u}`' for u in USERNAMES)}, from {args.since}.",
        "",
        f"- Principal(s): {', '.join(f'`{a}`' for a in arns) or 'none'}",
        f"- Events: {len(events)} ({errors} returned an error)",
        f"- First: {events[0]['eventTime'] if events else '-'} · Last: {events[-1]['eventTime'] if events else '-'}",
        "- Raw events: `cloudtrail-raw.json` (the full CloudTrail record for each call; "
        "`sourceIPAddress` and `userIdentity.accessKeyId` masked as REDACTED, nothing else changed)",
        "",
        "Scope: management events only (Event history does not hold data events such as "
        "Lambda Invoke or S3 object reads). Calls made by the deployed Lambdas' own roles are "
        "excluded by the principal filter. The terminal agents and the human share the build user "
        "(`MohitkPatwari@2005`), so for its rows the **Caller** column (from userAgent) is the only split: `aws-cli` / `sam-cli` "
        "are terminal calls (agent sessions, or the human typing in the same terminal), "
        "`console` is the human in a browser, `aws-mcp` is the agent calling through the AWS MCP "
        "server (user `secondbreath-dev`, `invokedBy` and `userAgent` = `aws-mcp.amazonaws.com`), "
        "`mcp-proxy` is the MCP session itself as seen by the MCP service (`AwsMcpEvent`), "
        "and `service:*` is AWS acting for the user "
        "(e.g. CloudFormation creating resources).",
        "",
        "## Calls per service",
        "",
        "| Service | Calls |",
        "|---|---|",
        *(f"| {s} | {n} |" for s, n in by_service.most_common()),
        "",
        "## Calls per caller",
        "",
        "| Caller | Calls |",
        "|---|---|",
        *(f"| {c} | {n} |" for c, n in by_caller.most_common()),
        "",
        "## Timeline (UTC)",
        "",
        "| Time | Region | Service | Event | Caller | Error |",
        "|---|---|---|---|---|---|",
        *(
            f"| {e['eventTime']} | {e['awsRegion']} | {e['eventSource'].split('.')[0]} | "
            f"{e['eventName']} | {caller(e)} | {e.get('errorCode', '')} |"
            for e in events
        ),
    ]
    (OUT / "cloudtrail-timeline.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(events)} events; {dict(by_service)}; {dict(by_caller)}")


if __name__ == "__main__":
    main()
