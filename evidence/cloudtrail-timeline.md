# CloudTrail timeline

Exported 2026-09-28T19:44:33+00:00 by `analysis/export_cloudtrail.py` from CloudTrail Event history (ap-south-1, us-east-1), filtered to `Username = MohitkPatwari@2005`, from 2026-09-28T00:00:00Z.

- Principal(s): `arn:aws:iam::232351199908:user/MohitkPatwari@2005`
- Events: 349 (49 returned an error)
- First: 2026-09-28T18:45:22Z · Last: 2026-09-28T19:43:28Z
- Raw events: `cloudtrail-raw.json` (the full CloudTrail record for each call; `sourceIPAddress` and `userIdentity.accessKeyId` masked as REDACTED, nothing else changed)

Scope: management events only (Event history does not hold data events such as Lambda Invoke or S3 object reads). Calls made by the deployed Lambdas' own roles are excluded by the principal filter. The coding agent and the human share this IAM user, so the **Caller** column (from userAgent) is the only split: `aws-cli` / `sam-cli` are terminal calls (agent sessions, or the human typing in the same terminal), `console` is the human in a browser, and `service:*` is AWS acting for the user (e.g. CloudFormation creating resources).

## Calls per service

| Service | Calls |
|---|---|
| s3 | 109 |
| cloudformation | 68 |
| lambda | 66 |
| iam | 46 |
| logs | 28 |
| kms | 13 |
| apigateway | 7 |
| bedrock | 5 |
| ssm | 5 |
| sts | 2 |

## Calls per caller

| Caller | Calls |
|---|---|
| service:cloudformation | 245 |
| sam-cli | 56 |
| aws-cli | 23 |
| service:lambda | 13 |
| Boto3 | 11 |
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
| 2026-09-28T19:43:26Z | ap-south-1 | cloudformation | DescribeStacks | aws-cli |  |
| 2026-09-28T19:43:26Z | ap-south-1 | cloudformation | DescribeStackEvents | sam-cli |  |
| 2026-09-28T19:43:28Z | ap-south-1 | logs | FilterLogEvents | aws-cli | InvalidParameterException |
