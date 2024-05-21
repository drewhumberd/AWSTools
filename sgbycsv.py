import csv
import boto3

client = boto3.client('ec2')

vpc = input("Please provide the VPC ID where the security group will be built.\n")
sg_name = input("Please provide a name for the security group.\n")
sg_desc = input("Please provide a description for the security group.\n")
sg_response = client.create_security_group(
    Description=sg_desc,
    GroupName=sg_name,
    VpcId=vpc,
    TagSpecifications=[
        {
            'ResourceType': 'security-group',
            'Tags': [
                {
                'Key': 'Name',
                'Value': sg_name
                }
            ]
        }
    ]
)
sg_id = sg_response["GroupId"]
print(f"{sg_id} created.")

rules=[]

with open('test.csv', encoding="utf-8") as csvfile:
    csv_data = csv.reader(csvfile)
    next(csv_data, None)
    for row in csv_data:
        cidr = row[0]
        startingport = int(row[1])
        endport = int(row[2])
        protocol = row[3]
        description = row[4]
        rule = {
                "FromPort": startingport,
                "IpProtocol": protocol,
                "IpRanges": [
                    {
                        "CidrIp": cidr,
                        "Description": description
                    }
                ],
                "ToPort": endport
        }
        rules.append(rule)

rules_response = client.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=rules
)
print('--------------------------------------------------------------------')
for rule in rules_response['SecurityGroupRules']:
    print("")
    print(f"   Security Group Rule ID: {rule['SecurityGroupRuleId']}")
    print(f"   Security Group ID: {rule['GroupId']}")
    print(f"   Protocol: {rule['IpProtocol']}")
    print(f"   Port Range: {str(rule['FromPort'])}-{str(rule['ToPort'])}")
    print(f"   IP Range: {rule['CidrIpv4']}")
    print(f"   Rule Description: {rule['Description']}")
    print("")
    print('--------------------------------------------------------------------')
