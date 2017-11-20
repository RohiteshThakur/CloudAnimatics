#!/usr/bin/python3

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

# Parse static file.
#file_to_parse = "/home/redhat/AWS/config_data/parsedfile1.cfg"
#file_to_parse = "E:\\AWS\\My Project\\AWS_Blender_programs\\pf_VPC_With_VPN_Connection.txt"
#file_to_parse = "E:\\AWS\\My Project\\AWS_Blender_programs\\pf_VPC_AutoScaling_With_Public_IPs.txt"
#file_to_parse = "E:\\AWS\\My Project\\AWS_Blender_programs\\pf_VPC_ASG_and_ELB.txt"
file_to_parse = "E:\\AWS\\My Project\\AWS_Blender_programs\\pf_WordPress_Multi_AZ.txt"

'''
# Parse command line arguments.
if (len(sys.argv) != 2):
	print ("Incorrect usage!")
	print ("usage: # <script name> <parsed_aws_template>")
	exit (1)
else:
	#print ("JSON to parse:", sys.argv[1])
	pass

file_to_parse = sys.argv[1]
'''

'''
def _save_scene_to_file():
	# This provides blender a filepath to refer to...
	bpy.ops.wm.save_mainfile(filepath="E:\AWS\My Project\AWS_Blender_programs\My_scene.blend")



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
        self.file_handle                    = file_to_parse
        self.vpc_to_coord_map               = {}                          # Dictionary of VPC and co-ordinates.
        self.subnet_to_coord_map            = {}
        self.vpc_name                       = []                                  # List of VPCs in file.
        self.vpc_count                      = 0
        self.subnet_names                   = []
        self.subnet_name                    = []
        self.subnet_type                    = {}
        self.vpc_to_subnet_map              = {}
        self.public_stack                   = []
        self.vpc_public_stack_map           = {}
        self.private_stack                  = []
        self.vpc_private_stack_map          = {}
        self.subnet_to_instance_map         = {}
        self.subnet_to_instance_nums        = {}
        self.public_networkacl              = []
        self.private_networkacl             = []
        self.internet_gateway               = []
        self.private_instances              = []
        self.public_instances               = []
        self.securitygroups_in_vpc          = []
        self.vpc_to_securitygroup_map       = {}
        self.instances_in_vpc               = []
        self.instance_to_securitygroups_map = {}
        self.vpc_to_elastic_beanstalk_stack = {}
        self.elastic_load_balancer          = []
        self.elb_security_group             = []
        self.subnet_to_resources_map        = {}

    '''
    def return_file_handle(self, file_to_parse):
        try:
            with open (file_to_parse, 'r') as file_handle:
                return file_handle
        except FileNotFoundError:
            msg = "Sorry, the file" + file_to_parse + "does not exist."
            print (msg)
    '''

    def build_default_objects(self):
        '''
        Note: This function must be called before any other in this class.
        Reads the file and looks for VPC and Subnets/AZ in the VPC. If VPC is not found, then we generate a default VPC.
        Remember: Up on creation of any VPC, following things are created automatically:
        1. Default Network ACL (Publicly accessible if it default VPC)
        2. Default Security Security Group
        3. Default Public Route (Connected to Internet Gateway, if it default VPC)
        4. Internet Gateway (if this is a default VPC, not created in custom)
        '''
        vpc_str = sub_str = igw_str = gti_str = vga_str = rtl_str = rou_str = sra_str = acl_str = sgp_str = sna_str = ""
        # Now that the parsed file has been created, and this code reads it, we need to parse the "Subnets" coming from Parameters.
        with open(self.file_handle, "r") as fh:
            for line in fh:
                if ('AWS::EC2::VPC::Id' in line):
                    vpc = str(line).split("|")[0]
                    print(vpc)
                if ('AWS::EC2::Subnet::Id' in line):
                    subnets = str(line).split("|")[2]
                    #print (subnets)
        fh.close()

        with open(self.file_handle, "r") as fh:
            fo = fh.read()
            #print (dir(fo))
            # Note: If VPC is present in the "Resources" section of the template, that means its a custom VPC, therefore no assumption should be made.
            # Hence we only check for "VPC passedfrom parameters" or "No VPC at all".
            if (fo.find('AWS::EC2::VPC|') > 0 or fo.find('Default') > 0):
                return
            if (fo.find('AWS::EC2::VPC::Id') == -1):
                vpc_str = "DefaultVPC|AWS::EC2::VPC|\n"

            if ((fo.find('AWS::EC2::Subnet') or fo.find('AWS::EC2::Subnet::Id')) == -1):
                sub_str = "DefaultSubnet|AWS::EC2::Subnet|Public|DefaultVPC|\n"

            if (fo.find('AWS::EC2::InternetGateway') == -1 and fo.find('AWS::EC2::VPC::Id') == -1):
                igw_str = "DefaultInternetGateway|AWS::EC2::InternetGateway|DefaultVPC|\n"
            else:
                igw_str = "DefaultInternetGateway|AWS::EC2::InternetGateway|"+vpc+"|\n"

            if (fo.find('AWS::EC2::VPCGatewayAttachment') == -1 and fo.find('AWS::EC2::VPC::Id') == -1):
                gti_str = "GatewayToInternet|AWS::EC2::VPCGatewayAttachment|DefaultVPC\n"
            else:
                gti_str = "GatewayToInternet|AWS::EC2::VPCGatewayAttachment|"+vpc+"|\n"
            '''
            if(fo.find('AWS::EC2::VPCGatewayAttachment') == -1 and fo.find('AWS::EC2::VPC::Id') == -1):
                vga_str = "DefaultVPCAttachment|AWS::EC2::VPCGatewayAttachment|DefaultVPC|\n"
            else:
                vga_str = "DefaultVPCAttachment|AWS::EC2::VPCGatewayAttachment|"+vpc+"|\n"
            '''
            if (fo.find('AWS::EC2::RouteTable') == -1 and fo.find('AWS::EC2::VPC::Id') == -1):
                rtl_str = "DefaultRouteTable|AWS::EC2::RouteTable|DefaultVPC|\n"
            else:
                rtl_str = "DefaultRouteTable|AWS::EC2::RouteTable|"+vpc+"|\n"

            if (fo.find('AWS::EC2::Route') == -1 and fo.find('AWS::EC2::VPC::Id') == -1):
                rou_str = "DefaultPublicRoute|AWS::EC2::Route|DependsOn:GatewayToInternet|GatewayId:DefaultInternetGateway|DefaultRouteTable|DefaultVPC\n"
            else:
                rou_str = "DefaultPublicRoute|AWS::EC2::Route|DependsOn:GatewayToInternet|GatewayId:DefaultInternetGateway|DefaultRouteTable|"+vpc+"|\n"

            if (fo.find('AWS::EC2::SubnetRouteTableAssociation|') == -1 and fo.find('AWS::EC2::Subnet::Id') == -1):
                sra_str = "DefaultSubnetRouteTableAssociation|AWS::EC2::SubnetRouteTableAssociation|DefaultSubnet|DefaultRouteTable\n"
            elif(fo.find('AWS::EC2::Subnet::Id') > 0):
                sra_str = "DefaultSubnetRouteTableAssociation|AWS::EC2::SubnetRouteTableAssociation|"+subnets+"|DefaultRouteTable\n"

            if (fo.find('AWS::EC2::NetworkAcl') == -1 and fo.find('AWS::EC2::VPC::Id') == -1):
                acl_str = "DefaultNetworkACL|AWS::EC2::NetworkAcl|DefaultVPC|\n"
            else:
                acl_str = "DefaultNetworkACL|AWS::EC2::NetworkAcl|"+vpc+"|\n"

            if (fo.find('AWS::EC2::SubnetNetworkAclAssociation') == -1 and fo.find('AWS::EC2::VPC::Id') == -1):
                sna_str = "DefaultSubnetNetworkAclAssociation|AWS::EC2::SubnetNetworkAclAssociation|SubnetId:DefaultSubnet|NetworkAclId:DefaultNetworkACL\n"
            else:
                sna_str = "DefaultSubnetNetworkAclAssociation|AWS::EC2::SubnetNetworkAclAssociation|SubnetId:"+subnets+"|NetworkAclId:DefaultNetworkACL\n"

            if (fo.find('AWS::EC2::SecurityGroup') == -1 and fo.find('AWS::EC2::VPC::Id') == -1):
                sgp_str = "DefaultSecurityGroup|AWS::EC2::SecurityGroup|DefaultVPC|\n"
            elif(fo.find('AWS::EC2::SecurityGroup') == -1):
                sgp_str = "DefaultSecurityGroup|AWS::EC2::SecurityGroup|"+vpc+"|\n"
            #print (vpc_str, sub_str, igw_str, vga_str, rou_str, acl_str)


        fh.close()
        with open(self.file_handle, "a") as fh:
            fh.write(vpc_str)
            fh.write(sub_str)
            fh.write(igw_str)
            fh.write(gti_str)
            #fh.write(vga_str)
            fh.write(rtl_str)
            fh.write(rou_str)
            fh.write(sra_str)
            fh.write(acl_str)
            fh.write(sna_str)
            fh.write(sgp_str)
        fh.close()

        '''
            for line in fh:
                print(line)
                if not ("AWS::EC2::VPC|" in line):
                    # If VPC is not found then neither "Parameters" and "Resources" contains VPC. So we define a default one.
                    fh.write("DefaultVPC|AWS::EC2::VPC|")
                if not ("AWS::EC2::Subnet|" in line):
                    # If not subnet defined inside the VPC, insert a default one.
                    fh.write("DefaultSubnet|AWS::EC2::Subnet|")               # All Subnets in Default VPC are public. Since, in this case VPC wasn't present we assume there is atleast on Subnet.
                    #print (self.subnet_names)
                if not ("AWS::EC2::InternetGateway|" iin line):
                    # Default VPC is publicly accessible, so we need to insert one.
                    fh.write("DefaultInternetGateway|AWS::EC2::InternetGateway|")
                if not ("AWS::EC2::VPCGatewayAttachment|" in line):
                    # Since default VPC is publicly accessible, VPC must remain attached to InternetGateway via GatewayAttachment.
                    fh.write("DefaultVPCAttachment|AWS::EC2::VPCGatewayAttachment|")
                if not ("AWS::EC2::Route" in line):
                    # Route in Default VPC connects InternetGateway and Subnet. That make subnet publicly accessible
                    fh.write("DefaultPublicRoute|AWS::EC2::Route|")
                if not ("AWS::EC2::NetworkAcl" in  line):
                    # NetworkACL have rules allowing In-gress and E-gress traffic.
                    fh.write("DefaultNetoworkACL|AWS::EC2::NetworkAcl")
        fh.close()
        with open(self.file_handle, "r") as fh:
            for line in fh:
                print (line)

        ########################

            for line in fh:
                if not ("AWS::EC2::VPC|" in line and "AWS::EC2::Subnet|" in line and "AWS::EC2::InternetGateway|" in line and "AWS::EC2::VPCGatewayAttachment|" in line and "AWS::EC2::Route" in line and "AWS::EC2::NetworkAcl" in line):

            fh.close()
            with open(self.file_handle, "a") as fh:
                fh.write("DefaultVPC|AWS::EC2::VPC|\n")
                fh.write("DefaultSubnet|AWS::EC2::Subnet|\n")
                fh.write("DefaultInternetGateway|AWS::EC2::InternetGateway|\n")
                fh.write("DefaultVPCAttachment|AWS::EC2::VPCGatewayAttachment|\n")
                fh.write("DefaultPublicRoute|AWS::EC2::Route|\n")
                fh.write("DefaultNetoworkACL|AWS::EC2::NetworkAcl|\n")
        '''


    def count_vpc(self):
        '''Parse simplified file and return co-ordinates as a list.'''
        with open(self.file_handle, 'r') as fh:
            for line in fh:
                # print(line)
                if (("AWS::EC2::VPC|" in line) or ("AWS::EC2::VPC::Id" in line)):
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
        This method parses each VPC in file and returns subnets in each VPC in form of dictionary.
        This method parsed
        '''
        subnet_name = vpc = ""
        # print(self.vpc_name)
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")                # Built a regex to make it uniq.
            # print(uniq_vpc)
            with open(self.file_handle, 'r') as fh:
                for line in fh:
                    #print (line)
                    if ("AWS::EC2::Subnet|" in line and re.search(uniq_vpc, line)): # This means the line containing subnet must also contain the "VPC" its in.
                        # self.subnet_names.append(str(line.split("|", 1)[0]))
                        subnet_name = (str(line.split("|", 1)[0]))
                        #print (subnet_name)
                        self.subnet_names.append(subnet_name)
                    elif ("AWS::EC2::Subnet::Id" in line):
                        subnet_list = (str(line.split("|")[2]))        # Parse Subnet(s) from last column from Param's subnet line.
                        subnet_name = str(subnet_list).split()          # Since subnets are delimited by " ", split them and form a list.
                        #print (subnet_nam)
                        self.subnet_names.extend(subnet_name)
                        #print (self.subnet_names)

        #if (len(self.subnet_names) == 0):           # i.e no subnet found in parsed AWS template.
            # Assign a subnet, as AWS creates a default public subnet up on account creation.
            #subnet_name = "DefaultSubnet"
            #self.subnet_names.append(subnet_name)

        self.vpc_to_subnet_map[vpc] = list(set(self.subnet_names))
        #fh.close()
        # self.subnet_names.append(subnet_names)

        # print(self.subnet_names)
        # print(end='\n')
        # print(self.subnet_names)
        #fh.close()
        return self.vpc_to_subnet_map

    def subnet_to_type_map(self):
        subnet = ""
        subnets = []
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")                # Built a regex to make it uniq.
            # print(uniq_vpc)
            with open(self.file_handle, 'r') as fh:
                for line in fh:
                    if ("AWS::EC2::Subnet::Id" in line):
                        subnets = (str(line.split("|")[2])).split()
                        #print (subnets)
                        for i in range(len(subnets)):
                            self.subnet_type[subnets[i]] = (str(line.split("|")[3]))             # Pick up the word "Public" by parsing.
                            #print (self.subnet_type[subnets[i]])

                    if ("AWS::EC2::Subnet|" in line):
                        self.subnet_type[(str(line.split("|")[0]))] = (str(line.split("|")[2]))

            fh.close()
        return (self.subnet_type)


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
            fh.close()
        # print(self.securitygroups)
        #fh.close()
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
        beanstalk_vpc = ""
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
        #fh.close()
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

        #fh.close()
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

        In case, VPC is not created, this functions assumes presense of defaultVPC and defaultSubnet. This is true because, post sign-up
        Amazon creates a publicly accessible DefaultVPC. With VPC, comes SecurityGroups, NetworkACL and a routetable - (created automatically)
        So, if VPC is not found in the template, A public VPC comprising above objects will created.

        This function builds: [Key:VPC]: value[Internet Gateway, Gateway Attachment, Route, [Network ACLs], Subnets Associated to Route]

        A Note on App Load Balancer(ALB): In available templates, I have not encountered ALB to Private Subnet mapping. There is no mention of "public or private" in parameters stanza as well.
        Therefore, this program assumes Subnets connect with ALB are public.
        '''
        vpn_gateway = public_networkacl = gateway = connected_route = route_table = elb = elbsgs =""
        public_subnet = public_subnets_to_route = subnets = networkacl = subnets_in_elb = []
        networkacllist = []
        if ('DefaultVPC' in self.vpc_name):
            vpc = 'DefaultVPC'
            self.internet_gateway = "DefaultInternetGateway"
            gateway = "AttachedtoGateway"
            connected_route = "DefaultRouteTable"
            self.public_networkacl = ["DefaultPublicNetworkACL"]
            public_subnets_to_route = self.subnet_names
            self.vpc_public_stack_map[vpc] = [self.internet_gateway, gateway, connected_route, self.public_networkacl, public_subnets_to_route]
            return self.vpc_public_stack_map


        for vpc in self.vpc_name:
            for subnet in self.subnet_names:
                uniq_vpc = (r"\b" + vpc + r"\b")
                with open(self.file_handle, 'r') as fh:
                    for line in fh:
                        if ("AWS::EC2::InternetGateway|" in line):                      # only one per VPC
                            self.internet_gateway = (str(line.split("|", 1)[0]))
                        if ("AWS::EC2::VPNGateway" in line):
                            vpn_gateway = (str(line.split("|")[0]))
                        if ("AWS::EC2::VPCGatewayAttachment" in line and re.search(uniq_vpc, line)):
                            if (len(vpn_gateway) == 0):
                                gateway = (str(line.split("|", 1)[0]))
                                #print (gateway)
                        #...And then we have a route connected to InternetGateway, thats definitely Public.
                        #if ("AWS::EC2::Route|" in line and "|DependsOn:" + gateway + "|GatewayId:" + str(self.internet_gateway) + "|" in line):
                        if ("AWS::EC2::Route|" in line and bool(self.internet_gateway) and str(self.internet_gateway) + "|" in line):
                            connected_route = str(line.split("|", 1)[0])
                            #print (connected_route)
                            route_table = str(line.split("|",)[4])
                        #...
                        if ("AWS::EC2::SubnetRouteTableAssociation" in line and bool(route_table) and route_table in line):
                            public_subnet = (str(line).split("|",)[2]).split()
                            public_subnets_to_route.extend(public_subnet)
                            temp_list = []
                            i = 0
                            if (subnets_in_elb):
                                for i in range(len(subnets_in_elb)):
                                    if (subnets_in_elb[i] in public_subnets_to_route):
                                        temp_list.append(subnets_in_elb[i])
                                #print (temp_list, subnets_in_elb)
                                if (temp_list == subnets_in_elb):
                                    self.elastic_load_balancer.append("SecGrp:"+elbsgs)
                                    self.elastic_load_balancer.append("ELB:"+elb)
                                    #print (self.elastic_load_balancer)

                        '''
                        # Make a list because a VPC can contain more than on subnets.
                        if ("AWS::EC2::NetworkAcl" in line and re.search(uniq_vpc, line) and "Public" in line):
                            public_networkacl = (str(line.split("|", 1)[0]))
                            self.public_networkacl.append(public_networkacl)
                        '''
                        '''
                        This function maps NetworkACL with Public subnets only. This is a two stage process because,
                        "SubnetNetworkAclAssociation" attribute maps only to "Subnet(s)" and not "public/private" qualifier. Therefore,
                        catagorizing NetworkACL as Public or Private is two stage process.
                        Step One - Map NetworkACL with Subnet.
                        Step two - Iterate over Subnet to Type mapping to check whether subnet is private or public.

                        Since a single NetworkACL can serve more than one subnets, We remove duplicates using set().
                        '''
                        if ("AWS::EC2::SubnetNetworkAclAssociation" in line):
                            subnets = (str(line.split("|")[2])).split(":")[-1].split()
                            public_networkacl = (str(line.split("|")[-1])).split(":")[-1].rstrip('\n')
                            for i in range(len(subnets)):
                                #print(self.subnet_type[subnets[i]])
                                if ('Public' in self.subnet_type[subnets[i]]):
                                    networkacllist.append(public_networkacl)
                                    continue
                                    #print (self.public_networkacl)
                                elif (self.subnet_type[subnets[i]] in public_subnets_to_route):
                                    networkacllist.append(public_networkacl)

                            self.public_networkacl = list(set(networkacllist))

                        if ("AWS::ElasticLoadBalancingV2::LoadBalancer" in line):
                            if (public_subnets_to_route):
                                for j in range(len(public_subnets_to_route)):
                                    if (public_subnets_to_route[j] in line):
                                        elbsgs = (str(line.split("|")[-2]).split(":")[-1].rstrip())
                                        #print (elbsgs)
                                        elb = (str(line.split("|", 1)[0]))
                                        if (elbsgs != ""):
                                            self.elastic_load_balancer.append("SecGrp:"+elbsgs)
                                        if (elb !=""):
                                            self.elastic_load_balancer.append("ELB:"+elb)
                                        #print (self.elastic_load_balancer)
                            else:
                                # These values are used in "SubnetRouteTableAssociation" section. Just to ensure ELB is taken into account if its encountered before Subnets line.
                                subnets_in_elb = str(line.split("|")[2]).split()
                                elbsgs = (str(line.split("|")[-2]).split(":")[-1].rstrip())
                                elb = (str(line.split("|", 1)[0]))


                self.public_stack = [self.internet_gateway, gateway,
                                     connected_route, self.public_networkacl, sorted(list(set(self.elastic_load_balancer))), public_subnets_to_route]
                self.vpc_public_stack_map[vpc] = self.public_stack
                return self.vpc_public_stack_map
                fh.close()

    def vpc_private_stack(self):
        '''
        Gathers VPC components which are in private subnet.
        '''
        # local variables
        if ('DefaultVPC' in self.vpc_name):                         # A DefaultVPC will mean that infrastructure has AWS Public stack only.
            return

        route_table = private_route = private_route_table = private_subnet = private_tag = private_networkacl = vpn_gateway = customer_gateway = vpn_connection = vpc_vpn_attachment = ""
        private_subnets_to_route = subnets_to_nacl = []

        # If a custom VPC exists (aka, VPC in Resources section of template), We build this stack.
        # For VPC in Parameters and templates where VPC is missing altogether, this code treats them as Public.
        # NOTE: Order to be followed: RouteTable OR Route and then SubnetRouteTableAssociation
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")
            with open(self.file_handle, 'r') as fh:
                for line in fh:
                    #print(line)
                    # Since no details of subnets is provided in Parammeters stanza, its assumed the VPC/Subnets are publicly accessible.
                    if ("AWS::EC2::VPC::Id" in line):
                        fh.close()
                        return
                    if ('AWS::EC2::VPNGateway' in line):
                        vpn_gateway = str(line.split("|")[0])
                        #print (vpn_gateway)
                    if ('AWS::EC2::CustomerGateway' in line):
                        customer_gateway = str(line.split("|")[0])
                    if ('AWS::EC2::VPCGatewayAttachment' in line and uniq_vpc in line and vpn_gateway in line):
                        vpc_vpn_attachment = str(line.split("|")[0])
                    if ('AWS::EC2::VPNConnection' in line and vpn_gateway in line and customer_gateway in line):
                        vpn_connection = str(line.split("|")[0])
                    # Note: A private leg, the stack begins with a private route and so on....except when we have a VPN connection.
                    #if ("AWS::EC2::RouteTable|" in line):
                    #    route_table = str(line.split("|", 1)[0]).strip()
                    if ("AWS::EC2::Route|" in line and bool(self.internet_gateway) and str(self.internet_gateway) not in line):
                        #print ("------------------")
                        private_route = str(line.split("|", 1)[0])
                        private_route_table = str(line.split("|")[-1])
                        #private_route_table = route_table
                        #print(private_route, private_route_table)
                        #print ("------------------")
                    elif ("AWS::EC2::Route|" in line and bool(vpn_gateway) and vpn_gateway in line):  # Here we assume that Hybrid cloud has only one way out i.e. To On-prem DC.
                        private_route = str(line.split("|", 1)[0])
                        private_route_table = str(line.split("|")[-1])
                        #print(private_route_table + "===============")
                    if ("AWS::EC2::SubnetRouteTableAssociation" in line and bool(private_route_table) and private_route_table in line):
                        #print (private_route_table + "--------")
                        private_subnet = str(line.split("|")[2])
                        private_subnets_to_route.append(private_subnet)
                        #print (private_subnet, private_subnets_to_route)
                        #print (private_route_table + "--------")
                    if ("AWS::EC2::Subnet" in line and "|Private|" in line):
                        private_tag = str(line.split("|")[2])
                    if ('AWS::EC2::SubnetNetworkAclAssociation' in line):
                        subnets_to_nacl = [sub_net for sub_net in (private_subnets_to_route) if sub_net in line]
                        if (subnets_to_nacl):
                            self.private_networkacl = (str(line.split("|")[-1]).split(":", 1)[-1].split())
                            #self.private_networkacl.append(private_networkacl)
                    '''
                    if ("AWS::EC2::NetworkAcl" in line):
                        private_networkacl = (str(line.split("|", 1)[0]))
                        print (private_networkacl)
                    '''

                    '''
                        # print(private_networkacl)
                    elif ("AWS::EC2::NetworkAcl" not in line and not (re.search(uniq_vpc, line))):
                        # No private subnet in the VPC.
                        self.private_stack = []
                    '''

            self.private_stack = [customer_gateway, vpn_connection, vpn_gateway, private_route, self.private_networkacl, private_subnets_to_route]
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
            if (subnet_count == 1):
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


    def autoscalinggrp_to_subnet():
        '''
        Returns ASG to Subnet Mapping.
        Note: ASG can be located within Subnet with Number of subnets in VPC is just one. Outside VPC when Subnets mapped is
              more than one.
        '''

    def resources_in_subnet(self):
        '''
        This method parses the file and considers every resources that gets configured within a Subnet.
        '''
        subnet_to_resources = []
        asg = dbs = dbi = ins = esg = esg_pair = ""
        for vpc in self.vpc_name:
            uniq_vpc = (r"\b" + vpc + r"\b")
            for subnet in self.subnet_names:
                if ("DefaultSubnet" in subnet):
                    with open(self.file_handle, 'r') as fh:
                        for line in fh:
                            if ("AWS::AutoScaling::AutoScalingGroup" in line):
                                asg = ("AutoScalingGroup:"+str(line).split("|")[0])
                            if ("AWS::RDS::DBSecurityGroup" in line):
                                dbs = ("DBSecurityGroup:"+str(line).split("|")[0])
                            if ("AWS::RDS::DBInstance" in line):
                                dbi = ("DBInstance:"+str(line).split("|")[0]+","+str(line).split("|")[-1].rstrip('\n'))
                            if ("AWS::EC2::Instance" in line):
                                ins = ("Instance:"+str(line).split("|")[0])
                            if ("AWS::EC2::SecurityGroup" in line):
                                esg = ("SecurityGroup:"+str(line).split("|")[0])

                        if (asg == ""):
                            esg_pair = esg+","+ins
                        else:
                            esg_pair = esg+","+asg

                        subnet_to_resources = [dbi, dbs, esg_pair]
                        self.subnet_to_resources_map[subnet] = subnet_to_resources
                        #return (self.subnet_to_resources_map)
                else:
                    with open(self.file_handle, 'r') as fh:
                        for line in fh:
                            if ("AWS::AutoScaling::AutoScalingGroup" in line):
                                asg = ("AutoScalingGroup:"+str(line).split("|")[0])
                            if ("AWS::RDS::DBSecurityGroup" in line):
                                dbs = ("DBSecurityGroup:"+str(line).split("|")[0])
                            if ("AWS::RDS::DBInstance" in line):
                                dbi = ("DBInstance:"+str(line).split("|")[0]+","+str(line).split("|")[-1].rstrip('\n'))
                            if ("AWS::EC2::Instance" in line):
                                ins = ("Instance:"+str(line).split("|")[0])
                            if ("AWS::EC2::SecurityGroup" in line):
                                esg = ("SecurityGroup:"+str(line).split("|")[0])

                        if (asg == ""):
                            esg_pair = esg+","+ins
                        else:
                            esg_pair = esg+","+asg

                        subnet_to_resources = [dbi, dbs, esg_pair]
                        self.subnet_to_resources_map[subnet] = subnet_to_resources
                        #return (self.subnet_to_resources_map)

            return self.subnet_to_resources_map




if __name__ == "__main__":
    cvpc = Location_Engine(file_to_parse)
    # lst = cvpc.count_vpc("E:\AWS\Blender files\parsed_file.txt")
    cvpc.build_default_objects()

    lst = cvpc.count_vpc()
    print(lst)


    sub = cvpc.vpc_to_subnet()
    print(sub)

    cvpc.subnet_to_type_map()
    print (cvpc.subnet_type)

    igvpc = cvpc.vpc_public_stack()
    print(igvpc)

    vpcsg = cvpc.vpc_to_securitygroup()
    print(vpcsg)


    #vtobk = cvpc.vpc_to_elasticbeanstalk()
    #print (vtobk)


    pvpc = cvpc.vpc_private_stack()
    print(pvpc)

    #stoi = cvpc.subnet_to_instance()
    #print(stoi)



    #stoi = cvpc.subnet_to_instance()
    #print(stoi)

    # print(end='\n')
    itosg = cvpc.instance_to_securitygroups()
    print(itosg)


    submap = cvpc.locate_object_offsets()
    print(submap)


    #print (cvpc.subnet_to_instance_nums)
    #print (cvpc.instances_in_vpc)

    cvpc.resources_in_subnet()
    print (cvpc.subnet_to_resources_map)
