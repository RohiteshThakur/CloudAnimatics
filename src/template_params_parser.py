#!/usr/bin/python3

 
#########################################################################################################################################
#	Notes: This code works in conjunction with and gets called by AWS_template_parser.py.	 											#
#	This program only parses "parameters" section of template, hence a independent execution will not give full and desired results.	#
#																																		#
#	The fundamental idea behind these programs is to pick AWS objects which can be 3-dimensional'ized, so parsing every object			#
#	under "parameters" is not required. So its up to developer to choose and updated the code. So far, I have added VPC & Subnet.		#
#																																		#
#																																		#
#########################################################################################################################################


import json
from collections import OrderedDict
import sys
import subprocess
import re
 

arg = sys.argv[1]

try:
	with open ("{0}".format(arg), 'r') as js:
	#with open('/home/redhat/AWS/sample_templates/AutoScalingMultiAZWithNotifications.template', 'r') as js:
	    data = (json.load(js, object_pairs_hook=OrderedDict))

except (ValueError, KeyError, TypeError):
	print ("JSON format error")

except IOError as e:
	print ("I/O error({0}): {1}".format(e.errno, e.strerror))

except:
	print ("Unexpected error:", sys.exc_info()[0])
	raise


#print (data)
#print ("This section of script tries to parse entities which are already existing in the infrastructure and attributes of these are passed as arguments to Resources")
#print ("Since VPC and subnet are the building blocks. As of now, the script searches for both in the Parameters list")

parameters_list = []
if ("Parameters" in data.keys()):
	for k, v in data["Parameters"].items():
		if (k):
			parameters_list.append(k)
else:
	sys.exit()

#print ("\n")


param_param_type=[]
param_param_type_str=""
for parameter in (parameters_list):
	if (parameter):
		#print (parameter)
		param_type = (str(data["Parameters"][parameter]["Type"]))
		#print (param_type)
		#res_res_type.append("["+item+"]"+" "+ "["+res_type+"]")
		param_param_type.append(parameter +" "+ param_type)
		param_param_type_str += parameter +" "+ param_type + "\t"
	    
'''
print ("\n\nprinting [resource][resource type]")
for i in (param_param_type):
	print (i)

#print (res_res_type_str)

print ("\n")
'''

def _get_parameters_vpc():
	if ('AWS::EC2::VPC::Id' in parameter):
		#print (parameter)
		param_name, param_type = str(parameter).split(" ")[0], str(parameter).split(" ")[-1]
		#print (parameter_name, parameter_type)
		if (data["Parameters"]["VpcId"]["Description"].count(' ') > 1 ):						# This is just a simple hack, to substitute a VPC if template doesn't contain one.
			param_vpc = (param_name + "|" + param_type + "|" + "VPC")
		else:
			param_vpc = (param_name + "|" + param_type + "|" + (data["Parameters"][param_name]["Description"]))
		print (param_vpc)


def _get_parameters_subnets():
	subnet_list = ""
	#if ("List<AWS::EC2::Subnet::Id>" in parameter):
	if (re.search (r'List<AWS::EC2::Subnet::Id>$', parameter)):
		param_name, param_type = str(parameter).split(" ")[0], str(parameter).split(" ")[-1]
		# This object is supposed to pass a List of Subnets, so we treat "Description"'s values as a list.
		for i in range(len(data["Parameters"][param_name]["Description"])):
			subnet_list += data["Parameters"][param_name]["Description"][i]+ " " 

		param_subnets = (param_name + "|" + param_type + "|" + subnet_list)
		print (param_subnets)

	#if ("AWS::EC2::Subnet::Id" in parameter):
	if (re.search (r'AWS::EC2::Subnet::Id$', parameter)):
		param_name, param_type = str(parameter).split(" ")[0], str(parameter).split(" ")[-1]
		#print (param_name, param_type)
		if (data["Parameters"][param_name]["Description"].count(' ') > 1):						# Doh!! Same hack in action, Again!
			param_subnet = (param_name + "|" + param_type + "|" + "SUBNET")
		else:
			param_subnet = (param_name + "|" + param_type + "|" + (data["Parameters"][param_name]["Description"]))
		print (param_subnet)



def errhandler():																
	'''
	Handles exceptions when take action doesn't encounter functions for a specific parameter.
	Because this program picks up objects that can be 3-Dimensional'ized. So we pass on objects we don't need.
	'''
	print(parameter,": is not a recognized service!")
	#pass											

'''
for parameter in (param_param_type):
	if ('AWS::EC2::VPC::Id' in parameter):
		_get_parameters_vpc()
	if ("List<AWS::EC2::Subnet::Id>" in parameter):
		_get_parameters_subnets()
'''


takeaction =	{
				'VPC::Id'							: _get_parameters_vpc, 
				'Subnet::Id'						: _get_parameters_subnets
				}

#print (takeaction.get.__doc__)

for parameter in (param_param_type):
	if (re.search (r'VPC::Id$\b', parameter)):
		#print (parameter)
		vpc = str(((parameter.split()[1]).split("::", 2)[-1]))
		#print (vpc.strip())
		try:
			takeaction.get(vpc, errhandler)()
		except:
			print ("Unexpected error:", sys.exc_info()[0])
			raise

	if (re.search (r'Subnet::Id$', parameter)):									# Match subnet.
		#print (parameter)
		subnet = str(((parameter.split()[1]).split("::", 2)[-1]))
		#print (subnet.strip())
		takeaction.get(subnet, errhandler)()

	if (re.search (r'Subnet::Id>$', parameter)):								# Match list of subnets.
		#print (parameter)
		subnet = str(((parameter.split()[1]).split("::", 2)[-1])).strip('>')
		#print (subnet.strip('>'))
		takeaction.get(subnet, errhandler)()








