# CloudTrail timeline

Exported 2026-09-29T12:56:34+00:00 by `analysis/export_cloudtrail.py` from CloudTrail Event history (ap-south-1, us-east-1), filtered to `Username` in `MohitkPatwari@2005`, `secondbreath-dev`, from 2026-09-28T00:00:00Z.

- Principal(s): `arn:aws:iam::232351199908:user/MohitkPatwari@2005`, `arn:aws:iam::232351199908:user/secondbreath-dev`
- Events: 939 (103 returned an error)
- First: 2026-09-28T18:45:22Z · Last: 2026-09-29T12:53:44Z
- Raw events: `cloudtrail-raw.json` (the full CloudTrail record for each call; `sourceIPAddress` and `userIdentity.accessKeyId` masked as REDACTED, nothing else changed)

Scope: management events only (Event history does not hold data events such as Lambda Invoke or S3 object reads). Calls made by the deployed Lambdas' own roles are excluded by the principal filter. The terminal agents and the human share the build user (`MohitkPatwari@2005`), so for its rows the **Caller** column (from userAgent) is the only split: `aws-cli` / `sam-cli` are terminal calls (agent sessions, or the human typing in the same terminal), `console` is the human in a browser, `aws-mcp` is the agent calling through the AWS MCP server (user `secondbreath-dev`, `invokedBy` and `userAgent` = `aws-mcp.amazonaws.com`), `mcp-proxy` is the MCP session itself as seen by the MCP service (`AwsMcpEvent`), and `service:*` is AWS acting for the user (e.g. CloudFormation creating resources).

## Calls per service

| Service | Calls |
|---|---|
| s3 | 253 |
| lambda | 178 |
| cloudformation | 175 |
| iam | 144 |
| kms | 53 |
| logs | 52 |
| cloudtrail | 37 |
| apigateway | 10 |
| ssm | 8 |
| cloudfront | 7 |
| sts | 6 |
| bedrock | 5 |
| budgets | 3 |
| signin | 3 |
| aws-mcp | 3 |
| account | 2 |

## Calls per caller

| Caller | Calls |
|---|---|
| service:cloudformation | 617 |
| sam-cli | 149 |
| aws-cli | 96 |
| service:lambda | 53 |
| Boto3 | 16 |
| mcp-proxy | 3 |
| console | 2 |
| aws-mcp | 2 |
| service:apigateway | 1 |

## Timeline (UTC)

