from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds
from constructs import Construct

class ServerStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Security Group for Web Server
        web_sg = ec2.SecurityGroup(self, "WebSG",
            vpc=vpc,
            description="Allow HTTP traffic",
            allow_all_outbound=True
        )
        web_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")

        # Security Group for RDS
        rds_sg = ec2.SecurityGroup(self, "RDSSG",
            vpc=vpc,
            description="Allow MySQL traffic from Web Server",
            allow_all_outbound=True
        )
        rds_sg.add_ingress_rule(web_sg, ec2.Port.tcp(3306), "Allow MySQL from Web Server")

        # Launch Web Server in each Public Subnet
        for index, subnet in enumerate(vpc.public_subnets):
            ec2.Instance(self, f"WebServer{index}",
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnets=[subnet]),
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
                machine_image=ec2.AmazonLinuxImage(),
                security_group=web_sg
            )

        # RDS MySQL Database
        rds_instance = rds.DatabaseInstance(self, "MyRDS",
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_groups=[rds_sg],
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            allocated_storage=20,
            credentials=rds.Credentials.from_generated_secret("admin"),
        )
