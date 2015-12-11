#! /usr/bin/env python

#Automatically build a table (with all the variables) in opal based on the
#i2b2 structure. The assumption is that opal project already exists.

__author__ = "Olly Butters"
__date__ = 11/12/15

import csv
import json
import os

opal_address = '192.168.56.100:8080' #opal IP address
opal_username = 'administrator'      #opal username for this project
opal_password = 'password'           #opal password for above username
opal_project = 'i2b2'                #opal project that tables get put into - this must already exist
i2b2_ontology_file = 'i2b2_ont.csv'  #input i2b2 ontology file

#Make a temp directory to put all the temp JSON and CSV files.
#os.mkdir('temp')
root_dir = os.getcwd()


#####################################################
#Read in the data from the i2b2 export file and store it in some lists.
#####################################################
label = []
snomed = []
valuetype = []

#read in the i2b2 dd and munge it.
with open(i2b2_ontology_file, 'r') as i2b2_file:
    i2b2_ont = csv.reader(i2b2_file, delimiter=';')
    for row in i2b2_ont:
	label.append(row[2])
	snomed.append(row[6])
	valuetype.append(row[11])

#Get rid of the first couple of rows from each.
label.pop(0)
snomed.pop(0)
valuetype.pop(0)
label.pop(0)
snomed.pop(0)
valuetype.pop(0)




########################
#Set up the table first
print 'Setting up the table'

table_name = 'i2b2_import'

#Table definition
this_table_dic = {'entityType': 'Patient', 'name': table_name}

#save it as a json file
this_table_json_name = 'temp/'+table_name+'_table.json'
with open(this_table_json_name, 'w') as fp:
    json.dump(this_table_dic, fp, indent=4)

#Push the above json file into the opal API, this will make an empty table i.e. no variables.
cmd = 'opal rest -o http://'+opal_address+' --user '+opal_username+' --password '+opal_password+' -m POST -ct "application/json" /datasource/'+opal_project+'/tables < temp/'+table_name+'_table.json'
#print cmd
os.system(cmd)


#######################
#Now do the variables
print 'Setting up the variables'
all_vars=[]
for i in range(0, len(label)):
    name='i2b2_'+str(i)

    this_var = {
    "name": snomed[i],
    "entityType": "Patient",
    "valueType": "text",
    "isRepeatable": False,
    "index": 1,
    "attributes": [
    {
        "name": "label",
        "value": label[i],
        "locale": "en"
    },
    {
        "name": "snomed",
        "value": snomed[i],
        "locale": "en"
    }
    ]
    }

    all_vars.append(this_var)

#save it as a json file
this_variable_json_name = 'temp/'+table_name+'_vars.json'
with open(this_variable_json_name, 'w') as fp:
    json.dump(all_vars, fp)

cmd = 'opal rest -o http://'+opal_address+' --user '+opal_username+' --password '+opal_password+' -m POST -ct "application/json" /datasource/'+opal_project+'/table/'+table_name+'/variables < '+this_variable_json_name
os.system(cmd)
