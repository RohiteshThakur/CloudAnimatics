#!/usr/bin/python3

 
import json
from collections import OrderedDict
import sys
import subprocess
import re
import os

#import param_parser

## Another json parser to checkout: https://github.com/mewwts/addict/tree/master/addict ###

####################################### Global Variables ########################################
config_file = '/home/redhat/AWS/config_data/testfile.cfg'
aws_services_full_list = '/home/redhat/AWS/aws_services.lst'


'''
AWS info:
Complete list of AWS resources: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html

'''

 


#######################      This parser reads through the json file and tries to find out the type of resource under Resources.   ####################



# Parse command line argument. The argument must be absolute path of the template file.
if (len(sys.argv) != 2):
	print ("Incorrect usage!")
	print ("usage: # <script name> <json file>")
	exit (1)
else:
	#print ("JSON to parse:", sys.argv[1])
	pass
	
"""
AWS template has two major sections: 1. Parameters and  2. Resources. 
	Parameters included AWS objects which already exisis in AWS infrastructure.
	Resources are objects which the template file will create when executed.

In order to parse these 2 sections, this program is divided in two sections but return the result in single output
"""

# Section 1 - Parse parameters section. This is done using param_parser python program which is coded separately and this programs call it. The same template file is passed as agrument.

#cwd = os.getcwd()
#cwd = os.path.realpath('.')
pathname = os.path.dirname(sys.argv[0]) 
dirname = os.path.abspath(pathname)
param_parser = (dirname + "/param_parser.py")
#print (param_parser)
arg = sys.argv[1]
#os.system(python3 param_parser sys.argv[1])
# subprocess.call(param_parser arg)
subprocess.call("{0} {1}".format(param_parser, arg), shell=True)							# Example of Variable substitution when method expects Absolute names

# Section 1 - Ends.


'''
try:
    with open('/home/redhat/AWS/sample_templates/RDS_MySQL_With_Read_Replica.template', 'r') as js:
        data = (json.load(js, object_pairs_hook=OrderedDict))
'''
    

# Section 2 - Parse resource section.

# Open the sample.json file.

try:
	#with open('EB_in_VPC_template', 'r') as js:																					#-> Works
	#with open('/home/redhat/AWS/sample_templates/VPC_multiAZ_template', 'r') as js:												#-> This file doesn't stick to AWS template. Non standard.
	#with open('/home/redhat/AWS/sample_templates/ElasticBeanstalk_in_VPC.template', 'r') as js:									#-> Works.
	#with open('/home/redhat/AWS/sample_templates/AutoScalingMultiAZWithNotifications.template', 'r') as js:						#-> Works.
	#with open('/home/redhat/AWS/sample_templates/VPC_AutoScaling_With_Public_IPs.template', 'r') as js:							#-> Works
	#with open('/home/redhat/AWS/sample_templates/AutoScalingScheduledAction.template', 'r') as js:									#-> Works
	#with open('/home/redhat/AWS/sample_templates/ELBGuidedAutoScalingRollingUpgrade.template', 'r') as js:							#-> Works
	#with open('/home/redhat/AWS/sample_templates/Rails_Multi_AZ.template', 'r') as js:												#-> Works
	#with open('/home/redhat/AWS/sample_templates/VPC_Single_Instance_In_Subnet.template', 'r') as js:								#-> Works
	#with open('/home/redhat/AWS/sample_templates/VPC_With_PublicIPs_And_DNS.template', 'r') as js:									#-> Works
	#with open('/home/redhat/AWS/sample_templates/VPC_EC2_Instance_With_Multiple_Dynamic_IPAddresses.template', 'r') as js:
	with open ("{0}".format(arg), 'r') as js:
		data = (json.load(js, object_pairs_hook=OrderedDict))
        #data = OrderedDict(json.load(js))
        #print data

except (ValueError, KeyError, TypeError):
    print ("JSON format error")

except IOError as e:
    print ("I/O error({0}): {1}".format(e.errno, e.strerror))

except:
    print ("Unexpected error:", sys.exc_info()[0])
    raise

 
# Display the keys under "Resources"
#for k, v in data["Resources"].items():         # Does the same thing as above.
#        print k

#for k in data["Resources"]:
#       print k

