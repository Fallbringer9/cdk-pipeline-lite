#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import Environment

from cdk_pipeline_lite.application_stack import ApplicationStack
from cdk_pipeline_lite.pipeline_stack import PipelineStack

app = cdk.App()

env_eu = Environment(
    account="309232818774",
    region="eu-west-3",
)

application_stack = ApplicationStack(
    app,
    "ApplicationStack",
    env=env_eu,
)

pipeline_stack = PipelineStack(
    app,
    "PipelineStack",
    target_lambda_name=application_stack.app_lambda.function_name,
    env=env_eu,
)

#Le pipeline dépend de la stack appli
pipeline_stack.add_dependency(application_stack)

app.synth()