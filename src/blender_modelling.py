r"'''"
# Change font size in blender's python console..
# bpy.context.space_data.font_size = 18

# After opening blender you want to save your file first, to access "bpy.data.filepath". This gives Blender a path to search.
# bpy.ops.wm.save_mainfile(filepath=("E:\\AWS\\My Project\\AWS_Blender_programs\\temp.blend"))
# bpy.ops.wm.save_mainfile(filepath=('E:\\AWS\\My Project\\AWS_Blender_programs\\temp.blend'))

# When first opening blender....
# import os, sys, bpy ; sys.path.append(os.path.dirname(bpy.data.filepath)); import blend_structs [Press Ctrl+V to paste in python console]

# Make blender pick changes to "texture_painter" module...
# import importlib ; importlib.reload(blend_structs) ; import blend_structs ; blend_structs.go(coord)

# NOTES:
# Press [CTRL] + SPACE to autocomplete in Python console.
r"'''"

import os
import sys
from aws_structs import Location_Engine
from ec2_dep_pattern import ec2_pattern

# Path to Blender files:
file_to_parse = "E:\AWS\Blender files\parsed_file.txt"

FDR = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\"
ALB = ["AWS_ApplicationLoadBalancer.blend", "\\Object\\", "AWS_App_LoadBalancer"]
ROU = ["AWS_VPC_Router.blend", "\\Object\\", "AWS_VPC_Router"]
ASG = ["AWS_AutoScalingGroup.blend", "\\Object\\", "AWS_AutoScalingGroup"]
EC2 = ["AWS_EC2_Instance.blend", "\\Object\\", "AWS_EC2_Instance"]
CGW = ["AWS_CustomerGateway.blend", "\\Object\\", "AWS_CustomerGateway"]
DBI = ["AWS_EC2_DBonInstance.blend", "\\Object\\", "AWS_EC2_DBonInstance"]
EIP = ["AWS_EC2_ElasticIP.blend", "\\Object", "AWS_EC2_ElasticIP"]
ECR = ["AWS_ECRR_Register.blend", "\\Object\\", "AWS_ECRRegistry"]
ECC = ["AWS_ECS_EC2_Compute_Container.blend", "\\Object\\", "AWS_ECS_EC2_Compute_Container"]
EBK = ["AWS_ElasticBeanstalk.blend", "\\Object\\", "AWS_ElasticBeanstalk"]
EBD = ["AWS_ElasticBeanstalk_Deployment.blend", "\\Object", "AWS_ElasticBeanstalk_Deployment"]
ELB = ["AWS_ElasticLoadBalancer.blend", "\\Object\\", "AWS_ElasticLoadBalancer"]
AIG = ["AWS_InternetGateway.blend", "\\Object\\", "AWS_InternetGateway"]
LMD = ["AWS_Lambda.blend", "\\Object\\", "AWS_Lambda"]
AS3 = ["AWS_S3.blend", "\\Object\\", "AWS_S3"]
VEP = ["AWS_VPC_Endpoint.blend", "\\Object\\", "AWS_VPC_EndPoint"]
VNG = ["AWS_VPC_NAT_Gateway.blend", "\\Object\\", "AWS_VPC_NAT_Gateway"]
VPR = ["AWS_VPC_Peering.blend", "\\Object\\", "AWS_VPC_Peering"]
VPN = ["AWS_VPN_Connection.blend", "\\Object\\", "AWS_VPN_Connection"]
VGW = ["AWS_VPNGateway.blend", "\\Object\\", "AWS_VPNGateway"]
PUS = ["AWS_Public_Subnet.blend", "\\Object\\", "AWS_Public_Subnet"]
PRS = ["AWS_Private_Subnet.blend", "\\Object\\", "AWS_Private_Subnet"]
NACL_Public = ["AWS_NetworkAcl_Public.blend", "\\Object\\", "AWS_NetworkAcl"]
NACL_Private = ["AWS_NetworkAcl_Private.blend", "\\Object\\", "AWS_NetworkAcl"]
SGRP = ["AWS_SecurityGroup.blend", "\\Object\\", "AWS_SecurityGroup"]
AWS_Route_Table_Envelope = ["AWS_RouteTable_with_Envelope.blend", "\\Object", "AWS_RouteTable", "AWS_Route_Envelope"]
AWS_Network_Connector = ["AWS_Network_Connector.blend", "\\Object","AWS_Network_Connector"]
AWS_Components_Connector = ["AWS_Components_Connector.blend", "\\Object", "AWS_Components_Connector"]


blend_data = Location_Engine("E:\AWS\Blender files\parsed_file.txt")        # Instantiate Location_Engine.
vpc_coord = blend_data.count_vpc()              # retusns vpc co-ordinates. Makes vpc_name list available.
vpc_subnet = blend_data.vpc_to_subnet()         # returns vpc to subnet dictionary. Make subnet_names list available.
obj_offset = blend_data.locate_object_offsets() # returns subnet co-ordinates.
sub_to_ins = blend_data.subnet_to_instance()    # returns subnet_to_instance_map. Makes instances_in_vpc available.
vpc_to_sg = blend_data.vpc_to_securitygroup()
ins_to_sg = blend_data.instance_to_securitygroups()
#print (sum(obj_offset.values(), []))

#v = str(vpc_coord.values())
v = (sum(vpc_coord.values(), []))          # sum converts lists of lists to a list.
v[0] = (v[0] - 2)                          # push x-coordinate to (x-2)
print (blend_data.vpc_name)
print (v)
print (sub_to_ins)
print (blend_data.subnet_to_instance_nums)
print (obj_offset)
print (blend_data.instances_in_vpc)
print (ins_to_sg)
'''
def go(loc):
    blendfile = FDR + EC2[0]
    section = EC2[1]
    object = EC2[2]

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=loc, constraint_axis=(True, True, True))


# Create EC2 instances.
for vpc in blend_data.vpc_name:
    for subnet in blend_data.subnet_names:
        if (subnet in obj_offset):
            coord = tuple(obj_offset[subnet])
            print (coord)
            for sub, i in blend_data.subnet_to_instance_nums.items():
                if (subnet in sub):
                    ec2_pattern(coord, i)

'''





'''
def go():
    # Setup
    #blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS ApplicationLoadBalancer.blend"
    #section = "\\Object\\"
    #object = "AWS_App_LoadBalancer"

    blendfile = FDR + VGW[0]
    section = VGW[1]
    object = VGW[2]

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)
    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)

    #Activate newly created object
    bpy.context.scene.objects.active = bpy.data.objects[object]

    #Transform object to desired location
    bpy.ops.transform.translate(value=v, constraint_axis=(True, True, True))
'''