# Till this point we are able to list the resources but their names can be mislesding, hence we MUST gather more information from "Type".
# Lets define a List and save those keys in there. Makes it easy to iterate.
# AWS resources in JSON file is formatted as: AWS::aws-product-name::data-type-name

 
resource_list = []
for k, v in data["Resources"].items():
    if (k):
        resource_list.append(k)

#print ("\n")


'''
for index, item in enumerate(resource_list):
    if (item):
        # We have to covert unicode to string, then split (delim set to '::') which converts it into a list. Print the last element in the list.
        # print (index,".", item, "is a", (str(data["Resources"][item]["Type"])).split("::", 2)[-1])
        print (item, (str(data["Resources"][item]["Type"])))

'''

# Create a array with each element is a combination of resources and resource types. 
res_res_type=[]
res_res_type_str=""
for item in (resource_list):
	if (item):
		res_type = (str(data["Resources"][item]["Type"]))
		#res_res_type.append("["+item+"]"+" "+ "["+res_type+"]")
		res_res_type.append(item +" "+ res_type)
		res_res_type_str += item +" "+ res_type + "\t"
        

'''
##########################################################    Do Not remove this - Very important for testing.   ##########################################################
print ("\n\nprinting [resource][resource type]")
for i in (res_res_type):
    print (i)

print (res_res_type_str)
'''

 
# Open config_file to write
#global config_file
#_file = open(config_file, 'a')

def errhandler ():
   print(item,": is not a recognized service!")




def _get_VPC ():
	if ('AWS::EC2::VPC' in item):
		#resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		#_file.write (resource_name+"\n")
		if ("Tags" in data["Resources"][resource_name]["Properties"]):
			vpc = (resource_name + "|" + resource_type + "|" + "StackID:" + (data["Resources"][resource_name]["Properties"]["Tags"][0]["Value"]["Ref"]))
		else:
			vpc = (resource_name + "|" + resource_type)
		print (vpc)

def _get_VPC_StackID ():
    
    #This function collects details of each VPC found in AWS template and feeds simplified data to config_file
    
    #global config_file
    #with open (config_file, 'w') as _file:
    if ("VPC" in data["Resources"]):									# This is going to Bite me back!!!
        if (data["Resources"]["VPC"]["Type"] == "AWS::EC2::VPC"):
            # Gather Stack ID of the VPC, that forms the pillar for one particular stack.
            #config_file.write(data["Resources"]["VPC"]["Type"]
            #_file.write (data["Resources"]["VPC"]["Properties"]["Tags"][0]["Value"]["Ref"]+"\n")
            print (data["Resources"]["VPC"]["Properties"]["Tags"][0]["Value"]["Ref"]+"\n")

def _get_Subnet (): 
	#for item in (res_res_type):
	if ("AWS::EC2::Subnet" in item):		
		#resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		#print ("\n\n", resource_name)
		#_file.write (resource_name + ":" + data["Resources"][resource_name]["Properties"]["VpcId"]["Ref"])
		#print (resource_name + "|" + resource_type  + "|" + data["Resources"][resource_name] ["Properties"]["CidrBlock"]["Fn::FindInMap"][1] + "|" + data["Resources"][resource_name] \
		#["Properties"]["VpcId"]["Ref"])
		print (resource_name + "|" + resource_type  + "|" + data["Resources"][resource_name]["Properties"]["VpcId"]["Ref"])


