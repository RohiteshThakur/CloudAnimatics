'''
Lessons Learned:
1. Never name a instance variable after a class method. Result: int object not callable. Because Python cannot decide what is what! and Integers are definitely not functions therefore, not callable.
2. The arguments passed to __init__() must be matched while instantiating a class.
3. While creating a dictionary, take time to understand what you are passing as a "Key". A list is not a valid key for a dictionary but a individual item of the key is. If we pass a list we'll get: TypeError: unhashable type list.
4. If you missed out on "self" in method definition, Python'll say: TypeError: Function takes 0 arguments but 1 is provided.
5. For passing a variable in regexe, we have to first make a regex string (see method: vpc_to_subnet)
7. Silly - but index of array can only be integers. array[4] and not array['four']
'''

r"'''"
# Change font size in blender's python console..
# bpy.context.space_data.font_size = 20

# After opening blender you want to save your file first, to access "bpy.data.filepath". This gives Blender a path to search.
# py.ops.wm.save_mainfile(filepath=('E:\Blender course\Blender programs\credits.blend'))
# py.ops.wm.save_mainfile(filepath=('C:\Users\Rohitesh\Blender Files\credits.blend'))

# When first opening blender....
# import os, sys, bpy ; sys.path.append(os.path.dirname(bpy.data.filepath)); import texture_painter [Press Ctrl+V to paste in python console]

# Make blender pick changes to "texture_painter" module...
# import importlib ; importlib.reload(texture_painter) ; import texture_painter ; texture_painter.go()

# NOTES:
# Press [CTRL] + SPACE to autocomplete in Python console.
r"'''"

# import bpy
import os
import sys
import re

file_to_parse = "E:\AWS\Blender files\parsed_file.txt"


def _save_scene_to_file():
    # This provides blender a filepath to refer to...
    bpy.ops.wm.save_mainfile(filepath="E:\AWS\My Project\AWS_Blender_programs\My_scene.blend")


'''
def _Create_EC2s(file_to_parse):

    ubnets decide the distribution of EC2 instances with in a VPC. As of now this method assumes we only have one VPC.
    Therefore, we will not perform explict checks on VPC.
    This function will return a list containing subnets.

    with open (file_to_parse) as conf_file:
        for line in conf_file:
            if ("AWS::EC2::Subnet|" in line):
                print (line)
'''


