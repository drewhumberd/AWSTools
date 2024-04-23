import boto3
import pandas as pd

ec2 = boto3.client('ec2')
response=ec2.describe_instances() # pulls all data for all instances in region
instancelist = [] # creates empty list for instances
req_data = ["InstanceId", "InstanceType", "PlatformDetails", "ImageId"]
for reservation in (response["Reservations"]):
    for instance in reservation["Instances"]:
        inst = {type:instance[type] for type in req_data} # creates empty dictionary for each instance
        inst["AZ"] = instance["Placement"]["AvailabilityZone"]
        for tag in instance["Tags"]:
            if tag["Key"] == "Name":
                inst["Name"] = tag["Value"] # retrieves Name tag if it exists
        instancelist.append(inst) # adds inst dictionary to list

for inst in instancelist:
    id = inst.get("InstanceId")
    instance_volumes=ec2.describe_volumes(
        Filters=[
            {
                'Name': 'attachment.instance-id',
                'Values': [
                    id,
                ]
            },
        ]
    ) # retrieves ec2 volumes attached to each instance polled in previous command
    total_storage = 0 # sets initial storage value to 0
    for volume in (instance_volumes["Volumes"]):
        size = volume["Size"] # retrives volume size
        total_storage += size # adds size to total_storage
    inst["Total Storage"] = total_storage # adds total_storage as a key/value pair in inst, which is dictionary for each instance

table = pd.DataFrame(instancelist) # creates table based on data
print(table.to_markdown())