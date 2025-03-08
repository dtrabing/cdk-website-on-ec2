from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class NetworkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(self, "MyVPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="PublicSubnet1", subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(name="PrivateSubnet1", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                ec2.SubnetConfiguration(name="PublicSubnet2", subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(name="PrivateSubnet2", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            ]
        )

        cdk.CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
