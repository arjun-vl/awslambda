import boto3
import json
import logging
import datetime 
import os
from botocore.exceptions import ClientError
from datetime import timedelta

region ='us-east-1'
ec2 = boto3.resource('ec2',region)
client = boto3.client('ec2',region)
snsClient = boto3.client('sns',region)

def publish_sns():
    print('Publish Messsage to SNS Topic')
    subject_str = 'Alert! AWS PPT EC2 Instances Started / Stopped'
    affected_instances1 = [instance1.id for instance1 in stop]
    affected_instances2 = [instance2.id for instance2 in start]
    DT = datetime.datetime.now() + timedelta(hours = 5.5)

    Waqt = DT.strftime("%Y-%m-%d %H:%M:%S")
    msg = '\n\nHello Team, \n\nFollowing EC2 instances have been started / stopped: \n\nStopped instance ID: \n'+ str(affected_instances1)+ '\n\nStarted instances ID: \n'+str(affected_instances2)+'\n\nInstance state changed time IST: '+str(Waqt)+''
    response = snsClient.publish(TopicArn='your SNS Topic ARN',Message=msg,Subject=subject_str)
    print response
    
def lambda_handler(event, context):
    global stop
    global start
    stop = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    start = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance1 in stop:
        print('Ec2 Instances which are stopped: ', 'Instance ID: ', instance1.id, 'Instance state: ', instance1.state, 'Instance type: ',instance1.instance_type)
    for instance2 in start:
        print('Ec2 Instances which are running: ', 'Instance ID: ', instance2.id, 'Instance state: ', instance2.state, 'Instance type: ',instance2.instance_type)
       
    publish_sns()
