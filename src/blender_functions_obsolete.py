r"'''"
# Change font size in blender's python console..
# bpy.context.space_data.font_size = 18

# After opening blender you want to save your file first, to access "bpy.data.filepath". This gives Blender a path to search.
# bpy.ops.wm.save_mainfile(filepath=("E:\\AWS\\My Project\\AWS_Blender_programs\\temp.blend"))    # Make sure we save the temp.blend where we have othwe python source codes.
# bpy.ops.wm.save_mainfile(filepath=('E:\\AWS\\My Project\\AWS_Blender_programs\\temp.blend'))

# When first opening blender....
# import os, sys, bpy ; sys.path.append(os.path.dirname(bpy.data.filepath)); import ec2_dep_pattern      [Press Ctrl+V to paste in python console]

# Make blender pick changes from "below" modules...
# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.ec2_pattern((0,-4,0), 25)
# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.elastic_beanstalk_pattern((0,4,0), 1)

# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.create_public_sub((0,-4,0))
# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.create_private_sub((0, 4,0))

# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.create_public_networkacl((0,-4,0)) : over Private subnet.
# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.create_private_networkacl((0,4,0)) : over Public subnet.

# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.create_route((0,-4,0))
# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.create_route((0,4,0))

# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.create_internet_gateway((0, -4, 0))
# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.create_route_connector((0, -4, 0), (0, 4, 0))
# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.components_connector((0, -4, 3.5), (0, -4, 4.5))
# import importlib ; importlib.reload(ec2_dep_pattern) ; import ec2_dep_pattern ; ec2_dep_pattern.components_connector((0, 4, 2.5), (0, 4, 5.5))



# NOTES:
# Press [CTRL] + SPACE to autocomplete in Python console.
r"'''"

import os
import sys
import bpy
import math                             # for sqrt function.
from math import cos, sin, radians

def frange (start, stop, step):
    '''
    This function implements a floating point "for loop". Start, End, and Step can be passed as floating point value.
    '''
    i = start
    while (i < stop):
        yield (i)
        i += step

def get_object_offset (number_of_objects, columns, spacing):            # Remember: 1st two args are integer and spacing is a tuple.
    '''
    Get Object location (x,y,z coordinates)
    number_of_objects = Number of Objects to draw. (integer)
    columns = number of columns (integer)
    spacing = Spacing between objects (a tuple of x,y,z coordinates)

    Returns = A tuple of (x,y,z coordinates)
    '''
    x_offset = (number_of_objects % columns) * spacing[0]
    y_offset = (number_of_objects // columns) * spacing[1]
    z_offset = spacing[2]
    return (x_offset, y_offset, z_offset)


def create_public_sub(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_Public_Subnet.blend"
    section = "\\Object\\"
    object = "AWS_Public_Subnet"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=coord, constraint_axis=(True, True, True))


def create_private_sub(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_Private_Subnet.blend"
    section = "\\Object\\"
    object = "AWS_Private_Subnet"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=coord, constraint_axis=(True, True, True))

def create_security_group(xco, yco, zco):
    #SGRP = ["AWS_SecurityGroup.blend", "\\Object\\", "AWS_SecurityGroup"]
    #FDR = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_Instance.blend"
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_SecurityGroup.blend"
    section = "\\Object\\"
    object = "AWS_SecurityGroup"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    # convert coord tuple into list so that we can create SG just above EC2.
    #coord_list = list(coord)
    zco += 1

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(xco, yco, zco), constraint_axis=(True, True, True))


def create_public_networkacl(coord):
    #SGRP = ["AWS_SecurityGroup.blend", "\\Object\\", "AWS_SecurityGroup"]
    #FDR = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_Instance.blend"
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_NetworkAcl_Public.blend"
    section = "\\Object\\"
    object = "AWS_NetworkAcl"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    x = coord[0]
    y = coord[1]
    z = coord[2] + 3

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

def create_private_networkacl(coord):
    #SGRP = ["AWS_SecurityGroup.blend", "\\Object\\", "AWS_SecurityGroup"]
    #FDR = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_Instance.blend"
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_NetworkAcl_Private.blend"
    section = "\\Object\\"
    object = "AWS_NetworkAcl"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    x = coord[0]
    y = coord[1]
    z = coord[2] + 3

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))


def create_internet_gateway(coord):
    # AIG = ["AWS_InternetGateway.blend", "\\Object\\", "AWS_InternetGateway"]
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_InternetGateway.blend"
    section = "\\Object\\"
    object = "AWS_InternetGateway"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    x = coord[0]
    y = coord[1]
    z = coord[2] + 6.5

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

