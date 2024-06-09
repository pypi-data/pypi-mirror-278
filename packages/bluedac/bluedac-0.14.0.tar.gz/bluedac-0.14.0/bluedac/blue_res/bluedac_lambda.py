from aws_cdk import (
    Duration,
    aws_codedeploy as codedeploy,
    RemovalPolicy,
    aws_lambda as AWS_Lambda,
    aws_cloudwatch as cloudwatch
)

from bluedac.utils.stack_utils import StackUtils as utils

class Bluedac_Lambda(AWS_Lambda.Function):

    def __init__(self, lambda_name, file_name, handler_name, stack, environment):
        super().__init__(
            stack,
            lambda_name,
            runtime=AWS_Lambda.Runtime.PYTHON_3_12,
            code=AWS_Lambda.Code.from_asset("resources"),
            handler=f"{file_name}.{handler_name}"
        )

        self.stack = stack
        self.environment = environment

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, stack):
        self._stack = stack


    def apply_deployment_strategy(self, fun_name: str,
        removal_policy = RemovalPolicy.RETAIN, alarm_config: dict = dict()):
        """Applies desired release strategy to specified lambda function. """

        release_strategy = utils.get_rs_info(self.environment)

        match release_strategy["name"]:
            case "canary":
                traffic_routing = codedeploy.TimeBasedCanaryTrafficRouting(
                    interval=Duration.minutes(release_strategy["interval"]),
                    percentage=release_strategy["percentage"]
                )

            case "linear":
                traffic_routing = codedeploy.TimeBasedLinearTrafficRouting(
                    interval=Duration.minutes(release_strategy["interval"]),
                    percentage=release_strategy["percentage"]
                )
            
            case _:
                traffic_routing = codedeploy.AllAtOnceTrafficRouting.all_at_once()


        new_version = self.current_version
        new_version.apply_removal_policy(removal_policy)

        alias = AWS_Lambda.Alias(
            self.stack,
            f"{release_strategy["name"]}-{fun_name}",
            alias_name=f"{fun_name}-alias",
            version=new_version
        )

        alarm = cloudwatch.Alarm(
            self.stack,
            f"{release_strategy["name"]}-Alarm-{fun_name}",
            metric=alias.metric(alarm_config["metric"]),
            threshold=alarm_config["threshold"],
            evaluation_periods=alarm_config["period"]
        ) if alarm_config else None

        config = codedeploy.LambdaDeploymentConfig(
            self.stack,
            f"{release_strategy["name"]}DeploymentConfig-{fun_name}",
            traffic_routing=traffic_routing
        )

        codedeploy.LambdaDeploymentGroup(
            self.stack,
            f"{release_strategy["name"]}DeploymentGroup-{fun_name}",
            alias=alias,
            deployment_config=config,
            alarms=[alarm] if alarm else None
        )