#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_website_on_ec2.network_stack import NetworkStack
from cdk_website_on_ec2.server_stack import ServerStack

env = cdk.Environment(account="084375588860", region="us-east-1")

app = cdk.App()

network_stack = NetworkStack(app, "NetworkStack", env=env)

server_stack = ServerStack(app, "ServerStack", vpc=network_stack.vpc, env=env)

app.synth()
