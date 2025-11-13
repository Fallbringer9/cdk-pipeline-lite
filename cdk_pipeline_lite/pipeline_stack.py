from aws_cdk import (
    Stack,
    aws_codebuild as codebuild,
    aws_iam as iam,
)
from constructs import Construct


class PipelineStack(Stack):
    """
    Stack dédiée au CI/CD.

    On crée uniquement un projet CodeBuild
    qui va :
      - zipper le dossier lambda/
      - appeler aws lambda update-function-code
    """

    def __init__(self, scope: Construct, construct_id: str, *, target_lambda_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Rôle IAM pour CodeBuild
        cb_role = iam.Role(
            self,
            "CodeBuildRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
        )

        # Logs CloudWatch + accès de base CodeBuild
        cb_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSCodeBuildDeveloperAccess"
            )
        )

        # Permission pour mettre à jour le code d'une Lambda
        cb_role.add_to_policy(
            iam.PolicyStatement(
                actions=["lambda:UpdateFunctionCode"],
                resources=["*"],  # simplifié pour l'apprentissage
            )
        )

        # Projet CodeBuild
        self.build_project = codebuild.Project(
            self,
            "LambdaUpdateProject",
            role=cb_role,
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0,
                privileged=False,
            ),
            environment_variables={
                "FUNCTION_NAME": codebuild.BuildEnvironmentVariable(
                    value=target_lambda_name
                ),
                "AWS_DEFAULT_REGION": codebuild.BuildEnvironmentVariable(
                    value=self.region
                ),
            },
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "install": {
                            "runtime-versions": {
                                "python": "3.11"
                            }
                        },
                        "build": {
                            "commands": [
                                "echo 'Packing lambda code...'",
                                "cd lambda",
                                "zip -r ../function.zip .",
                                "cd ..",
                                "echo 'Updating Lambda function code...'",
                                "aws lambda update-function-code "
                                "--function-name $FUNCTION_NAME "
                                "--zip-file fileb://function.zip "
                                "--region $AWS_DEFAULT_REGION",
                            ]
                        },
                    },
                    "artifacts": {
                        "files": [
                            "function.zip"
                        ]
                    },
                }
            ),
        )