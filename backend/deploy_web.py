"""Ship web/ to the live site: sync to S3, then invalidate CloudFront.

    python backend/deploy_web.py

Needs only the AWS CLI and credentials; bucket and distribution are read from
the secondbreath stack outputs, so nothing here changes when the stack does.
"""
import json
import subprocess
from pathlib import Path

STACK, REGION = "secondbreath", "ap-south-1"
WEB = Path(__file__).resolve().parents[1] / "web"


def aws(*args):
    out = subprocess.run(["aws", *args, "--region", REGION, "--output", "json"],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out) if out.strip() else None


if not (WEB / "index.html").is_file():
    raise SystemExit(f"{WEB / 'index.html'} not found; refusing to sync an empty site")

outputs = {o["OutputKey"]: o["OutputValue"] for o in
           aws("cloudformation", "describe-stacks", "--stack-name", STACK)["Stacks"][0]["Outputs"]}

# --delete keeps the bucket an exact mirror of web/. Five-minute max-age bounds
# how long a browser can hold an old page; the invalidation clears the edges now.
subprocess.run(["aws", "s3", "sync", str(WEB), f"s3://{outputs['WebBucketName']}",
                "--delete", "--exclude", ".*", "--cache-control", "public, max-age=300",
                "--region", REGION], check=True)
# No distribution while EnableCloudFront is false; the API-served page reads S3 live.
if "DistributionId" in outputs:
    inv = aws("cloudfront", "create-invalidation", "--distribution-id", outputs["DistributionId"],
              "--paths", "/*")["Invalidation"]
    print(f"invalidation {inv['Id']} {inv['Status']}")
print(f"live: {outputs['SiteUrl']}")
