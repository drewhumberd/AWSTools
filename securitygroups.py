import boto3
import botocore.exceptions

client = boto3.client('ec2')

print("Welcome to the Security Group Maker")
new_sg_answer = input("Is this a new security group? Y/N\n").lower()
if new_sg_answer == "y":
    vpc = input("Please provide the VPC ID where the security group will be built.\n")
    sg_name = input("Please provde a name for the security group.\n")
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
else:
    sg_id = input("Please provide the Security Group ID you want to add rules to.\n")
    try:
        sg_response = client.describe_security_groups(
            GroupIds=[sg_id]
        )
    except botocore.exceptions.ClientError:
        print("Invalid Security Group ID - Please try again.")
        exit()

cidrs = {}
gettingcidrs = True
while gettingcidrs:
    cidr = input("Provide a CIDR that requires whitelisting in the SG.\n")
    cidrs[cidr] = []
    gettingports = True
    while gettingports:
        portrange = {}
        portrange["startingport"] = int(input("Provide the first port in the port range for the specified CIDR.\n"))
        portrange["endport"] = int(input("Provide the last port in the port range for the specified CIDR. Same as first port if only one port in range is needed.\n"))
        portrange["protocol"] = input("TCP or UDP?\n").upper()
        portrange["cidr"] = cidr
        cidrs[cidr].append(portrange)
        contports = input("Need to add more ports? Y/N\n")
        if contports == "n":
            gettingports = False
    contcidrs = input("Need to add more CIDRs? Y/N\n")
    if contcidrs == "n":
        gettingcidrs = False

permissions = []
for cidr in cidrs.values():
    for rule in cidr:
        permissions.append(
            {
                "FromPort": rule["startingport"],
                "IpProtocol": rule["protocol"],
                "IpRanges": [
                    {
                        "CidrIp": rule["cidr"],
                        "Description": ""
                    }
                ],
                "ToPort": rule["endport"]
            }
        )

rules_response = client.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=permissions
)

print('--------------------------------------------------------------------')
for rule in rules_response['SecurityGroupRules']:
    print("")
    print(f"   Security Group Rule ID: {rule['SecurityGroupRuleId']}")
    print(f"   Security Group ID: {rule['GroupId']}")
    print(f"   Protocol: {rule['IpProtocol']}")
    print(f"   Port Range: {str(rule['FromPort'])}-{str(rule['ToPort'])}")
    print(f"   IP Range: {rule['CidrIpv4']}")
    print("")
    print('--------------------------------------------------------------------')