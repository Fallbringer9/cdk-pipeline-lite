from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
)
from constructs import Construct


class ApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Role IAM minimal pour la Lambda
        lambda_role = iam.Role(
            self,
            "AppLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Permissions basiques : logs uniquement
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        # La Lambda qui sera déployée par le pipeline
        self.app_lambda = _lambda.Function(
            self,
            "AppLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda"),
            role=lambda_role,
            function_name="pipeline-lite-demo",
        )

        # Output pour récupérer facilement son nom
        from aws_cdk import CfnOutput
        CfnOutput(
            self,
            "LambdaName",
            value=self.app_lambda.function_name
        )