import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_sqs_sns_lambda.aws_sqs_sns_lambda_stack import AwsSqsSnsLambdaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_sqs_sns_lambda/aws_sqs_sns_lambda_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsSqsSnsLambdaStack(app, "aws-sqs-sns-lambda")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