def create_route_table(coord):
    '''
    Creates an route table and envelope around VPC route. This method is called by create_route.
    '''
    x = coord[0]
    y = coord[1]
    z = coord[2]

    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_RouteTable_with_Envelope.blend"
    section = "\\Object\\"
    object1 = "AWS_RouteTable"
    object2 = "AWS_Route_Envelope"

    filepath1 = blendfile + section + object1
    directory1 = blendfile + section
    filename1 = object1

    filepath2 = blendfile + section + object2
    directory2 = blendfile + section
    filename2 = object2

    bpy.ops.wm.append(filepath=filepath2, filename=filename2, directory=directory2)
    bpy.context.scene.objects.active = bpy.data.objects[object2]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

    bpy.ops.wm.append(filepath=filepath1, filename=filename1, directory=directory1)
    bpy.context.scene.objects.active = bpy.data.objects[object1]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

def create_route(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_VPC_Router.blend"
    section = "\\Object\\"
    object = "AWS_VPC_Router"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    x = coord[0]
    y = coord[1]
    z = coord[2] + 4.5

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

    create_route_table((x,y,z))

def create_route_connector(public_route_coord, private_route_coord):
    # The co-ordinates are passed a a tuple. In order to calculate distance we need co-ordinates.
    public_xco = public_route_coord[0]
    public_yco = public_route_coord[1]
    public_zco = public_route_coord[2]

    private_xco = private_route_coord[0]
    private_yco = private_route_coord[1]
    private_zco = private_route_coord[2]
    #print (private_xco)
    #print (private_yco)

    scale_factor = (math.sqrt(math.pow((public_xco - private_xco),2) + math.pow((public_yco - private_yco),2) + math.pow((public_zco - private_zco), 2))) / 2
    private_zco += 4.5

    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_Network_Connector.blend"
    section = "\\Object\\"
    object = "AWS_Network_Connector"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    #bpy.ops.transform.translate(value=(0, 0, 4.5), constraint_axis=(True, True, True))
    bpy.ops.transform.translate(value=(private_xco, private_yco, private_zco), constraint_axis=(False, False, True))
    #bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2.11, view_align=False, enter_editmode=False, location=(0, 0, 0))
    #bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')
    #bpy.ops.transform.translate(value=(0,0,0), constraint_orientation='GLOBAL')
    #bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')
    bpy.context.object.scale[2] = scale_factor          # (This 3 units both side, so the over all length becomes 6 units)


def components_connector(pointA_coord, pointB_coord):
    '''
    This connects various AWS components stacked vertically. Since this is a vertical connector, The function expects the source and
    destination co-ordinates to have same x and y coordinates. Only z co-coordinate should have different values with magnitude of
    pointA_coord less than pointB_coord's.
    '''
    pointA_xco = pointA_coord[0]
    pointA_yco = pointA_coord[1]
    pointA_zco = pointA_coord[2]

    pointB_xco = pointB_coord[0]
    pointB_yco = pointB_coord[1]
    pointB_zco = pointB_coord[2]

    if (pointB_zco <= pointA_zco):
        print ("Can\'t join components from top to down. Destination\'s [z] co-cordinate must be larger than source\'s")
        return (-1)
    else:
        connector_location = ((pointB_zco - pointA_zco) / 2)

    scale_factor = (math.sqrt(math.pow((pointB_xco - pointA_xco),2) + math.pow((pointB_yco - pointA_yco),2) + math.pow((pointB_zco - pointA_zco), 2))) / 2

    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_Components_Connector.blend"
    section = "\\Object\\"
    object = "AWS_Components_Connector"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    # Make the connector vertical...again ;)
    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    #bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')
    bpy.ops.transform.translate(value=(pointA_xco, pointA_yco, (pointA_zco+connector_location)), constraint_axis=(True, True, True), constraint_orientation='GLOBAL')
    bpy.context.object.scale[2] = scale_factor

def create_ec2(coord, num_ins, radius):
    '''
    This function is called by ec2_pattern.
    '''
    #FDR = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_Instance.blend"
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_Instance.blend"
    section = "\\Object\\"
    object = "AWS_EC2_Instance"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    theta = 0
    xco = coord[0]
    yco = coord[1]
    zco = coord[2]
    #radius = 1.0
    if (num_ins == 1):
        radius = 0
    dist = 6.28 / num_ins                   # Divide the circle in equal spacing to accomodate EC2 instances.
    while (theta < 6.28):
        x = xco + radius * cos(theta)       # (rad * cos(*))-> follow a circular path. with xco as center.
        y = yco + radius * sin(theta)
        z = zco                             # These three variables form co-ordinates for EC2 on the fly.

        bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
        bpy.context.scene.objects.active = bpy.data.objects[object]
        bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

        create_security_group(x, y, z)      # create SG on top of EC2.
        theta += dist

def ec2_pattern(coord, num_ins):
    if (num_ins < 10):
        create_ec2(coord, num_ins, 1)
    if (num_ins >=10 and num_ins < 26):
        instances_in_inner_circle = 10
        create_ec2(coord, instances_in_inner_circle, 1)
        instances_in_outer_circle = (num_ins - 10)
        create_ec2(coord, instances_in_outer_circle, 1.75)
    if (num_ins >=26 and num_ins < 50):
        instances_in_inner_circle = 10
        create_ec2(coord, instances_in_inner_circle, 1)
        instances_in_second_circle = 16
        create_ec2(coord, instances_in_second_circle, 1.75)
        instances_in_outer_circle = (num_ins - (10+16))
        create_ec2(coord, instances_in_outer_circle, 2.5)
        '''
    if (num_ins >=50 and num_ins < 80):
        instances_in_inner_circle = 10
        create_ec2(coord, instances_in_inner_circle, 1)
        instances_in_second_circle = 16
        create_ec2(coord, instances_in_second_circle, 1.75)
        instances_in_third_circle = 50
        create_ec2(coord, instances_in_third_circle, 2.5)
        instances_in_outer_circle = (num_ins - (10+16+50))
        create_ec2(coord, instances_in_outer_circle, 3.5)
        '''

'''
        radius = 1.0
        if (num_ins == 1):
            radius = 0
        dist = 6.28 / num_ins
        while (theta < 6.28):
            x = xco + radius * cos(theta)       # (rad * cos(*))-> follow a circular path. with xco as center.
            y = yco + radius * sin(theta)
            z = zco                             # These three variables form co-ordinates for EC2 on the fly.

            bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
            bpy.context.scene.objects.active = bpy.data.objects[object]
            bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

            create_security_group(x, y, z)
            # create EC2 on top of SG.

            theta += dist

    if (num_ins >=10 and num_ins <27):
        rings = 2
    if (num_ins >=27 and num_ins <40):
        rings = 3
    for radius in frange(1, rings, 0.75):
        #print (radius)
        theta = 0
        #if (num_ins % 2 == 0):                      # Works only for EVEN number of instances.
        #if (radius == 1):
            dist = (6.28 / 9)
            while (theta < 6.28):
                x = xco + radius * cos(theta)       # (rad * cos(*))-> follow a circular path. with xco as center.
                y = yco + radius * sin(theta)
                z = zco

                bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
                bpy.context.scene.objects.active = bpy.data.objects[object]
                bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

                create_security_group(x, y, z)
                theta += dist
'''

def elastic_beanstalk_pattern(coord, num_ins, beanstalk_app = 'yes', sec_grp = 'yes'):
    #FDR = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_Instance.blend"
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_ElasticBeanstalk.blend"
    section = "\\Object\\"
    object = "AWS_ElasticBeanstalk"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    xco = coord[0]
    yco = coord[1]
    zco = coord[2]
    theta = 0

    if (num_ins <= 10):
        radius = 0.5
        if (num_ins == 1):
            radius = 0
        dist = 6.28 / num_ins
        while (theta < 6.28):
            x = xco + radius * cos(theta)       # (rad * cos(*))-> follow a circular path. with xco as center.
            y = yco + radius * sin(theta)
            z = zco

            bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
            bpy.context.scene.objects.active = bpy.data.objects[object]
            bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

            # Time to create a Application entitiy on top of Beanstalk (if exists)
            z += 1.2                          # Separation between bleanstalk and application.
            create_beanstalk_app((x,y,z))
            z += 1                            # Separation between beanstalk app and security group.
            create_beanstalk_security_group((x, y, z))
            theta += dist

    if (num_ins >=11 and num_ins <=20):
        rings = 1.5
        for radius in frange(0.5, rings, 0.5):
            #print (radius)
            theta = 0
            if (num_ins % 2 == 0):
                dist = (6.28 / (num_ins/2))
                while (theta < 6.28):
                    x = xco + radius * cos(theta)       # (rad * cos(*))-> follow a circular path. with xco as center.
                    y = yco + radius * sin(theta)
                    z = zco

                    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
                    bpy.context.scene.objects.active = bpy.data.objects[object]
                    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

                    # As of now, No provision of creating app deployment in case of multiple beanstalk deployments.
                    theta += dist

def create_beanstalk_app(coord):
    #FDR = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_Instance.blend"
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_ElasticBeanstalk_Deployment.blend"
    section = "\\Object\\"
    object = "AWS_ElasticBeanstalk_Deployment"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    x = coord[0]
    y = coord[1]
    z = coord[2]

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

def create_beanstalk_security_group(coord):
    #FDR = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_Instance.blend"
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_SecurityGroup.blend"
    section = "\\Object\\"
    object = "AWS_SecurityGroup"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    x = coord[0]
    y = coord[1]
    z = coord[2]

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))
