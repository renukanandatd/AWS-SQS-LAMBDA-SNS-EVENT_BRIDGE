from aws_cdk import (
    Stack,
    Duration,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_sources,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_iam as iam
)
from constructs import Construct

class AwsSqsSnsLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create SQS queue with custom settings
        queue = sqs.Queue(
            self, "MyQueue",
            visibility_timeout=Duration.seconds(300),  # Polling duration
            delivery_delay=Duration.seconds(0),        # Delivery delay
            retention_period=Duration.days(4),         # Message retention period
            max_message_size_bytes=256*1024            # Maximum message size (256 KB)
        )

        # Create SNS topic
        topic = sns.Topic(
            self, "MyTopic"
        )

        # Lambda function to process SQS messages
        function = _lambda.Function(
            self, "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="MyFunction.main",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(300)
        )

        # Grant Lambda permissions to read from SQS
        queue.grant_consume_messages(function)

        # Grant Lambda permissions to put events to EventBridge
        function.add_to_role_policy(iam.PolicyStatement(
            actions=["events:PutEvents"],
            resources=["arn:aws:events:*:*:event-bus/default"]
        ))

        # Attach the CloudWatch Logs policy to the Lambda execution role
        function.add_to_role_policy(iam.PolicyStatement(
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
            resources=["*"]
        ))

        # Add SQS as an event source to the Lambda function
        function.add_event_source(lambda_event_sources.SqsEventSource(queue))

        # Create EventBridge rule with correct event pattern format
        rule = events.Rule(
            self, "MyRule",
            event_pattern=events.EventPattern(
                source=["my.source"],
                detail_type=["Order"]
            )
        )

        # Add SNS topic as target to EventBridge rule
        rule.add_target(targets.SnsTopic(topic))

        # Add email subscription to SNS topic
        topic.add_subscription(subscriptions.EmailSubscription("renukananda2000@gmail.com"))
