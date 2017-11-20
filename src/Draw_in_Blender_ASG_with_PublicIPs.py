r"'''"
# Change font size in blender's python console..
# bpy.context.space_data.font_size = 18

# After opening blender you want to save your file first, to access "bpy.data.filepath". This gives Blender a path to search.
# bpy.ops.wm.save_mainfile(filepath=("E:\\AWS\\My Project\\AWS_Blender_programs\\tempX.blend"))
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
import re
import bpy

bpy.ops.wm.save_mainfile(filepath=("E:\\AWS\\My Project\\AWS_Blender_programs\\Draw_in_Blender_ASG_With_PublicIPs.blend"))
sys.path.append(os.path.dirname(bpy.data.filepath))

from aws_structs import Location_Engine
import blender_methods
import importlib ; importlib.reload(blender_methods)

# Path to Blender files:
#file_to_parse = "/home/redhat/AWS/config_data/parsedfile1.cfg"
#file_to_parse = "E:\\AWS\\My Project\\AWS_Blender_programs\\pf_VPC_With_VPN_Connection.txt"
#file_to_parse = "E:\\AWS\\My Project\\AWS_Blender_programs\\pf_VPC_AutoScaling_With_Public_IPs.txt"
#file_to_parse = "E:\\AWS\\My Project\\AWS_Blender_programs\\pf_VPC_ASG_and_ELB.txt"

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

#blend_data = Location_Engine("E:\\AWS\\My Project\\AWS_Blender_programs\\pf_VPC_With_VPN_Connection.txt")
blend_data = Location_Engine("E:\\AWS\\My Project\\AWS_Blender_programs\\pf_VPC_AutoScaling_With_Public_IPs.txt")        # Instantiate Location_Engine.
blend_data.build_default_objects()
vpc_coord = blend_data.count_vpc()                  # returns vpc co-ordinates. Makes vpc_name list available.
vpc_to_sub = blend_data.vpc_to_subnet()             # Maps VPC to Subnet and Returns: List of Subnets.vpc_to_subnet
obj_offset = blend_data.locate_object_offsets()     # returns subnet co-ordinates.
subnet_type = blend_data.subnet_to_type_map()       # Returns subnet:subnet type in dictionary
vpc_pub_stack = blend_data.vpc_public_stack()       # Build VPC public stack.
vpc_pri_stack = blend_data.vpc_private_stack()      # Build VPC Provate stack. Returns: VPD(Key): Resources (values)
res_in_subnets = blend_data.resources_in_subnet()   # Returns: Dictionary of subnet(key): Resources(values)
vpc_subnet = blend_data.vpc_to_subnet()             # returns vpc to subnet dictionary. Make subnet_names list available.
sub_to_ins = blend_data.subnet_to_instance()        # returns subnet_to_instance_map. Makes instances_in_vpc available.
vpc_to_sg = blend_data.vpc_to_securitygroup()
ins_to_sg = blend_data.instance_to_securitygroups()
#print (sum(obj_offset.values(), []))


#v = str(vpc_coord.values())
print (vpc_coord)
v = (sum(vpc_coord.values(), []))          # sum converts lists of lists to a list.
print (v)
#v[0] = (v[0] - 2)                          # push x-coordinate to (x-2)
print (blend_data.vpc_name)
print (v)
print (vpc_to_sub)
print (obj_offset)
print (subnet_type)
print (vpc_pub_stack)
print (vpc_pri_stack)
print (res_in_subnets)
#print (sub_to_ins)
#print (blend_data.subnet_to_instance_nums)
#print (blend_data.instances_in_vpc)
#print (ins_to_sg)
print ()
coordinate_tracker = {}
public_vpc_tracker = []

def draw_subnets():
    for sub, clas in subnet_type.items():
        for subnet, coord in obj_offset.items():
            new_co_ords = draw_resources_in_subnet(subnet, coord)
            if (sub in subnet and "Public" in clas  or "public" in clas):
                blender_methods.draw_public_sub(coord)
            elif (sub in subnet and "Private" in clas  or "private" in clas):
                blender_methods.draw_private_sub(coord)

            # This dictionary tracks co-ordinates of all subnets in the infrastructure.
            coordinate_tracker[subnet] = new_co_ords

