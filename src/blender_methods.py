r"'''"
# Change font size in blender's python console..
# bpy.context.space_data.font_size = 18
import os, sys, bpy
# After opening blender you want to save your file first, to access "bpy.data.filepath". This gives Blender a path to search.
# bpy.ops.wm.save_mainfile(filepath=("E:\\AWS\\My Project\\AWS_Blender_programs\\trial1.blend"))    # Make sure we save the temp.blend where we have othwe python source codes.
# bpy.ops.wm.save_mainfile(filepath=('E:\\AWS\\My Project\\AWS_Blender_programs\\temp.blend'))

# When first opening blender....
sys.path.append(os.path.dirname(bpy.data.filepath))
import blender_methods      #[Do this first, then un-hash the next line and run in python console]
#import importlib ; importlib.reload(blender_methods)

print ("Entered")
# Make blender pick changes from "below" modules...
# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.ec2_pattern((0,-4,0), 25)
# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.elastic_beanstalk_pattern((0,4,0), 1)

#import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_public_sub((0,0,0))
#import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_private_sub((0, 4,0))

# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_public_networkacl((0,-4,0)) : over Private subnet.
# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_private_networkacl((0,4,0)) : over Public subnet.

# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_route((0,-4,0))
# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_route((0,4,0))

# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_internet_gateway((0, -4, 0))
# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_route_connector((0, -4, 0), (0, 4, 0))
# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.components_connector((0, -4, 3.5), (0, -4, 4.5))
# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.components_connector((0, 4, 2.5), (0, 4, 5.5))

# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_DBInstance_MultiAZ(1, (0,4,0))
# import importlib ; importlib.reload(blender_methods) ; import blender_methods ; blender_methods.draw_DBInstance(1, (0,4,0))
# NOTES:
# Press [CTRL] + SPACE to autocomplete in Python console.
r"'''"
import bpy
import os
import sys
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


def Slope(x, y):
    p1_x = x[0]
    p1_y = x[1]
    p1_z = x[2]

    p2_x = y[0]
    p2_y = y[1]
    p2_z = y[2]

    if (p1_x == p2_x):
        if (p2_y == p1_y):
            angle = 1.5708
            return (angle)
        else:
            # x-plane is constant. We calculate angle considering y & z coordinates.
            ratio = (p2_z - p1_z) / (p2_y - p1_y)
            angle = math.atan(ratio)
            return (angle)          # In radians
            #print (math.degrees(angle))
    elif (p1_z == p2_z):
        angle = 1.5708
        #print (angle)
        return (angle)


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


def draw_public_sub(coord):
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


def draw_private_sub(coord):
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

def draw_security_group(xco, yco, zco):
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

    # convert coord tuple into list so that we can draw SG just above EC2.
    #coord_list = list(coord)
    x = coord[0]
    y = coord[1]
    z = coord[2] + 3
    #zco += 1

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

    z = coord[2] + 2
    return [x, y, z]

def draw_SecurityGroup(count, coord):
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

    # convert coord tuple into list so that we can draw SG just above EC2.
    #coord_list = list(coord)
    x = coord[0]
    y = coord[1]
    z = coord[2]
    #zco += 1

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

    z = coord[2] + 1
    return [x, y, z]

def draw_public_networkacl(coord):
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
    z = coord[2]

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

    z = coord[2] + 1.5
    return [x, y, z]

def draw_private_networkacl(coord):
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
    z = coord[2]

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

    z = coord[2] + 1.5
    return [x, y, z]

def draw_internet_gateway(coord):
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
    z = coord[2]

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

    z = coord[2] + 1
    return [x, y, z]