def _get_subnet_nacl_assn ():
	if ("AWS::EC2::SubnetNetworkAclAssociation" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		subnetid = (data["Resources"][resource_name]["Properties"]["SubnetId"]["Ref"])
		networkaclid = (data["Resources"][resource_name]["Properties"]["NetworkAclId"]["Ref"])
		print (resource_name + "|" + resource_type + "|" + "SubnetId:" + subnetid + "|" + "NetworkAclId:" + networkaclid)


def _get_InternetGateway ():
	if ("AWS::EC2::InternetGateway" in item):
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		print (resource_name + "|" + resource_type + "|")

def _get_InternetGateway_Attachment ():
	if ("AWS::EC2::VPCGatewayAttachment" in  item):
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		print (resource_name + "|" + resource_type + "|" + data["Resources"][resource_name]["Properties"]["VpcId"]["Ref"])

def _get_RouteTable ():
	if ("AWS::EC2::RouteTable" in item):
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		print (resource_name + "|" + resource_type + "|" + data["Resources"][resource_name]["Properties"]["VpcId"]["Ref"])
	
def _get_Route ():
	if ("AWS::EC2::Route" in item):
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		routetable_str = resource_name + "|" + resource_type + "|"
		for i in data["Resources"][resource_name].items():
			if ("DependsOn" in i):
				routetable_str += "DependsOn:" + data["Resources"][resource_name]["DependsOn"] + "|" + "GatewayId:" + data["Resources"][resource_name]["Properties"]["GatewayId"]["Ref"] + "|"	
				#print (routetable_str)
			
		rtid = data["Resources"][resource_name]["Properties"]["RouteTableId"]["Ref"]
		routetable_str += rtid
		print (routetable_str)


def _get_Route_Assn ():
	if ("AWS::EC2::SubnetRouteTableAssociation" in item):
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		route_assn = resource_name + "|" + resource_type + "|" + data["Resources"][resource_name]["Properties"]["SubnetId"]["Ref"] + "|" + data["Resources"][resource_name]["Properties"] \
		["RouteTableId"]["Ref"]
		print (route_assn)

def _get_NetworkAcl ():
	if ("AWS::EC2::NetworkAcl" in item):
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		if ("VpcId" in data["Resources"][resource_name]["Properties"]):
			vpc_id = data["Resources"][resource_name]["Properties"]["VpcId"]["Ref"]
		if (isinstance(data["Resources"][resource_name]["Properties"]["Tags"][0]["Value"], OrderedDict)):
			stack_id = data["Resources"][resource_name]["Properties"]["Tags"][0]["Value"]["Ref"]
		else:
			stack_id = data["Resources"][resource_name]["Properties"]["Tags"][0]["Value"]

		#nacl = resource_name + "|" + resource_type + "|" + data["Resources"][resource_name]["Properties"]["VpcId"]["Ref"] + "|" + data["Resources"][resource_name]["Properties"]["Tags"][0]["Value"]
		nacl = resource_name + "|" + resource_type + "|" + vpc_id + "|" + stack_id
		print (nacl)


def _get_ElasticIP ():
	if ("AWS::EC2::EIP" in  item):
		resource_name, resource_type = str(item).split(" ")[0], str(item).split(" ")[-1]
		for i in data["Resources"][resource_name].items():
			if ("DependsOn" in i):
				eip = resource_name + "|" + resource_type + "|" + "DependsOn:" + data["Resources"][resource_name]["DependsOn"] + "|" + "Attachedto:" + data["Resources"][resource_name] \
				["Properties"]["InstanceId"]["Ref"] + "|" + "Domain:" + data["Resources"][resource_name]["Properties"]["Domain"]
				print (eip)

def _get_Instances ():
	if (('AWS::EC2::Instance' in item) and ('NATDevice' not in item) and ('BastionHost' not in item)):
		# If we have reached here, that means the stack contains at least one EC2 instance. This one counts in which subnet each one belongs to.
		# Also 1 Subnet = 1 AZ. If we find EC2 instances part of more than one subnet - Won't work.
		'''
		Sometimes we will encounter EC2 instances with a Network Interface attached, having no explicit stanza for "Security Groups" - Which is an important entity.
        In that case it becomes imperative to parse, Network Interface stanza, to search for Security Groups. Basically, now we have an additional component on top of EC2, which maps itsself
		to Security Groups. 
		Understanding the mapping: 
		A single EC2 instance can be a part of more than one Network instances.
		A single EC2 instance can be a part of more than one Security Group. - That's why 
		A Single Network Interface can be a part of more than one Security Group. - That's why this program assumes Network Interfaces as a List.
		'''
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		#resource_name = "WebServerInstance"
		#print ("\n\n\n")
		#print ((resource_name + "|" + resource_type + ":" + data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][0]["SubnetId"]["Ref"]+"\n"))
		Sec_Group_Set = Subnet_Id = Interface_Name = Ec2_NI = Ec2_SG = Ebs_Device = ""
		for prop_list in (data["Resources"][resource_name]["Properties"].items()):
			if ("NetworkInterfaces" in prop_list):
				if (isinstance(data["Resources"][resource_name]["Properties"]["NetworkInterfaces"], list)):
					for ni in range(len(data["Resources"][resource_name]["Properties"]["NetworkInterfaces"])):
						if ("GroupSet" in data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][ni]):
							for gs in range(len(data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][ni]["GroupSet"])):
								Sec_Group_Set += data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][ni]["GroupSet"][gs]["Ref"] + " "
							#print (Sec_Group_Set)
						if ("SubnetId" in data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][ni]):
							Subnet_Id = data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][ni]["SubnetId"]["Ref"] + " "
							#print (Subnet_Id)
						if ("NetworkInterfaceId" in data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][ni]):
							Interface_Name += data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][ni]["NetworkInterfaceId"]["Ref"] + " "
							#print (Interface_Name)				    
						
						Ec2_NI += "NetworkInterfaces" + str(ni) + ":" + Sec_Group_Set + "," + Subnet_Id + "," + Interface_Name + " "
				#print (Ec2_NI)
				#print (type(data["Resources"][resource_name]["Properties"]["NetworkInterfaces"]))
				#EC2_NI = (data["Resources"][resource_name]["Properties"]["NetworkInterfaces"][0]["Ref"])

			if ("SecurityGroups" in prop_list):
				for sg_count in range(len(data["Resources"][resource_name]["Properties"]["SecurityGroups"])):
					Ec2_SG += (data["Resources"][resource_name]["Properties"]["SecurityGroups"][sg_count]["Ref"]) + "|"
			else:
				Ec2_SG = " "

			if ("BlockDeviceMappings" in prop_list):
				for ebs_count in range(len(data["Resources"][resource_name]["Properties"]["BlockDeviceMappings"])):
					Ebs_Device += (data["Resources"][resource_name]["Properties"]["BlockDeviceMappings"][ebs_count]["DeviceName"]) + "|"				
			else:
				Ebs_Device = " "
		
		print (resource_name + "|" + resource_type + "|" + Ec2_NI + "|" + Ec2_SG + "|" + Ebs_Device)
                
	if ('NATDevice' in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		nd = (resource_name + "|" + resource_type + "|" + "Subnet:" + data["Resources"][resource_name]["Properties"]["SubnetId"]["Ref"] + "|" + "SecurityGroups:" + data["Resources"] \
		[resource_name]["Properties"]["SecurityGroupIds"][0]["Ref"])
		print (nd)
                
	if ('BastionHost' in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		bh = (resource_name + "|" + resource_type + "|" + "Subnet:" + data["Resources"][resource_name]["Properties"]["SubnetId"]["Ref"] + "|" + "SecurityGroups:" + data["Resources"] \
		[resource_name]["Properties"]["SecurityGroupIds"][0]["Ref"])
		print (bh)


def _get_Security_Group ():
	if ("AWS::EC2::SecurityGroup" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		if ("VpcId" in data["Resources"][resource_name]["Properties"]):
			sg = (resource_name + "|" + resource_type + "|" + "VPC:" + data["Resources"][resource_name]["Properties"]["VpcId"]["Ref"])
			print (sg)
		#if ("SourceSecurityGroupName" in data["Resources"][resource_name]["Properties"]["SecurityGroupIngress"]):
		#	sg = (resource_name + "|" + resource_type + "|" + data["Resources"][resource_name]["Properties"]["SecurityGroupIngress"][0]["SourceSecurityGroupName"]["Ref"])
		#	print (sg)


def _get_DB_Security_Group():
	if ("AWS::RDS::DBSecurityGroup" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		if ("DBSecurityGroupIngress" in data["Resources"][resource_name]["Properties"]):
			if ("EC2SecurityGroupId" in data["Resources"][resource_name]["Properties"]["DBSecurityGroupIngress"]):
				sg = (resource_name + "|" + resource_type + "|" + data["Resources"][resource_name]["Properties"]["DBSecurityGroupIngress"]["EC2SecurityGroupId"]["Ref"])
				print (sg)
			elif ("EC2SecurityGroupName" in data["Resources"][resource_name]["Properties"]["DBSecurityGroupIngress"]):
				sg = (resource_name + "|" + resource_type + "|" + data["Resources"][resource_name]["Properties"]["DBSecurityGroupIngress"]["EC2SecurityGroupName"]["Ref"])


def _get_Elastic_Beanstalk ():
	if ("AWS::ElasticBeanstalk::Application" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		ebk = (resource_name + "|" + resource_type + "|" + data["Resources"][resource_name]["Properties"]["Description"])
	
	if ("AWS::ElasticBeanstalk::Environment" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		app_name = (data["Resources"][resource_name]["Properties"]["ApplicationName"]["Ref"])
		env = (resource_name + "|" + resource_type + "|" + "ApplicationName:" + app_name + "|") 
		if ("OptionSettings" in data["Resources"][resource_name]["Properties"]):
			for i in range(len(data["Resources"][resource_name]["Properties"]["OptionSettings"])):							# Traversing an array element in JSON.
					#print (data["Resources"][resource_name]["Properties"]["OptionSettings"][i]["OptionName"])
					if ("SSHSourceRestriction" in (data["Resources"][resource_name]["Properties"]["OptionSettings"][i]["OptionName"])):
						#print (data["Resources"][resource_name]["Properties"]["OptionSettings"][i]["OptionName"], end=" ")
						#"Namespace" : "aws:autoscaling:launchconfiguration", "OptionName" : "SSHSourceRestriction", "Value" : { "Fn::Join" : [ "", ["tcp,22,22,", { "Ref" : "BastionSecurityGroup" }]]}},
						ssh_attrib_list = (data["Resources"][resource_name]["Properties"]["OptionSettings"][i]["Value"]["Fn::Join"][1])
						ssh_sg = [elem['Ref'] for elem in ssh_attrib_list if 'Ref' in elem]
						continue
						#str_ssh_sg = ""
						#str_ssh_sg = str(ssh_sg)
						#env = env + str_ssh_sg + "|"

					env += (data["Resources"][resource_name]["Properties"]["OptionSettings"][i]["OptionName"]) + ":"
					env += (data["Resources"][resource_name]["Properties"]["OptionSettings"][i]["Value"]["Ref"]) + "|"
			
		print (env)


def _get_ApplicationLBListener():
	if ("AWS::ElasticLoadBalancingV2::Listener" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		tg = (data["Resources"][resource_name]["Properties"]["DefaultActions"][0]["TargetGroupArn"]["Ref"])
		type = (data["Resources"][resource_name]["Properties"]["DefaultActions"][0]["Type"])
		arn =  (data["Resources"][resource_name]["Properties"]["LoadBalancerArn"]["Ref"])
		print (resource_name + "|" + resource_type + "|" + type + "|" + tg + "|" + arn)

 

def _get_ALBTargetGroup ():
	if ("AWS::ElasticLoadBalancingV2::TargetGroup" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		vpcid = (data["Resources"][resource_name]["Properties"]["VpcId"]["Ref"])
		print (resource_name + "|" + resource_type + "|" + vpcid)

 
def _get_AutoScalingGroup ():
	if ("AWS::AutoScaling::AutoScalingGroup" in item):
		vpczoneid =""
		tg = ""
		tgarn = ""
		asg = lcn = min = max =""
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		if ("VPCZoneIdentifier" in data["Resources"][resource_name]["Properties"]):
			if (isinstance(data["Resources"][resource_name]["Properties"]["VPCZoneIdentifier"], OrderedDict)):			# If VPCZoneIdentifier is an Orderdict. If not consider it as a List.
				asg_subnets = data["Resources"][resource_name]["Properties"]["VPCZoneIdentifier"]["Ref"]	
				for i in range(len(data["Resources"][resource_name]["Properties"]["TargetGroupARNs"])):
					tgarn = tgarn + data["Resources"][resource_name]["Properties"]["TargetGroupARNs"][i]["Ref"] + " "

				print (resource_name + "|" + resource_type + "|" + asg_subnets + "|" + tgarn)

			else:
				for i in (data["Resources"][resource_name].items()):
					if ("DependsOn" in i):
						asg = "DependsOn:" + (data["Resources"][resource_name]["DependsOn"])
						#print (data["Resources"][resource_name]["Properties"]["VPCZoneIdentifier"])

				for j in range(len(data["Resources"][resource_name]["Properties"]["VPCZoneIdentifier"])):			# When VPCZoneIdentifier is a List containing Subnets.
					vpczoneid = vpczoneid + (data["Resources"][resource_name]["Properties"]["VPCZoneIdentifier"][j]["Ref"]) + " "
					lcn = (data["Resources"][resource_name]["Properties"]["LaunchConfigurationName"]["Ref"])
					min = (data["Resources"][resource_name]["Properties"]["MinSize"])
					max = (data["Resources"][resource_name]["Properties"]["MaxSize"]) 

				for j in range(len(data["Resources"][resource_name]["Properties"]["TargetGroupARNs"])):
					tg  = tg + (data["Resources"][resource_name]["Properties"]["TargetGroupARNs"][j]["Ref"])

			print (resource_name + "|" + resource_type + "|" + "|" + asg + "|" + vpczoneid + "|" + lcn + "|" + min + "|" + max + "|" + tg)



def _get_s3_bucket():
    #'''
	#Parses S3 stanza in the template file. Returns: S3 resource name and AWS tag delimited by "|"
	#'''
	if ("AWS::S3::Bucket" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		s3_bucket = (resource_name + "|" + resource_type + "|")
		
	print (s3_bucket)		


def _get_load_balancer():
	#'''
	#Parses LoadBalancer stanza in the AWS template file. Returns: Resource name, type, subnets and security groups delimited by "|"
	#'''
	_subnets  = "Subnet:"
	_Sec_grps = "SecurityGroup:"
	if ("AWS::ElasticLoadBalancingV2::LoadBalancer" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		if (isinstance(data["Resources"][resource_name]["Properties"]["Subnets"], OrderedDict)):
			_subnets += (data["Resources"][resource_name]["Properties"]["Subnets"]["Ref"])
			#print (resource_name + "|" + resource_type + "|" + _subnets)
		else:
			if (data["Resources"][resource_name]["Properties"]["Subnets"]):
				for j in range(len(data["Resources"][resource_name]["Properties"]["Subnets"])):
					_subnets += ((data["Resources"][resource_name]["Properties"]["Subnets"][j]["Ref"] + " "))

		if ("SecurityGroups" in data["Resources"][resource_name]["Properties"]):
			if (isinstance(data["Resources"][resource_name]["Properties"]["SecurityGroups"], OrderedDict)):
				_Sec_grps += (data["Resources"][resource_name]["Properties"]["SecurityGroups"]["Ref"])
				#print (resource_name + "|" + resource_type + "|" + _Sec_grps)
			else:
				for i in range(len(data["Resources"][resource_name]["Properties"]["SecurityGroups"])):
					_Sec_grps += (data["Resources"][resource_name]["Properties"]["SecurityGroups"][i]["Ref"] + " ")
		print (resource_name + "|" + resource_type + "|" + _subnets + "|" + _Sec_grps)				


def _get_load_balancer_obsolete():
	#'''
	#Parses LoadBalancer stanza in the AWS template file. Returns: Resource name, type, subnets and security groups delimited by "|"
	#'''
	_subnets  = "Subnet:"
	_Sec_grps = "SecurityGroup:"
	if ("AWS::ElasticLoadBalancingV2::LoadBalancer" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		if (data["Resources"][resource_name]["Properties"]["Subnets"]):
			for j in range(len(data["Resources"][resource_name]["Properties"]["Subnets"])):
				_subnets += ((data["Resources"][resource_name]["Properties"]["Subnets"][j]["Ref"] + " "))

		if (data["Resources"][resource_name]["Properties"]["SecurityGroups"]):
			for i in range(len(data["Resources"][resource_name]["Properties"]["SecurityGroups"])):
				_sec_grps += (data["Resources"][resource_name]["Properties"]["Subnets"][i]["SecurityGroups"] + " ")

	print (resource_name + "|" + resource_type + "|" + _subnets + "|" + _sec_grps)


def _get_master_DB():
	'''
	#Parses Master DB stanza in AWS template. Returns:
	'''
	'''
	Learning: We know that both Master and Replica DB instance comes under same catagory of resources - "AWS::RDS::DBInstance".
	In order to make the method, differentiate between the two, make sure you when you search for unique attributes what would help method decide whether its Master or Slave,
    always traverse dictionary up to a key which is common to BOTH but their values are unique.
    For e.g. in below method, I have traversed till ..[]..[]..["Properties"] and the searched for keys which are uniq to Master and Slave. This way, method don't complain of "Keyerror" because I am
	only traversing up to a key which exists in both dictionaries of Master and Slave(i.e. ["Properties"]
	'''
	if ("AWS::RDS::DBInstance" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		# check if DB instance has a name and its multiAZ enabled. There is nothing I could find in template that will seal DB instance as a primary one. Hence I am using these two.
		if (("DBName" in data["Resources"][resource_name]["Properties"]) and ("MultiAZ" in data["Resources"][resource_name]["Properties"])):
			engine  = data["Resources"][resource_name]["Properties"]["Engine"]
			multiaz = data["Resources"][resource_name]["Properties"]["MultiAZ"]["Ref"]
			#if (data["Resources"][resource_name]["Properties"]["VPCSecurityGroups"]):
			#	vpc_sec_group = data["Resources"][resource_name]["Properties"]["VPCSecurityGroups"]["Fn::If"][0]["Is-EC2-VPC"][0]["Fn::GetAtt"][0]
			#	db_sec_group  = data["Resources"][resource_name]["Properties"]["VPCSecurityGroups"]["Fn::If"][0]["Is-EC2-Classic"][0]["Ref"]
			print (resource_name + "|" + resource_type + "|" + str(engine) + "|" + str(multiaz))

		if ("SourceDBInstanceIdentifier" in data["Resources"][resource_name]["Properties"]):
			primary_db_name = (data["Resources"][resource_name]["Properties"]["SourceDBInstanceIdentifier"]["Ref"])
			print (resource_name + "|" + resource_type + "|" + primary_db_name+"-"+"Replica")



def _get_slave_DB():
	#'''
	#Parses slave DB stanza in AWS template (Applicable when RDS is Multi-AZ enabled). Returns:
	#'''
	if ("AWS::RDS::DBInstance" in item):
		resource_name, resource_type = str(item).split(" ")[0].strip(" []"), str(item).split(" ")[-1]
		if (data["Resources"][resource_name]["Properties"]["SourceDBInstanceIdentifier"]["Ref"]):			# Check if this DB is linked to a Primary DB.
			primary_db_name = (data["Resources"][resource_name]["Properties"]["SourceDBInstanceIdentifier"]["Ref"])
			print (resource_name + "|" + resource_type + "|" + primary_db_name+"-"+"Replica")								    

  



# This stanza keeps stacking the new services as they are added.

takeaction =	{
				"VPC"							: _get_VPC, 
				"Subnet"						: _get_Subnet, 
				"InternetGateway"				: _get_InternetGateway, 
				"VPCGatewayAttachment"			: _get_InternetGateway_Attachment,
				"RouteTable"					: _get_RouteTable,
				"Route"							: _get_Route,
				"SubnetRouteTableAssociation"	: _get_Route_Assn,
				"NetworkAcl"					: _get_NetworkAcl,
				"EIP"							: _get_ElasticIP,
				"Instance"						: _get_Instances,
				"SecurityGroup"					: _get_Security_Group,
				"Environment"					: _get_Elastic_Beanstalk,
				"Listener"						: _get_ApplicationLBListener,
				"TargetGroup"					: _get_ALBTargetGroup,
				"AutoScalingGroup"				: _get_AutoScalingGroup,
				"SubnetNetworkAclAssociation"	: _get_subnet_nacl_assn,							# Make sure, there is a comma(,) in the pen-ultimate stanza.
				"Environment"					: _get_Elastic_Beanstalk,
				"Listener"						: _get_ApplicationLBListener,
				"TargetGroup"					: _get_ALBTargetGroup,
				"AutoScalingGroup"				: _get_AutoScalingGroup,
				"Bucket"						: _get_s3_bucket,
				"LoadBalancer"					: _get_load_balancer,
				"DBInstance"					: _get_master_DB,
				"DBSecurityGroup"				: _get_DB_Security_Group
				}




# Remember: IG's value must be the same as takeaction's Key. Its the value and not name of the variable that gets called!!

for item in (res_res_type):
	if (re.search (r'VPC$\b', item)):
		#print (item)
		vpc = ((item.split()[1]).split("::")[-1])
		#print (vpc)
		takeaction.get(vpc, errhandler)()
	if (re.search (r'Subnet$\b', item)):									# Match
		#print (item)
		subnet = ((item.split()[1]).split("::")[-1])
		#print (subnet)
		takeaction.get(subnet, errhandler)()
	if (re.search (r'InternetGateway\b', item)):
		IG = ((item.split()[1]).split("::")[-1])			
		#print (IG)
		takeaction.get(IG, errhandler)()
	if (re.search (r'VPCGatewayAttachment$\b', item)):									# Match
		vpcga = ((item.split()[1]).split("::")[-1])
		takeaction.get(vpcga, errhandler)()	
	if (re.search (r'RouteTable$\b', item)):
		routetable = ((item.split()[1]).split("::")[-1])
		takeaction.get(routetable, errhandler)()
	if (re.search (r'Route$\b', item)):
		rt = ((item.split()[1]).split("::")[-1])
		takeaction.get(rt, errhandler)()
	if (re.search (r'SubnetRouteTableAssociation$\b', item)):
		sassn = ((item.split()[1]).split("::")[-1])
		takeaction.get(sassn, errhandler)()
	if (re.search (r'NetworkAcl$\b', item)):
		nacl = ((item.split()[1]).split("::")[-1])
		takeaction.get(nacl, errhandler)()
	if (re.search (r'EIP$\b', item)):
		eip = ((item.split()[1]).split("::")[-1])
		takeaction.get(eip, errhandler)()
	if (re.search (r'\WInstance$\b', item)):											# Added "\W" to match non-word characters, to differentiate between "Instance" and "DBInstance"
		ins = ((item.split()[1]).split("::")[-1])
		takeaction.get(ins, errhandler)()
	if (re.search (r'\WSecurityGroup$\b', item)):										# Added "\W" to match non-word characters. To differentiate between "SG" and "DBSG"
		sg = ((item.split()[1]).split("::")[-1])
		takeaction.get(sg, errhandler)()
	if (re.search (r'DBSecurityGroup$\b', item)):
		dbsg = ((item.split()[1]).split("::")[-1])
		takeaction.get(dbsg, errhandler)()
	if (re.search (r'Environment$\b', item)):
		se = ((item.split()[1]).split("::")[-1])
		takeaction.get(se, errhandler)()
	#if (re.search (r'Listener$\b', item)):
	#	se = ((item.split()[1]).split("::")[-1])
	#	takeaction.get(se, errhandler)()
	#if (re.search (r'TargetGroup$\b', item)):
	#	se = ((item.split()[1]).split("::")[-1])
	#	takeaction.get(se, errhandler)()
	#if (re.search (r'AutoScalingGroup$\b', item)):
	#	se = ((item.split()[1]).split("::")[-1])
	#	takeaction.get(se, errhandler)()
	if (re.search (r'SubnetNetworkAclAssociation$\b', item)):
		se = ((item.split()[1]).split("::")[-1])
		takeaction.get(se, errhandler)()
	if (re.search (r'Environment$\b', item)):								# recently added.
		ebk = ((item.split()[1]).split("::")[-1])
		takeaction.get(ebk, errhandler)()
	if (re.search (r'Listener$\b', item)):
		lsnr = ((item.split()[1]).split("::")[-1])
		takeaction.get(lsnr, errhandler)()
	if (re.search (r'TargetGroup$\b', item)):
		tgp = ((item.split()[1]).split("::")[-1])
		takeaction.get(tgp, errhandler)()
	if (re.search (r'AutoScalingGroup$\b', item)):
		asg = ((item.split()[1]).split("::")[-1])
		takeaction.get(asg, errhandler)()
	if (re.search (r'Bucket$\b', item)):
		bkt = ((item.split()[1]).split("::")[-1])
		takeaction.get(bkt, errhandler)()
	if (re.search (r'LoadBalancer$\b', item)):
		lbr = ((item.split()[1]).split("::")[-1])
		takeaction.get(lbr, errhandler)()
	if (re.search (r'DBInstance$\b', item)):
		dbi = ((item.split()[1]).split("::")[-1])
		takeaction.get(dbi, errhandler)()




        