print (coordinate_tracker)      # This keeps track of Subnets


def draw_resources_in_subnet(subnet_name, coordinates):
    for subnet, resources in res_in_subnets.items():
        if(subnet == subnet_name):
            local_coord = coordinates
            if (resources[0] != '' and "MultiAZ" in resources[0]):
                local_coord = blender_methods.draw_DBInstance_MultiAZ(1, local_coord)
            elif(resources[0] != ''):
                local_coord = blender_methods.draw_DBInstance(1, local_coord)
            if (resources[1] != '' and "DBSecurityGroup" in resources[1]):
                local_coord = blender_methods.draw_DBSecurityGroup(1, local_coord)
            if (resources[2] != '' and "Instance" in resources[2]):
                local_coord = blender_methods.draw_ec2(local_coord, 1, 1)
            if (resources[2] != '' and "AutoScalingGroup" in resources[2]):
                local_coord = blender_methods.draw_AutoScalingGroup(1, local_coord)
            if (resources[2] != '' and "SecurityGroup" in resources[2]):
                local_coord = blender_methods.draw_SecurityGroup(1, local_coord)

    return local_coord


def draw_private_vpc_stack():
    global coordinate_tracker               # Keeps track of co-ordinates or resources in subnets.
    reversed_stack = []
    local_coord = {}                        # Copies co-ordinates for tracking co-ordinates in this VPC.
    subnet_name = []
    local_unified_coord_tracker = []        # This is passed as argument for resources to be created at a particular co-ordinate.
    centroid_x = centroid_y = centroid_z = 0
    for vpc in blend_data.vpc_name:
        for key, value in(vpc_pri_stack.items()):
            reversed_stack = (value[::-1])
            size = len(reversed_stack)
            print (reversed_stack)
            for subnet in reversed_stack[0]:            # This loop will go through each subnet present in VPC public stack.
                print(subnet)
                if subnet in coordinate_tracker:
                    subnet_name.append(subnet)
                    local_coord[subnet] = coordinate_tracker[subnet]    # Buid the list of coordinates for each subnet.
                    print (local_coord)

            num_subnets = len(reversed_stack[0])
            if (num_subnets == 2):
                # calculate the center/centroid. Max 4 subnets will be considered.
                centroid_x = (local_coord[subnet_name[0]][0] + local_coord[subnet_name[1]][0])/2
                centroid_y = (local_coord[subnet_name[0]][1] + local_coord[subnet_name[1]][1])/2
                if (local_coord[subnet_name[0]][2] > local_coord[subnet_name[1]][2]):
                    local_coord[subnet_name[0]][2] = local_coord[subnet_name[1]][2]
                else:
                    local_coord[subnet_name[1]][2] = local_coord[subnet_name[0]][2]
                centroid_z = (local_coord[subnet_name[0]][2] + local_coord[subnet_name[1]][2])/2
                centroid_z += 1
                #print (centroid_x, centroid_y, centroid_z)
                local_unified_coord_tracker = [centroid_x, centroid_y, centroid_z]
            if (num_subnets == 3):
                centroid_x = (local_coord[subnet_name[0]][0] + local_coord[subnet_name[1]][0] + local_coord[subnet_name[2]][0])/3
                centroid_y = (local_coord[subnet_name[0]][1] + local_coord[subnet_name[1]][1] + local_coord[subnet_name[2]][1])/3
                if (local_coord[subnet_name[0]][2] > local_coord[subnet_name[1]][2]):
                    local_coord[subnet_name[1]][2] = local_coord[subnet_name[0]][2]
                    if (local_coord[subnet_name[0]][2] > local_coord[subnet_name[2]][2]):
                        local_coord[subnet_name[2]][2] = local_coord[subnet_name[0]][2]
                    else:
                        local_coord[subnet_name[0]][2] = local_coord[subnet_name[2]][2]
                        local_coord[subnet_name[1]][2] = local_coord[subnet_name[0]][2]

                elif (local_coord[subnet_name[0]][2] < local_coord[subnet_name[1]][2]):
                    local_coord[subnet_name[0]][2] = local_coord[subnet_name[1]][2]
                    if (local_coord[subnet_name[0]][2] > local_coord[subnet_name[2]][2]):
                        local_coord[subnet_name[2]][2] = local_coord[subnet_name[0]][2]
                    else:
                        local_coord[subnet_name[0]][2] = local_coord[subnet_name[2]][2]
                        local_coord[subnet_name[1]][2] = local_coord[subnet_name[0]][2]

                centroid_z = (local_coord[subnet_name[0]][2] + local_coord[subnet_name[1]][2] + local_coord[subnet_name[2]][2])/3
                centroid_z += 1
                #print (centroid_x, centroid_y, centroid_z)
                local_unified_coord_tracker = [centroid_x, centroid_y, centroid_z]
            else:
                centroid_z += 1
                #print (centroid_x, centroid_y, centroid_z)
                local_unified_coord_tracker = [centroid_x, centroid_y, centroid_z]

            for nacl in reversed_stack[1]:
                if (nacl != ""):
                    if (local_unified_coord_tracker[2] < 2):
                        local_unified_coord_tracker[2] = 3
                    nacl_coord_tracker = local_unified_coord_tracker
                    # As of now there are only one NetworkACLs encountered, but if there are more use the z-coord increment factor to control the NACL stack. This can be passed to draw... function as parameter.
                    local_unified_coord_tracker = blender_methods.draw_private_networkacl(local_unified_coord_tracker)
                    blender_methods.draw_Connectors(nacl_coord_tracker, nacl_coord_tracker, 1)

            if (reversed_stack[2] != ""):
                source = local_unified_coord_tracker
                local_unified_coord_tracker = blender_methods.draw_PrivateRoute(local_unified_coord_tracker)
                dest = local_unified_coord_tracker
                #print (source, dest)
                blender_methods.draw_Connectors(source, dest, 1, 1)     # Remember to pass the call_number (last argument)

            if (reversed_stack[3] != ""):
                vpn_coord_tracker = local_unified_coord_tracker
                local_unified_coord_tracker = blender_methods.draw_VPNGateway(local_unified_coord_tracker)

            if (reversed_stack[4] != ""):
                vpn_conn_coord_tracker = local_unified_coord_tracker
                local_unified_coord_tracker = blender_methods.draw_VPNConnection(local_unified_coord_tracker)
                #print (vpn_coord_tracker, local_unified_coord_tracker)
                #blender_methods.draw_Horizontal_Connectors(vpn_coord_tracker, local_unified_coord_tracker, 1)

            if (reversed_stack[4] != ""):
                cg_coord_tracker = local_unified_coord_tracker
                blender_methods.draw_Horizontal_Connectors(cg_coord_tracker, local_unified_coord_tracker, 3)
                local_unified_coord_tracker = blender_methods.draw_CustomerGateway(local_unified_coord_tracker)

                local_unified_coord_tracker = blender_methods.draw_OnPrem(local_unified_coord_tracker)
                #on_prem_tracker = local_unified_coord_tracker
                #blender_methods.draw_Horizontal_Connectors(cg_coord_tracker, on_prem_tracker, 1, 1)

    return local_unified_coord_tracker