class Location_Engine():
    '''
    This class decides co-ordinates where AWS entities will be created in blender scene and returns the same.
    '''

    def __init__(self, file_to_parse):
        ''' Initialize co-ordinates'''
        self.x = 0
        self.y = 0
        self.z = 0
        self.file_handle = file_to_parse
        self.vpc_to_coord_map = {}                          # Dictionary of VPC and co-ordinates.
        self.subnet_to_coord_map = {}
        self.vpc_name = []                                  # List of VPCs in file.
        self.vpc_count = 0
        self.subnet_names = []
        self.subnet_name = []
        self.vpc_to_subnet_map = {}
        self.public_stack = []
        self.vpc_public_stack_map = {}
        self.private_stack = []
        self.vpc_private_stack_map = {}
        self.subnet_to_instance_map = {}
        self.subnet_to_instance_nums = {}
        self.public_networkacl = []
        self.private_networkacl = []
        self.internet_gateway = []
        self.private_instances = []
        self.public_instances = []
        self.securitygroups_in_vpc = []
        self.vpc_to_securitygroup_map = {}
        self.instances_in_vpc = []
        self.instance_to_securitygroups_map = {}
        self.vpc_to_elastic_beanstalk_stack = {}

    '''
    def return_file_handle(self, file_to_parse):
        try:
            with open (file_to_parse, 'r') as file_handle:
                return file_handle
        except FileNotFoundError:
            msg = "Sorry, the file" + file_to_parse + "does not exist."
            print (msg)
    '''

    def count_vpc(self):
        '''Parse simplified file and return co-ordinates as a list.'''
        with open(self.file_handle, 'r') as fh:
            for line in fh:
                # print(line)
                if ("AWS::EC2::VPC|" in line):
                    self.vpc_count += 1
                    self.vpc_name.append(str(line.split("|", 1)[0]))
                    # print(self.vpc_count)
                    # print(self.vpc_name)

            if (self.vpc_count == 1):
                self.coordinates = [self.x, self.y, self.z]
                self.vpc_to_coord_map[self.vpc_name[0]] = [self.x, self.y, self.z]
                return self.vpc_to_coord_map

            if (self.vpc_count == 2):
                self.y = -10
                self.vpc_to_coord_map[self.vpc_name[0]] = [self.x, self.y, self.z]
                self.y = 10
                self.vpc_to_coord_map[self.vpc_name[1]] = [self.x, self.y, self.z]
                return self.vpc_to_coord_map

            if (self.vpc_count == 3):
                self.x = -10
                self.vpc_to_coord_map[self.vpc_name[0]] = [self.x, self.y, self.z]
                self.x, self.y = 10, -10
                self.vpc_to_coord_map[self.vpc_name[1]] = [self.x, self.y, self.z]
                self.x, self.y = 10, 10
                self.vpc_to_coord_map[self.vpc_name[2]] = [self.x, self.y, self.z]
                return self.vpc_to_coord_map

            if (self.vpc_count == 4):
                self.x, self.y = 10, -10
                self.vpc_to_coord_map[self.vpc_name[0]] = [self.x, self.y, self.z]
                self.x, self.y = 10, 10
                self.vpc_to_coord_map[self.vpc_name[1]] = [self.x, self.y, self.z]
                self.x, self.y = -10, 10
                self.vpc_to_coord_map[self.vpc_name[2]] = [self.x, self.y, self.z]
                self.x, self.y = -10, -10
                self.vpc_to_coord_map[self.vpc_name[3]] = [self.x, self.y, self.z]
                return self.vpc_to_coord_map

        fh.close()

    def vpc_to_subnet(self):
        '''
        This method parses each VPC and returns subnets in each VPC in form of dictionary.
        '''
        subnet_name = ""
        # print(self.vpc_name)
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")                # Built a regex to make it uniq.
            # print(uniq_vpc)
            with open(self.file_handle, 'r') as fh:
                for line in fh:
                    if ("AWS::EC2::Subnet|" in line and re.search(uniq_vpc, line)):
                        # self.subnet_names.append(str(line.split("|", 1)[0]))
                        subnet_name = (str(line.split("|", 1)[0]))
                        self.subnet_names.append(subnet_name)

            self.vpc_to_subnet_map[vpc] = self.subnet_names
            # self.subnet_names.append(subnet_names)

        #print(self.subnet_names)
        # print(end='\n')
        # print(self.subnet_names)
        fh.close()
        return self.vpc_to_subnet_map


    def vpc_to_securitygroup(self):
        '''
        Since security groups are directly related to VPC, this function collects all security group in particular VPC.
        creates instance variable of list of security groups and returns a dictionary with VPC as key and security groups as
        values in an array.
        '''
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")
            with open(self.file_handle, 'r') as fh:
                for line in fh:
                    if ("AWS::EC2::SecurityGroup" in line and re.search(uniq_vpc, line)):
                        vpc_securitygroup = (str(line.split("|", 1)[0]))
                        self.securitygroups_in_vpc.append(vpc_securitygroup)

            self.vpc_to_securitygroup_map[vpc] = (self.securitygroups_in_vpc)

        # print(self.securitygroups)
        fh.close()
        return (self.vpc_to_securitygroup_map)

    def vpc_to_elasticbeanstalk(self):
        '''
        This method generates VPC to elasticbeanstalk mappings. A single elastic beanstalk can be a part of multiple Security Groups.
        Returns a dictionary with vpc as Key and elasticbeanstalk instance(s) as values.
        '''
        # instance variables used/needed (so make sure the methods using these variables are called):
        # self.securitygroups_in_vpc, self.instances_in_vpc
        # I have intentionally used local variables in this method, just to see the implications later on.
        # I will change them to instance variables if need be.
        elastic_beanstalk = []
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")
            with open(self.file_handle, 'r') as fh:
                for line in fh:
                    if ("AWS::ElasticBeanstalk::Environment" in line):
                        vpc_name = re.search(r"\|VPCId:\w+\|", line)
                        if vpc_name:
                            beanstalk_vpc     = (line[vpc_name.start() + 7 : vpc_name.end() - 1])
                            #elastic_beanstalk.append(beanstalk_vpc)

                        sub_net  = re.search(r"\|Subnets:\w+\|", line)
                        if sub_net:
                            beanstalk_sub_net  = (line[sub_net.start() + 9 : sub_net.end() - 1])
                            elastic_beanstalk.append(beanstalk_sub_net)

                        sec_grp  = re.search(r"\|SecurityGroups:\w+\|", line)
                        if sec_grp:
                            beanstalk_sec_grp = (line[sec_grp.start() + 16 : sec_grp.end() - 1])
                            elastic_beanstalk.append(beanstalk_sec_grp)

                        bs_name   = re.search(r"^\w+\|", line)
                        if bs_name:
                            beanstalk_name    = (line[:bs_name.end() - 1])
                            elastic_beanstalk.append(beanstalk_name)

                        app      = re.search(r"\|ApplicationName:\w+\|", line)
                        if app:
                            beanstalk_app     = (line[app.start() + 17 : app.end() - 1])
                            elastic_beanstalk.append(beanstalk_app)

            # Lets build the BeanStalk stack
            self.vpc_to_elastic_beanstalk_stack[beanstalk_vpc] = elastic_beanstalk
            elastic_beanstalk = []

        return self.vpc_to_elastic_beanstalk_stack

    def subnet_to_instance(self):
        '''
        This method generates mappings between Subnet and Security Groups and enveloped Instances in a particular VPC.
        Returns a dictionary with VPC as Key and subnet and EC2 instances as nested dictionary.
        '''
        instances_in_each_subnet = []
        instances_in_each_subnet_1 = []
        instance_count = 0
        instance_count_1 = 0
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")
            for subnet in self.subnet_names:
                # print(str(subnet))
                with open(self.file_handle, 'r') as fh:
                    for line in fh:
                        if (subnet in line and "AWS::EC2::Instance" in line):
                            #instance = ("EC2:"+(str(line.split("|", 1)[0])))
                            instance = (str(line.split("|", 1)[0]))
                            instance_count += 1
                            # print(instance)
                            # sec_grp = str((line.split("|")[-1]).split(":")[-1])
                            instances_in_each_subnet.append(instance)
                            # Total EC2 instances in particular VPC
                            self.instances_in_vpc.append(instance)
                        if ("AWS::ElasticBeanstalk::Environment" in line and ("|Subnets:" + subnet) in line):
                            #elb_instance = ("ElasticBeanstalk:"+(str(line.split("|", 1)[0])))
                            elb_instance = (str(line.split("|", 1)[0]))
                            instance_count_1 += 1
                            # print(elb_instance)
                            instances_in_each_subnet_1.append(elb_instance)

                if (instances_in_each_subnet):
                    self.subnet_to_instance_map[subnet] = (instances_in_each_subnet)
                    self.subnet_to_instance_nums[subnet] = instance_count
                if (instances_in_each_subnet_1):
                    self.subnet_to_instance_map[subnet] = (instances_in_each_subnet_1)
                    self.subnet_to_instance_nums[subnet] = instance_count_1
                    #self.subnet_to_instance_nums
                # self.instances_in_vpc.append(instances_in_each_subnet)
                instances_in_each_subnet = []
                instances_in_each_subnet_1 = []
                instance_count = 0
                instance_count_1 = 0

        #print(self.instances_in_vpc)
        fh.close()
        return (self.subnet_to_instance_map)

    def instance_to_securitygroups(self):
        '''
        This method generates EC2 instance to Security Groups mappings. A single instance can be a part of multiple Security Groups.
        Returns a dictionary with EC2 instance as Key and Security Groups as values.
        '''
        # instance variables used/needed (so make sure the methods using these variables are called):
        # self.securitygroups_in_vpc, self.instances_in_vpc
        security_group_list = []
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")
            for instance in self.instances_in_vpc:
                # print(str(subnet))
                with open(self.file_handle, 'r') as fh:
                    for line in fh:
                        if (instance in line):
                            for security_group in self.securitygroups_in_vpc:
                                if (security_group in line):
                                    # "tr" equivalent.
                                    sg = (line.split(":")[-1]).replace("\n", "")
                                    # print(sg)
                                    security_group_list.append(sg)

                self.instance_to_securitygroups_map[instance] = security_group_list
                security_group_list = []

        fh.close()
        return (self.instance_to_securitygroups_map)

    def vpc_public_stack(self):
        '''
        For IG to connect AWS VPC to external world it needs to remain connected to two things:
        1. VPC
        2. Route.

        This method searches for IG and finds out:
        1. Whether IG is attached to VPC.
        2. If there are more than one VPC then which VPC is attached to IG.
        3. Whether or not a route is attached to IG.
        '''
        public_networkacl = ""
        for vpc in self.vpc_name:
            for subnet in self.subnet_names:
                uniq_vpc = (r"\b" + vpc + r"\b")
                with open(self.file_handle, 'r') as fh:
                    for line in fh:
                        if ("AWS::EC2::InternetGateway|" in line):                      # only one per VPC
                            self.internet_gateway = (str(line.split("|", 1)[0]))
                        if ("AWS::EC2::VPCGatewayAttachment" in line and re.search(uniq_vpc, line)):
                            gateway = (str(line.split("|", 1)[0]))
                        if ("AWS::EC2::Route" in line and "|DependsOn:" + gateway + "|GatewayId:" + self.internet_gateway + "|" in line):
                            connected_route = str(line.split("|", 1)[0])
                            route_table = str(line.split("|",)[4])
                        if ("AWS::EC2::SubnetRouteTableAssociation" in line and route_table in line):
                            public_subnet = str(line.split("|",)[2])
                        if ("AWS::EC2::NetworkAcl" in line and re.search(uniq_vpc, line) and "Public" in line):
                            public_networkacl += (str(line.split("|", 1)[0]))

                self.public_networkacl.append(public_networkacl)
                self.public_stack = [self.internet_gateway, gateway,
                                     connected_route, self.public_networkacl, public_subnet]
                self.vpc_public_stack_map[vpc] = self.public_stack
                return self.vpc_public_stack_map
                fh.close()

    def vpc_private_stack(self):
        '''
        Gathers VPC components which are in private subnet.
        '''
        # local variables
        private_route = ""
        private_route_table = ""
        private_subnet = ""
        private_tag = ""
        private_networkacl = ""

        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")
            with open(self.file_handle, 'r') as fh:
                for line in fh:
                    if ("AWS::EC2::Route|" in line and self.internet_gateway not in line):
                        private_route = str(line.split("|", 1)[0])
                        private_route_table = str(line.split("|")[2])
                        # print(private_route_table)
                    if ("AWS::EC2::SubnetRouteTableAssociation" in line and private_route_table in line):
                        private_subnet = str(line.split("|")[2])
                    if ("AWS::EC2::Subnet" in line and "|Private|" in line):
                        private_tag = str(line.split("|")[2])
                    if ("AWS::EC2::NetworkAcl" in line and "Private" in line and re.search(uniq_vpc, line)):
                        private_networkacl += (str(line.split("|", 1)[0]))
                        # print(private_networkacl)
                    elif ("AWS::EC2::NetworkAcl" not in line and not (re.search(uniq_vpc, line))):
                        # No private subnet in the VPC.
                        self.private_stack = []

            self.private_networkacl.append(private_networkacl)
            self.private_stack = [private_route, self.private_networkacl, private_subnet]
            self.vpc_private_stack_map[vpc] = self.private_stack
            return self.vpc_private_stack_map
            fh.close()

    def locate_object_offsets(self):
        '''
        Genetates tuple of co-ordinates for subnets and instances. Takes in to consideration:
        1. Number of VPCs in file.
        2. Subnets in VPC.
        3. Instances in VPC.
        '''
        # VPC to subnet dict - self.vpc_to_subnet_map
        for vpc in self.vpc_name:
            # uniq_vpc = (r"\b" + vpc + r"\b")
            vpc_offset = (self.vpc_to_coord_map[vpc])
            # print(vpc_offset)
            # subnet_count = (self.vpc_to_subnet_map[vpc].values)
            # print(len(self.vpc_to_subnet_map))
            subnet_count = (len(self.subnet_names))
            if (subnet_count == 0 or subnet_count == 0):
                self.subnet_to_coord_map[self.subnet_names[0]] = [
                    vpc_offset[0], vpc_offset[1], vpc_offset[2]]
                # print(self.subnet_to_coord_map)

            if (subnet_count == 2):
                self.subnet_to_coord_map[self.subnet_names[0]] = [
                    vpc_offset[0], (vpc_offset[1] - 4), vpc_offset[2]]
                # print(self.subnet_to_coord_map[self.subnet_names[0]])
                self.subnet_to_coord_map[self.subnet_names[1]] = [
                    vpc_offset[0], (vpc_offset[1] + 4), vpc_offset[2]]
                # print(self.subnet_to_coord_map[self.subnet_names[1]])

            if (subnet_count == 3):
                self.subnet_to_coord_map[self.subnet_names[0]] = [
                    vpc_offset[0], (vpc_offset[1] - 4), vpc_offset[2]]
                print(self.subnet_to_coord_map[self.subnet_names[0]])
                self.subnet_to_coord_map[self.subnet_names[1]] = [
                    vpc_offset[0], (vpc_offset[1] + 4), vpc_offset[2]]
                print(self.subnet_to_coord_map[self.subnet_names[1]])
                self.subnet_to_coord_map[self.subnet_names[2]] = [
                    vpc_offset[0] + 4, (vpc_offset[1]), vpc_offset[2]]

            if (subnet_count == 4):
                self.subnet_to_coord_map[self.subnet_names[0]] = [
                    vpc_offset[0], (vpc_offset[1] - 4), vpc_offset[2]]
                print(self.subnet_to_coord_map[self.subnet_names[0]])
                self.subnet_to_coord_map[self.subnet_names[1]] = [
                    vpc_offset[0], (vpc_offset[1] + 4), vpc_offset[2]]
                print(self.subnet_to_coord_map[self.subnet_names[1]])
                self.subnet_to_coord_map[self.subnet_names[2]] = [
                    vpc_offset[0] + 4, (vpc_offset[1]), vpc_offset[2]]
                self.subnet_to_coord_map[self.subnet_names[3]] = [
                    vpc_offset[0] - 4, (vpc_offset[1]), vpc_offset[2]]

        return (self.subnet_to_coord_map)


cvpc = Location_Engine("E:\AWS\Blender files\parsed_file.txt")
# lst = cvpc.count_vpc("E:\AWS\Blender files\parsed_file.txt")
lst = cvpc.count_vpc()
print(lst)

sub = cvpc.vpc_to_subnet()
print(sub)

igvpc = cvpc.vpc_public_stack()
print(igvpc)

pvpc = cvpc.vpc_private_stack()
print(pvpc)

vpcsg = cvpc.vpc_to_securitygroup()
print(vpcsg)

stoi = cvpc.subnet_to_instance()
print(stoi)

# print(end='\n')
itosg = cvpc.instance_to_securitygroups()
print(itosg)

submap = cvpc.locate_object_offsets()
print(submap)

vtobk = cvpc.vpc_to_elasticbeanstalk()
print (vtobk)

print (cvpc.subnet_to_instance_nums)
print (cvpc.instances_in_vpc)
