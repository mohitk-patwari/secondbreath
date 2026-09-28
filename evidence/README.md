# evidence/

Proof for the hackathon judges that the claims in the write-up actually
happened. Nothing here is generated for show; each file is a raw export or a
screenshot of a real run.

| What | File(s) | Proves |
|---|---|---|
| Agent-connection screenshots | `agent-connection/*.png` | The Bedrock-backed `/explain` agent was reachable from the deployed app and answered a real request. |
| CloudTrail export | `cloudtrail/*.json` | The deployed Lambdas made real `bedrock:InvokeModel` calls (Converse API) in our account, with timestamps, and nothing beyond least-privilege IAM was used. |
| MCP verification | `mcp/*` | The MCP tool connection was established and exercised; transcript or screenshot of the tool list and one successful call. |

The dataset audit itself (834 decay fits across three lecture halls) is not
here: it is reproducible from `analysis/audit_lecture_halls.py` and its
committed output is `analysis/audit.json`.

Redact account IDs, access keys and personal emails before committing
anything to this folder.