def draw_public_vpc_stack():
    global coordinate_tracker
    reversed_stack = []
    local_coord = {}
    subnet_name = []
    local_unified_coord_tracker = []
    for vpc in blend_data.vpc_name:
        for key, value in(vpc_pub_stack.items()):
            reversed_stack = (value[::-1])
            size = len(reversed_stack)
            for subnet in reversed_stack[0]:            # This loop will go through each subnet present in VPC public stack.
                #print(subnet)
                if subnet in coordinate_tracker:
                    subnet_name.append(subnet)
                    local_coord[subnet] = coordinate_tracker[subnet]    # Buid the list of coordinates for each subnet.

            num_subnets = len(reversed_stack[0])
            if (num_subnets == 2):
                # calculate the center/centroid. Max 4 subnets will be considered.
                centroid_x = (local_coord[subnet_name[0]][0] + local_coord[subnet_name[1]][0])/2
                centroid_y = (local_coord[subnet_name[0]][1] + local_coord[subnet_name[1]][1])/2
                if (local_coord[subnet_name[0]][2] > local_coord[subnet_name[1]][2]):
                    local_coord[subnet_name[0]][2] = local_coord[subnet_name[1]][2]
                else:
                    local_coord[subnet_name[1]][2] = local_coord[subnet_name[0]][2]
                centroid_z = (local_coord[subnet_name[0]][2] + local_coord[subnet_name[1]][2])/2
                centroid_z += 1
                #print (centroid_x, centroid_y, centroid_z)
                local_unified_coord_tracker = [centroid_x, centroid_y, centroid_z]
            if (num_subnets == 3):
                centroid_x = (local_coord[subnet_name[0]][0] + local_coord[subnet_name[1]][0] + local_coord[subnet_name[2]][0])/3
                centroid_y = (local_coord[subnet_name[0]][1] + local_coord[subnet_name[1]][1] + local_coord[subnet_name[2]][1])/3
                if (local_coord[subnet_name[0]][2] > local_coord[subnet_name[1]][2]):
                    local_coord[subnet_name[1]][2] = local_coord[subnet_name[0]][2]
                    if (local_coord[subnet_name[0]][2] > local_coord[subnet_name[2]][2]):
                        local_coord[subnet_name[2]][2] = local_coord[subnet_name[0]][2]
                    else:
                        local_coord[subnet_name[0]][2] = local_coord[subnet_name[2]][2]
                        local_coord[subnet_name[1]][2] = local_coord[subnet_name[0]][2]

                elif (local_coord[subnet_name[0]][2] < local_coord[subnet_name[1]][2]):
                    local_coord[subnet_name[0]][2] = local_coord[subnet_name[1]][2]
                    if (local_coord[subnet_name[0]][2] > local_coord[subnet_name[2]][2]):
                        local_coord[subnet_name[2]][2] = local_coord[subnet_name[0]][2]
                    else:
                        local_coord[subnet_name[0]][2] = local_coord[subnet_name[2]][2]
                        local_coord[subnet_name[1]][2] = local_coord[subnet_name[0]][2]

                centroid_z = (local_coord[subnet_name[0]][2] + local_coord[subnet_name[1]][2] + local_coord[subnet_name[2]][2])/3
                centroid_z += 1
                #print (centroid_x, centroid_y, centroid_z)
                local_unified_coord_tracker = [centroid_x, centroid_y, centroid_z]
            else:
                centroid_z += 1
                #print (centroid_x, centroid_y, centroid_z)
                local_unified_coord_tracker = [centroid_x, centroid_y, centroid_z]

            elb_count = 0
            for elb in reversed_stack[1]:
                if (re.search(r'ELB:\w', elb)):
                    elb_coord_tracker = local_unified_coord_tracker
                    elb_count += 1
                    local_unified_coord_tracker = blender_methods.draw_ElasticLoadBalancer(local_unified_coord_tracker)
                if (re.search(r'SecGrp:\w', elb)):
                    local_unified_coord_tracker = blender_methods.draw_ELBSecurityGroup(local_unified_coord_tracker)

                # connect ELB with Subnets.
                point_1 = coordinate_tracker[subnet_name[0]]
                point_2 = coordinate_tracker[subnet_name[1]]
                for i in range(elb_count):
                    dest = elb_coord_tracker
                    blender_methods.draw_Connectors(point_1, dest, 1.5)
                    blender_methods.draw_Connectors(point_2, dest, 1.5, 1)

            for nacl in reversed_stack[2]:
                if (nacl != ""):
                    local_unified_coord_tracker = blender_methods.draw_public_networkacl(local_unified_coord_tracker)

            if (reversed_stack[3] != ""):
                local_unified_coord_tracker = blender_methods.draw_PublicRoute(local_unified_coord_tracker)

            if (reversed_stack[5] != ""):
                local_unified_coord_tracker = blender_methods.draw_internet_gateway(local_unified_coord_tracker)
                blender_methods.draw_Connectors(elb_coord_tracker, local_unified_coord_tracker, 2, 2)



draw_subnets()

public_vpc_tracker = draw_public_vpc_stack()

#.. And....finally....Bring in the VPC.
blender_methods.draw_VPC(v)