def draw_route_table(coord):
    '''
    Creates an route table and envelope around VPC route. This method is called by draw_route.
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

def draw_PublicRoute(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_VPC_Public_Router.blend"
    section = "\\Object\\"
    object = "AWS_VPC_Public_Router"

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

    draw_route_table((x,y,z))

    z = coord[2] + 2
    return [x, y, z]

def draw_PrivateRoute(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_VPC_Private_Router.blend"
    section = "\\Object\\"
    object = "AWS_VPC_Private_Router"

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

    draw_route_table((x,y,z))

    z = coord[2] + 2
    return [x, y, z]


def draw_route_connector(public_route_coord, private_route_coord):
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




def draw_Connectors(source, dest, scale_factor, call_count = "None"):
    # The co-ordinates are passed a a tuple. In order to calculate distance we need co-ordinates.
    public_xco = source[0]
    public_yco = source[1]
    public_zco = source[2]

    private_xco = dest[0]
    private_yco = dest[1]
    private_zco = dest[2]
    #print (private_xco)
    #print (private_yco)

    dist = ((dest[0] - source[0])**2 + (dest[1] - source[1])**2 + (dest[2] - source[2])**2)**0.5

    mid_point = ((dest[0] + source[0])/2, (dest[1] + source[1])/2, (dest[2] + source[2])/2)

    #scale_factor = (math.sqrt(math.pow((public_xco - private_xco),2) + math.pow((public_yco - private_yco),2) + math.pow((public_zco - private_zco), 2))) / 2
    #scale_factor = (dist * 2)

    slope = Slope(source, dest)

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
    if (call_count != "None"):
        object = "AWS_Network_Connector"+".00"+str(call_count)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(mid_point[0], mid_point[1], mid_point[2]), constraint_axis=(False, False, False))
    #bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2.11, view_align=False, enter_editmode=False, location=(0, 0, 0))
    #bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')
    #bpy.ops.transform.translate(value=(0,0,0), constraint_orientation='GLOBAL')
    bpy.ops.transform.rotate(value=(slope), axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')
    bpy.context.object.scale[2] = scale_factor          # (This 3 units both side, so the over all length becomes 6 units)
    #if (slope == 1.5708):
    #    bpy.ops.transform.resize(value=(5.19073, 5.19073, 5.19073), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')
        #bpy.context.object.scale[0] = scale_factor
    #bpy.ops.object.select_all(action='DESELECT')
    #bpy.ops.transform.resize(value = (scale_factor), constraint_axis = (True, True, True))



def draw_Horizontal_Connectors(source, dest, scale_factor, call_count = "None"):
    # The co-ordinates are passed a a tuple. In order to calculate distance we need co-ordinates.
    public_xco = source[0]
    public_yco = source[1]
    public_zco = source[2]

    private_xco = dest[0]
    private_yco = dest[1]
    private_zco = dest[2]
    #print (private_xco)
    #print (private_yco)

    dist = ((dest[0] - source[0])**2 + (dest[1] - source[1])**2 + (dest[2] - source[2])**2)**0.5

    mid_point = ((dest[0] + source[0])/2, (dest[1] + source[1])/2, (dest[2] + source[2])/2)

    #scale_factor = (math.sqrt(math.pow((public_xco - private_xco),2) + math.pow((public_yco - private_yco),2) + math.pow((public_zco - private_zco), 2))) / 2
    #scale_factor = (dist * 2)

    slope = Slope(source, dest)
    #print ("Slope Value returned:" + str(slope))

    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_Horizontal_Connector.blend"
    section = "\\Object\\"
    object = "AWS_Horizontal_Connector"


    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    if (call_count != "None"):
        object = "AWS_Network_Connector"+".00"+str(call_count)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(mid_point[0], mid_point[1], mid_point[2]), constraint_axis=(False, False, False))
    bpy.ops.transform.rotate(value=(slope), axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')
    bpy.context.object.scale[2] = scale_factor          # (This 3 units both side, so the over all length becomes 6 units)
    #if (slope == 1.5708):
    #    bpy.ops.transform.resize(value=(5.19073, 5.19073, 5.19073), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')
        #bpy.context.object.scale[0] = scale_factor
    #bpy.ops.object.select_all(action='DESELECT')
    #bpy.ops.transform.resize(value = (scale_factor), constraint_axis = (True, True, True))

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

def draw_ec2(coord, num_ins, radius):
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

        draw_security_group(x, y, z)      # draw SG on top of EC2.
        theta += dist

        z = z + 3
        return [x, y, z]

def ec2_pattern(coord, num_ins):
    if (num_ins < 10):
        draw_ec2(coord, num_ins, 1)
    if (num_ins >=10 and num_ins < 26):
        instances_in_inner_circle = 10
        draw_ec2(coord, instances_in_inner_circle, 1)
        instances_in_outer_circle = (num_ins - 10)
        draw_ec2(coord, instances_in_outer_circle, 1.75)
    if (num_ins >=26 and num_ins < 50):
        instances_in_inner_circle = 10
        draw_ec2(coord, instances_in_inner_circle, 1)
        instances_in_second_circle = 16
        draw_ec2(coord, instances_in_second_circle, 1.75)
        instances_in_outer_circle = (num_ins - (10+16))
        draw_ec2(coord, instances_in_outer_circle, 2.5)
        '''
    if (num_ins >=50 and num_ins < 80):
        instances_in_inner_circle = 10
        draw_ec2(coord, instances_in_inner_circle, 1)
        instances_in_second_circle = 16
        draw_ec2(coord, instances_in_second_circle, 1.75)
        instances_in_third_circle = 50
        draw_ec2(coord, instances_in_third_circle, 2.5)
        instances_in_outer_circle = (num_ins - (10+16+50))
        draw_ec2(coord, instances_in_outer_circle, 3.5)
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

            draw_security_group(x, y, z)
            # draw EC2 on top of SG.

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

                draw_security_group(x, y, z)
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

            # Time to draw a Application entitiy on top of Beanstalk (if exists)
            z += 1.2                          # Separation between bleanstalk and application.
            draw_beanstalk_app((x,y,z))
            z += 1                            # Separation between beanstalk app and security group.
            draw_beanstalk_security_group((x, y, z))
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

