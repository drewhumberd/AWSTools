import boto3
import csv

client = boto3.client('ec2')

response = client.describe_security_groups()

data = response["SecurityGroups"]

header = ["GroupName", "GroupId", "VpcId", "FromPort", "ToPort", "IpProtocol", "CidrIP"]
with open("results.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(header)
# filtered_data = []
for sg in data:
    IpPerms = sg["IpPermissions"]
    for perm in IpPerms:
        iprange = perm["IpRanges"]
        for ipset in iprange:
            cidr = ipset["CidrIp"]
            groupname=sg["GroupName"]
            groupid=sg["GroupId"]
            vpcid=sg["VpcId"]
            try:
                fromport = perm["FromPort"]
            except KeyError:
                pass
            else:
                toport = perm["ToPort"]
            protocol = perm["IpProtocol"]
            # filtered_data.append(
            #     {
            #         "GroupName": groupname,
            #         "GroupId": groupid,
            #         "VpcId": vpcid,
            #         "FromPort": fromport,
            #         "ToPort": toport,
            #         "IpProtocol": protocol,
            #         "CidrIP": cidr
            #     }
            # )
            csv_data = [groupname, groupid, vpcid, fromport, toport, protocol, cidr]
            with open("results.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(csv_data)
