#!/usr/bin/env python
import os
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, TerraformAsset, AssetType
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.default_vpc import DefaultVpc
from cdktf_cdktf_provider_aws.default_subnet import DefaultSubnet
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction
from cdktf_cdktf_provider_aws.lambda_permission import LambdaPermission
from cdktf_cdktf_provider_aws.data_aws_caller_identity import DataAwsCallerIdentity
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket
from cdktf_cdktf_provider_aws.s3_bucket_cors_configuration import S3BucketCorsConfiguration, S3BucketCorsConfigurationCorsRule
from cdktf_cdktf_provider_aws.s3_bucket_notification import S3BucketNotification, S3BucketNotificationLambdaFunction
from cdktf_cdktf_provider_aws.dynamodb_table import DynamodbTable, DynamodbTableAttribute

class ServerlessStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        AwsProvider(self, "AWS", region="us-east-1")

        account_id = DataAwsCallerIdentity(self, "acount_id").account_id
        
        bucket = S3Bucket(
            self, "bucketpostgram",
            bucket_prefix = "bucketpostgram",
            acl="private",
            force_destroy=True,
            versioning= {"enabled":True}
            )

        S3BucketCorsConfiguration(
            self, "cors",
            bucket=bucket.id,
            cors_rule=[S3BucketCorsConfigurationCorsRule(
                allowed_headers = ["*"],
                allowed_methods = ["GET", "HEAD", "PUT"],
                allowed_origins = ["*"]
            )]
            )

        dynamo_table = DynamodbTable(
            self, "DynamodDB-table",
            name= "dynamo_postgram",
            hash_key="user",
            range_key="id",
            attribute=[
            DynamodbTableAttribute(name="user",type="S" ),
            DynamodbTableAttribute(name="id",type="S" )
            ],
            billing_mode="PROVISIONED",
            read_capacity=5,
            write_capacity=5,
            )

        code = TerraformAsset(
            self, "code",
            path="./lambda",
            type= AssetType.ARCHIVE
        )

        lambda_function = LambdaFunction(self,
                "lambda",
                function_name="lambda_postgram",
                runtime="python3.12",
                memory_size=128,
                timeout=60,
                role=f"arn:aws:iam::{account_id}:role/LabRole",
                filename= code.path,
                handler="lambda_function.lambda_handler",                
                environment={"variables": {"dynamo_table_id": dynamo_table.id}}
            )

        permission = LambdaPermission(
            self, "lambda_permission",
            action="lambda:InvokeFunction",
            statement_id="AllowExecutionFromS3Bucket",
            function_name=lambda_function.arn,
            principal="s3.amazonaws.com",
            source_arn=bucket.arn,
            source_account=account_id,
            depends_on=[lambda_function, bucket]
        )

        notification = S3BucketNotification(
            self, "notification",
            lambda_function=[S3BucketNotificationLambdaFunction(
                lambda_function_arn=lambda_function.arn,
                events=["s3:ObjectCreated:*"]
            )],
            bucket=bucket.id,
            depends_on=[permission]
        )

        TerraformOutput(
            self, "s3_id",
            value=bucket.id,
            )
        
        TerraformOutput(
            self,
            "dynamodb_id",
            value= dynamo_table.id
        )
       

app = App()
ServerlessStack(app, "cdktf_serverless")
app.synth()