def draw_beanstalk_app(coord):
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

def draw_beanstalk_security_group(coord):
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

def draw_DBInstance_MultiAZ(count, coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_DBonInstance-MultiAZ.blend"
    section = "\\Object\\"
    object = "AWS_EC2_DBonInstance-MultiAZ"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    z = coord[2] + 0.5
    return [x, y, z]

def draw_DBInstance(count, coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_EC2_DBonInstance.blend"
    section = "\\Object\\"
    object = "AWS_EC2_DBonInstance"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    z = coord[2] + 0.5
    return [x, y, z]

def draw_DBSecurityGroup(count, coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_DB_SecurityGroup.blend"
    section = "\\Object\\"
    object = "AWS_DB_SecurityGroup"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    z = coord[2] + 2
    return [x, y, z]

def draw_AutoScalingGroup(count, coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_AutoScalingGroup.blend"
    section = "\\Object\\"
    object = "AWS_AutoScalingGroup"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    z = coord[2] + 1
    return [x, y, z]

def draw_ElasticLoadBalancer(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_ApplicationLoadBalancer.blend"
    section = "\\Object\\"
    object = "AWS_ApplicationLoadBalancer"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    z = coord[2] + 1
    return [x, y, z]


def draw_ELBSecurityGroup(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_ELBSecurityGroup.blend"
    section = "\\Object\\"
    object = "AWS_ELBSecurityGroup"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    z = coord[2] + 1
    return [x, y, z]

def draw_VPNGateway(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_VPNGateway.blend"
    section = "\\Object\\"
    object = "AWS_VPNGateway"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    x = coord[0] + 2
    return [x, y, z]

def draw_VPNConnection(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_VPC_VPN_Connection.blend"
    section = "\\Object\\"
    object = "AWS_VPC_VPN_Connection"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    x = coord[0] + 2
    return [x, y, z]

def draw_CustomerGateway(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_CustomerGateway.blend"
    section = "\\Object\\"
    object = "AWS_CustomerGateway"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    x = coord[0] + 2
    return [x, y, z]

def draw_OnPrem(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\On_Premise_Building.blend"
    section = "\\Object\\"
    object = "On_Premise_Building"

    filepath = blendfile + section + object
    # print(filepath)
    directory = blendfile + section
    # print(directory)
    filename = object
    # print(filename)

    x = coord[0] + 1
    y = coord[1]
    z = 0

    bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
    bpy.context.scene.objects.active = bpy.data.objects[object]
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(True, True, True))

    # Raise the z-coordinate by 0.5 for SecurityGroup.
    x = coord[0]
    return [x, y, coord[2]]


def draw_VPC(coord):
    blendfile = "E:\\AWS\\My Project\\AWS_Blender_programs\\blend_files\\AWS_VPC.blend"
    section = "\\Object\\"
    object = "AWS_VPC"

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

    # Raise the z-coordinate by 0.5 for SecurityGroup.