| Time | Region | Service | Event | Caller | Error |
|---|---|---|---|---|---|
| 2026-09-28T18:45:22Z | us-east-1 | sts | GetCallerIdentity | aws-cli |  |
| 2026-09-28T18:48:52Z | ap-south-1 | bedrock | ListFoundationModels | aws-cli |  |
| 2026-09-28T18:50:20Z | ap-south-1 | bedrock | ListInferenceProfiles | aws-cli |  |
| 2026-09-28T18:50:39Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 | ValidationException |
| 2026-09-28T18:50:40Z | ap-south-1 | cloudformation | DescribeChangeSet | Boto3 |  |
| 2026-09-28T18:50:40Z | ap-south-1 | cloudformation | CreateChangeSet | Boto3 |  |
| 2026-09-28T18:50:56Z | ap-south-1 | cloudformation | DescribeChangeSet | Boto3 |  |
| 2026-09-28T18:50:56Z | ap-south-1 | cloudformation | ExecuteChangeSet | Boto3 |  |
| 2026-09-28T18:50:56Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T18:51:01Z | ap-south-1 | s3 | CreateBucket | service:cloudformation |  |
| 2026-09-28T18:51:01Z | ap-south-1 | s3 | PutBucketEncryption | service:cloudformation |  |
| 2026-09-28T18:51:02Z | ap-south-1 | s3 | PutBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T18:51:02Z | ap-south-1 | s3 | PutBucketVersioning | service:cloudformation |  |
| 2026-09-28T18:51:12Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T18:51:14Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:14Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:14Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T18:51:14Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:14Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:14Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T18:51:15Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T18:51:16Z | ap-south-1 | s3 | PutBucketPolicy | service:cloudformation |  |
| 2026-09-28T18:51:16Z | ap-south-1 | s3 | GetBucketPolicy | service:cloudformation | NoSuchBucketPolicy |
| 2026-09-28T18:51:16Z | ap-south-1 | s3 | GetBucketPolicy | service:cloudformation |  |
| 2026-09-28T18:51:28Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T18:51:28Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T18:51:31Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli | ValidationException |
| 2026-09-28T18:51:33Z | ap-south-1 | cloudformation | CreateChangeSet | sam-cli |  |
| 2026-09-28T18:51:33Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T18:51:37Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation | ResourceNotFoundException |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T18:51:37Z | ap-south-1 | lambda | GetAccountSettings20160819 | service:cloudformation |  |
| 2026-09-28T18:51:37Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T18:51:37Z | us-east-1 | iam | GetAccountSummary | service:cloudformation |  |
| 2026-09-28T18:51:38Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:51:38Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T18:51:38Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T18:51:39Z | ap-south-1 | cloudformation | ExecuteChangeSet | sam-cli |  |
| 2026-09-28T18:51:41Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T18:51:41Z | us-east-1 | iam | AttachRolePolicy | service:cloudformation |  |
| 2026-09-28T18:51:41Z | us-east-1 | iam | CreateRole | service:cloudformation |  |
| 2026-09-28T18:51:42Z | ap-south-1 | logs | CreateLogGroup | service:cloudformation |  |
| 2026-09-28T18:51:43Z | ap-south-1 | logs | PutRetentionPolicy | service:cloudformation |  |
| 2026-09-28T18:51:44Z | ap-south-1 | logs | DescribeResourcePolicies | service:cloudformation |  |
| 2026-09-28T18:51:44Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:51:44Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T18:51:44Z | ap-south-1 | logs | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T18:51:44Z | ap-south-1 | logs | DescribeIndexPolicies | service:cloudformation |  |
| 2026-09-28T18:51:49Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:51:54Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:51:57Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T18:51:57Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T18:51:58Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T18:51:58Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T18:51:58Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T18:51:58Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T18:51:59Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:51:59Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation | ResourceNotFoundException |
| 2026-09-28T18:52:00Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T18:52:00Z | ap-south-1 | lambda | CreateFunction20150331 | service:cloudformation |  |
| 2026-09-28T18:52:01Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T18:52:03Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T18:52:04Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T18:52:04Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:52:04Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T18:52:04Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T18:52:04Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T18:52:04Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T18:52:09Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:52:14Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:52:15Z | ap-south-1 | bedrock | ListInferenceProfiles | aws-cli |  |
| 2026-09-28T18:52:19Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:52:25Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:52:30Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:52:32Z | us-east-1 | iam | CreateServiceLinkedRole | service:apigateway | InvalidInputException |
| 2026-09-28T18:52:33Z | ap-south-1 | apigateway | GetApi | service:cloudformation |  |
| 2026-09-28T18:52:33Z | ap-south-1 | apigateway | ImportApi | service:cloudformation |  |
| 2026-09-28T18:52:34Z | ap-south-1 | lambda | AddPermission20150331v2 | service:cloudformation |  |
| 2026-09-28T18:52:35Z | ap-south-1 | apigateway | CreateStage | service:cloudformation |  |
| 2026-09-28T18:52:35Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:52:35Z | ap-south-1 | apigateway | GetStage | service:cloudformation |  |
| 2026-09-28T18:52:35Z | ap-south-1 | lambda | GetPolicy20150331v2 | service:cloudformation |  |
| 2026-09-28T18:52:40Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T18:52:40Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T18:52:40Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T18:52:53Z | ap-south-1 | logs | DescribeLogGroups | aws-cli | InvalidParameterException |
| 2026-09-28T18:53:01Z | ap-south-1 | logs | DescribeLogGroups | aws-cli |  |
| 2026-09-28T18:56:10Z | ap-south-1 | bedrock | Converse | aws-cli | ValidationException |
| 2026-09-28T18:57:08Z | ap-south-1 | bedrock | Converse | aws-cli | ValidationException |
| 2026-09-28T19:26:17Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T19:26:20Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:26:20Z | ap-south-1 | cloudformation | GetTemplateSummary | sam-cli |  |
| 2026-09-28T19:26:21Z | ap-south-1 | cloudformation | CreateChangeSet | sam-cli |  |
| 2026-09-28T19:26:21Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:26:25Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation | ResourceNotFoundException |
| 2026-09-28T19:26:25Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:26:25Z | ap-south-1 | lambda | GetAccountSettings20160819 | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:26:25Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation | ResourceNotFoundException |
| 2026-09-28T19:26:25Z | us-east-1 | iam | GetAccountSummary | service:cloudformation |  |
| 2026-09-28T19:26:25Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:26:26Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:26:26Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:26:26Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:26Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:31Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:26:31Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:26:31Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:26:32Z | ap-south-1 | cloudformation | ExecuteChangeSet | sam-cli |  |
| 2026-09-28T19:26:34Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:26:34Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:26:34Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:34Z | us-east-1 | iam | CreateRole | service:cloudformation |  |
| 2026-09-28T19:26:34Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:34Z | us-east-1 | iam | AttachRolePolicy | service:cloudformation |  |
| 2026-09-28T19:26:34Z | us-east-1 | iam | CreateRole | service:cloudformation |  |
| 2026-09-28T19:26:34Z | us-east-1 | iam | AttachRolePolicy | service:cloudformation |  |
| 2026-09-28T19:26:34Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:26:35Z | ap-south-1 | logs | CreateLogGroup | service:cloudformation |  |
| 2026-09-28T19:26:35Z | ap-south-1 | logs | CreateLogGroup | service:cloudformation |  |
| 2026-09-28T19:26:35Z | us-east-1 | iam | PutRolePolicy | service:cloudformation |  |
| 2026-09-28T19:26:36Z | ap-south-1 | logs | PutRetentionPolicy | service:cloudformation |  |
| 2026-09-28T19:26:36Z | ap-south-1 | logs | PutRetentionPolicy | service:cloudformation |  |
| 2026-09-28T19:26:37Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:26:38Z | ap-south-1 | logs | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:26:38Z | ap-south-1 | logs | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:26:38Z | ap-south-1 | logs | DescribeResourcePolicies | service:cloudformation |  |
| 2026-09-28T19:26:38Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:26:38Z | ap-south-1 | logs | DescribeIndexPolicies | service:cloudformation |  |
| 2026-09-28T19:26:38Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:26:38Z | ap-south-1 | logs | DescribeIndexPolicies | service:cloudformation |  |
| 2026-09-28T19:26:38Z | ap-south-1 | logs | DescribeResourcePolicies | service:cloudformation |  |
| 2026-09-28T19:26:42Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:26:47Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:26:50Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:26:50Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:26:51Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:51Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:26:51Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:51Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:51Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:52Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:26:52Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation | ResourceNotFoundException |
| 2026-09-28T19:26:52Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:52Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:26:52Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:52Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:26:52Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:26:52Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:52Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:53Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:26:53Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:26:53Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:26:53Z | ap-south-1 | lambda | CreateFunction20150331 | service:cloudformation |  |
| 2026-09-28T19:26:53Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:53Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:53Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:26:53Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:53Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:26:53Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:53Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:53Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:26:54Z | ap-south-1 | lambda | UpdateFunctionConfiguration20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:54Z | ap-south-1 | kms | Encrypt | service:lambda |  |
| 2026-09-28T19:26:54Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:26:54Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:54Z | ap-south-1 | kms | DescribeKey | service:lambda |  |
| 2026-09-28T19:26:54Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:26:54Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation | ResourceNotFoundException |
| 2026-09-28T19:26:54Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:55Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:55Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:55Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:26:55Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:26:55Z | ap-south-1 | lambda | CreateFunction20150331 | service:cloudformation |  |
| 2026-09-28T19:26:55Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:55Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:26:55Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:26:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:57Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:26:57Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:26:57Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:57Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:57Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:26:57Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:57Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:26:58Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:26:58Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:26:58Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:26:59Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:26:59Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:02Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:02Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:02Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:27:02Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:27:02Z | ap-south-1 | lambda | UpdateFunctionCode20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:02Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:27:03Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:27:07Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:27:07Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:27:07Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:27:07Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:27:07Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:27:07Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:07Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:08Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:27:09Z | ap-south-1 | apigateway | GetApi | service:cloudformation |  |
| 2026-09-28T19:27:12Z | ap-south-1 | apigateway | ReimportApi | service:cloudformation |  |
| 2026-09-28T19:27:12Z | ap-south-1 | apigateway | GetApi | service:cloudformation |  |
| 2026-09-28T19:27:13Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:27:13Z | ap-south-1 | lambda | AddPermission20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:13Z | ap-south-1 | lambda | AddPermission20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:14Z | ap-south-1 | lambda | GetPolicy20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:14Z | ap-south-1 | lambda | GetPolicy20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:15Z | ap-south-1 | lambda | AddPermission20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:16Z | ap-south-1 | lambda | GetPolicy20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:18Z | ap-south-1 | lambda | RemovePermission20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:19Z | ap-south-1 | lambda | GetPolicy20150331v2 | service:cloudformation |  |
| 2026-09-28T19:27:19Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:27:24Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:27:24Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:27:24Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:28:18Z | ap-south-1 | ssm | PutParameter | aws-cli |  |
| 2026-09-28T19:28:21Z | ap-south-1 | ssm | PutParameter | aws-cli |  |
| 2026-09-28T19:28:23Z | ap-south-1 | ssm | DeleteParameter | aws-cli |  |
| 2026-09-28T19:28:25Z | ap-south-1 | logs | DescribeLogGroups | aws-cli |  |
| 2026-09-28T19:28:28Z | ap-south-1 | lambda | GetFunctionConfiguration20150331v2 | aws-cli |  |
| 2026-09-28T19:28:30Z | us-east-1 | iam | ListAttachedRolePolicies | aws-cli |  |
| 2026-09-28T19:28:32Z | us-east-1 | iam | ListRolePolicies | aws-cli |  |
| 2026-09-28T19:28:35Z | ap-south-1 | lambda | GetFunctionConfiguration20150331v2 | aws-cli |  |
| 2026-09-28T19:28:37Z | us-east-1 | iam | ListAttachedRolePolicies | aws-cli |  |
| 2026-09-28T19:28:39Z | us-east-1 | iam | ListRolePolicies | aws-cli |  |
| 2026-09-28T19:41:32Z | ap-south-1 | sts | GetCallerIdentity | aws-cli |  |
| 2026-09-28T19:42:24Z | us-east-1 | sts | GetCallerIdentity | aws-cli |  |
| 2026-09-28T19:42:46Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T19:42:48Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:42:48Z | ap-south-1 | cloudformation | GetTemplateSummary | sam-cli |  |
| 2026-09-28T19:42:49Z | ap-south-1 | cloudformation | CreateChangeSet | sam-cli |  |
| 2026-09-28T19:42:50Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:42:55Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:43:00Z | ap-south-1 | cloudformation | ExecuteChangeSet | sam-cli |  |
| 2026-09-28T19:43:00Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:43:00Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:00Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:43:03Z | ap-south-1 | ssm | PutParameter | aws-cli |  |
| 2026-09-28T19:43:03Z | us-east-1 | cloudfront | GetOriginAccessControl | service:cloudformation |  |
| 2026-09-28T19:43:03Z | us-east-1 | cloudfront | CreateOriginAccessControl | service:cloudformation |  |
| 2026-09-28T19:43:06Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:07Z | ap-south-1 | s3 | PutBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:43:07Z | ap-south-1 | s3 | CreateBucket | service:cloudformation |  |
| 2026-09-28T19:43:11Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:16Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | ssm | GetParameter | aws-cli |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:43:20Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:43:21Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:43:21Z | us-east-1 | cloudfront | GetOriginAccessControl | service:cloudformation |  |
| 2026-09-28T19:43:22Z | us-east-1 | cloudfront | CreateDistributionWithTags | service:cloudformation | AccessDenied |
| 2026-09-28T19:43:26Z | ap-south-1 | cloudformation | DescribeStacks | aws-cli |  |
| 2026-09-28T19:43:26Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:28Z | ap-south-1 | logs | FilterLogEvents | aws-cli | InvalidParameterException |
| 2026-09-28T19:43:30Z | ap-south-1 | logs | DescribeLogGroups | aws-cli | InvalidParameterException |
| 2026-09-28T19:43:31Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:37Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:42Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:47Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:52Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:58Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:03Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:05Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:06Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:06Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:06Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:06Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:06Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:06Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:08Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:09Z | ap-south-1 | cloudformation | DescribeStackEvents | aws-cli |  |
| 2026-09-28T19:44:09Z | us-east-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:13Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:18Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:24Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:29Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:29Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:29Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:29Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:29Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:29Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:29Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:29Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:32Z | us-east-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-28T19:44:34Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:39Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:45Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:50Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:44:56Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:01Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:06Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:11Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:16Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:22Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:27Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:32Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:33Z | ap-south-1 | cloudformation | DescribeStacks | aws-cli |  |
| 2026-09-28T19:45:37Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:41Z | ap-south-1 | s3 | DeleteBucket | service:cloudformation |  |
| 2026-09-28T19:45:41Z | us-east-1 | cloudfront | GetOriginAccessControl | service:cloudformation |  |
| 2026-09-28T19:45:41Z | us-east-1 | cloudfront | DeleteOriginAccessControl | service:cloudformation |  |
| 2026-09-28T19:45:42Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:45:42Z | us-east-1 | cloudfront | GetOriginAccessControl | service:cloudformation | NoSuchOriginAccessControl |
| 2026-09-28T19:45:43Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:45:44Z | ap-south-1 | cloudformation | DescribeStacks | aws-cli |  |
| 2026-09-28T19:45:46Z | ap-south-1 | cloudformation | DescribeStacks | aws-cli |  |
| 2026-09-28T19:45:58Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T19:46:01Z | ap-south-1 | cloudformation | GetTemplateSummary | sam-cli |  |
| 2026-09-28T19:46:01Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:46:01Z | ap-south-1 | ssm | PutParameter | aws-cli |  |
| 2026-09-28T19:46:02Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:46:02Z | ap-south-1 | cloudformation | CreateChangeSet | sam-cli |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:06Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:07Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:46:07Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | lambda | GetAccountSettings20160819 | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation | ResourceNotFoundException |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:46:08Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:46:08Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:46:08Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:08Z | us-east-1 | iam | GetAccountSummary | service:cloudformation |  |
| 2026-09-28T19:46:08Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:08Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:09Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:46:09Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:46:09Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:46:09Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:46:09Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:46:09Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:46:09Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:09Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:09Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:09Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:09Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:46:09Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:09Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:12Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:46:13Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:13Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:46:13Z | ap-south-1 | cloudformation | ExecuteChangeSet | sam-cli |  |
| 2026-09-28T19:46:15Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:46:15Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:16Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | UpdateFunctionCode20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | UpdateFunctionCode20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:17Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | UpdateFunctionCode20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | logs | CreateLogGroup | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:17Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:46:18Z | ap-south-1 | logs | PutRetentionPolicy | service:cloudformation |  |
| 2026-09-28T19:46:18Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:18Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:18Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:18Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:18Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | s3 | CreateBucket | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | s3 | PutBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:19Z | ap-south-1 | logs | DescribeResourcePolicies | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | logs | DescribeIndexPolicies | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | logs | DescribeLogGroups | service:cloudformation |  |
| 2026-09-28T19:46:19Z | ap-south-1 | logs | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:46:23Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:28Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:46:30Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:46:31Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:46:32Z | us-east-1 | iam | PutRolePolicy | service:cloudformation |  |
| 2026-09-28T19:46:32Z | us-east-1 | iam | CreateRole | service:cloudformation |  |
| 2026-09-28T19:46:32Z | us-east-1 | iam | AttachRolePolicy | service:cloudformation |  |
| 2026-09-28T19:46:34Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:39Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:44Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:44Z | ap-south-1 | ssm | PutParameter | aws-cli |  |
| 2026-09-28T19:46:49Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:50Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:50Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:46:51Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:46:51Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:46:51Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:51Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:51Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:51Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:46:52Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation | ResourceNotFoundException |
| 2026-09-28T19:46:53Z | ap-south-1 | kms | Encrypt | service:lambda |  |
| 2026-09-28T19:46:53Z | ap-south-1 | lambda | CreateFunction20150331 | service:cloudformation |  |
| 2026-09-28T19:46:53Z | ap-south-1 | kms | DescribeKey | service:lambda |  |
| 2026-09-28T19:46:53Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:54Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:54Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:46:54Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:55Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:46:55Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:46:55Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:55Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:46:55Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:55Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:46:55Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:46:59Z | ap-south-1 | apigateway | GetApi | service:cloudformation |  |
| 2026-09-28T19:47:00Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:47:01Z | ap-south-1 | apigateway | ReimportApi | service:cloudformation |  |
| 2026-09-28T19:47:02Z | ap-south-1 | apigateway | GetApi | service:cloudformation |  |
| 2026-09-28T19:47:03Z | ap-south-1 | lambda | AddPermission20150331v2 | service:cloudformation |  |
| 2026-09-28T19:47:03Z | ap-south-1 | lambda | GetPolicy20150331v2 | service:cloudformation |  |
| 2026-09-28T19:47:05Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:47:05Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:47:05Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:47:11Z | ap-south-1 | ssm | PutParameter | aws-cli |  |
| 2026-09-28T19:47:16Z | ap-south-1 | cloudformation | DescribeStacks | aws-cli |  |
| 2026-09-28T19:47:37Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | aws-cli |  |
| 2026-09-28T19:47:55Z | ap-south-1 | cloudformation | DescribeStacks | aws-cli |  |
| 2026-09-28T19:47:56Z | ap-south-1 | logs | DescribeLogGroups | aws-cli |  |
| 2026-09-28T19:47:58Z | ap-south-1 | logs | DescribeLogGroups | aws-cli |  |
| 2026-09-28T19:48:00Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:00Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:01Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:01Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:02Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:02Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:04Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:05Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:05Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:48:38Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T19:48:40Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:48:40Z | ap-south-1 | cloudformation | GetTemplateSummary | sam-cli |  |
| 2026-09-28T19:48:41Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:48:41Z | ap-south-1 | cloudformation | CreateChangeSet | sam-cli |  |
| 2026-09-28T19:48:46Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:48:47Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:48:47Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:48:47Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:47Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:47Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:48:47Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:47Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:48:47Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:47Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:48:48Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:48:48Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:48Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:48Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:48Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:48:48Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:51Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:48:52Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:48:52Z | ap-south-1 | cloudformation | ExecuteChangeSet | sam-cli |  |
| 2026-09-28T19:48:52Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:48:54Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:48:54Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:48:54Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:48:54Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:54Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:54Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:55Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:55Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:55Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:55Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:48:55Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:55Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:48:55Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:48:55Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | UpdateFunctionCode20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | UpdateFunctionCode20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:56Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:56Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:57Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:57Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:57Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:57Z | ap-south-1 | lambda | UpdateFunctionConfiguration20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:57Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:57Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:57Z | ap-south-1 | lambda | UpdateFunctionConfiguration20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:57Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:57Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:57Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:57Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:48:57Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:58Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:58Z | ap-south-1 | lambda | UpdateFunctionCode20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:58Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:48:58Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:48:58Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:58Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:58Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:58Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:58Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:58Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:58Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:48:59Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:59Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:48:59Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:59Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:48:59Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:00Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:00Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:49:00Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:00Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:00Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:00Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:49:00Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:00Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:49:00Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:01Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:01Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:01Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:01Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:02Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:02Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:03Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:03Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:49:03Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:49:03Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:49:03Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:03Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:49:04Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:04Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:04Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:04Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:04Z | ap-south-1 | lambda | UpdateFunctionCode20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:04Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:05Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:05Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:06Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:06Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:08Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:49:11Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:11Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:11Z | ap-south-1 | lambda | GetFunctionCodeSigningConfig | service:cloudformation |  |
| 2026-09-28T19:49:11Z | ap-south-1 | lambda | GetRuntimeManagementConfig | service:cloudformation |  |
| 2026-09-28T19:49:11Z | ap-south-1 | lambda | GetFunction20150331v2 | service:cloudformation |  |
| 2026-09-28T19:49:11Z | ap-south-1 | kms | Decrypt | service:lambda |  |
| 2026-09-28T19:49:11Z | ap-south-1 | lambda | GetFunctionRecursionConfig | service:cloudformation |  |
| 2026-09-28T19:49:13Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:49:19Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:49:24Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:49:29Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:49:34Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:49:40Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:49:40Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:49:40Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:50:00Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:50:00Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:50:02Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:50:02Z | ap-south-1 | logs | FilterLogEvents | aws-cli |  |
| 2026-09-28T19:53:29Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T19:53:32Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:53:33Z | ap-south-1 | cloudformation | GetTemplateSummary | sam-cli |  |
| 2026-09-28T19:53:34Z | ap-south-1 | cloudformation | CreateChangeSet | sam-cli |  |
| 2026-09-28T19:53:35Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:53:39Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:53:40Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:53:45Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:53:46Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:53:46Z | ap-south-1 | cloudformation | ExecuteChangeSet | sam-cli |  |
| 2026-09-28T19:53:46Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:53:50Z | us-east-1 | budgets | CreateBudget | service:cloudformation |  |
| 2026-09-28T19:53:51Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:53:57Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:53:57Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:53:57Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:54:14Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T19:54:17Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:54:18Z | ap-south-1 | cloudformation | GetTemplateSummary | sam-cli |  |
| 2026-09-28T19:54:19Z | ap-south-1 | cloudformation | CreateChangeSet | sam-cli |  |
| 2026-09-28T19:54:19Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:54:25Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:54:27Z | us-east-1 | budgets | DescribeNotificationsForBudget | aws-cli |  |
| 2026-09-28T19:54:30Z | us-east-1 | budgets | DescribeSubscribersForNotification | aws-cli |  |
| 2026-09-28T19:54:59Z | ap-south-1 | cloudformation | DescribeStacks | Boto3 |  |
| 2026-09-28T19:55:03Z | ap-south-1 | cloudformation | GetTemplateSummary | sam-cli |  |
| 2026-09-28T19:55:03Z | ap-south-1 | cloudformation | DescribeStacks | sam-cli |  |
| 2026-09-28T19:55:05Z | ap-south-1 | cloudformation | CreateChangeSet | sam-cli |  |
| 2026-09-28T19:55:06Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:55:10Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:55:10Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:11Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:55:11Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:55:11Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:11Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketMetadataTableConfiguration | service:cloudformation | V1APIsNotAllowed |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketEncryption | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketLifecycle | service:cloudformation | NoSuchLifecycleConfiguration |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketWebsite | service:cloudformation | NoSuchWebsiteConfiguration |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketPublicAccessBlock | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketOwnershipControls | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketIntelligentTieringConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | ListTagsForResource | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketObjectLockConfiguration | service:cloudformation | ObjectLockConfigurationNotFoundError |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketAnalyticsConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketAbac | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketReplication | service:cloudformation | ReplicationConfigurationNotFoundError |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketMetadataConfiguration | service:cloudformation | MetadataConfigurationNotFound |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketLogging | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketNotification | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketInventoryConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketCors | service:cloudformation | NoSuchCORSConfiguration |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetAccelerateConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketMetricsConfiguration | service:cloudformation |  |
| 2026-09-28T19:55:13Z | ap-south-1 | s3 | GetBucketVersioning | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | GetRolePolicy | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | ListAttachedRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | GetRole | service:cloudformation |  |
| 2026-09-28T19:55:13Z | us-east-1 | iam | ListRolePolicies | service:cloudformation |  |
| 2026-09-28T19:55:16Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:55:16Z | ap-south-1 | cloudformation | DescribeChangeSet | sam-cli |  |
| 2026-09-28T19:55:26Z | ap-south-1 | cloudformation | DescribeChangeSet | aws-cli |  |
| 2026-09-28T19:55:28Z | ap-south-1 | cloudformation | DeleteChangeSet | aws-cli |  |
| 2026-09-28T20:20:57Z | us-east-1 | account | ListRegions | aws-cli |  |
| 2026-09-28T20:20:57Z | us-east-1 | account | ListRegions | aws-cli |  |
| 2026-09-29T12:43:54Z | ap-south-1 | signin | ConsoleLogin | console |  |
| 2026-09-29T12:43:54Z | ap-south-1 | signin | AuthorizeOAuth2Access | console |  |
| 2026-09-29T12:43:55Z | ap-south-1 | signin | CreateOAuth2Token | aws-cli |  |
| 2026-09-29T12:44:16Z | ap-south-1 | sts | GetCallerIdentity | aws-cli |  |
| 2026-09-29T12:52:16Z | ap-south-1 | sts | GetCallerIdentity | aws-cli |  |
| 2026-09-29T12:52:46Z | ap-south-1 | sts | GetCallerIdentity | aws-mcp |  |
| 2026-09-29T12:52:47Z | ap-south-1 | cloudformation | DescribeStacks | aws-mcp |  |
| 2026-09-29T12:52:47Z | us-east-1 | aws-mcp | CallReadWriteTool | mcp-proxy |  |
| 2026-09-29T12:53:05Z | us-east-1 | aws-mcp | DestroySession | mcp-proxy |  |
| 2026-09-29T12:53:17Z | us-east-1 | aws-mcp | DestroySession | mcp-proxy |  |
| 2026-09-29T12:53:34Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:34Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:34Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:34Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:34Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:34Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:34Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:35Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:35Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:35Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:35Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:35Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:35Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:35Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:36Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:37Z | ap-south-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:40Z | us-east-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:40Z | us-east-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:41Z | us-east-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:42Z | us-east-1 | cloudtrail | LookupEvents | aws-cli |  |
| 2026-09-29T12:53:44Z | us-east-1 | cloudtrail | LookupEvents | aws-cli |  |
