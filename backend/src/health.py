import json


def handler(event, context):
    # lastAuditRun stays null until T3's audit pipeline writes a timestamp somewhere we can read.
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"ok": True, "service": "secondbreath", "lastAuditRun": None}),
    }
