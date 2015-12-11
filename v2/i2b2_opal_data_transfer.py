#! /usr/bin/env python

#Upload some actual data to opal. This assumes that the table has been
#set up alrady.

__author__ = "Olly Butters"
__date__ = 11/12/15

import csv
import json
import os

opal_address = '192.168.56.100:8080' #opal IP address
opal_username = 'administrator'      #opal username for this project
opal_password = 'password'           #opal password for above username
opal_project = 'i2b2'                #opal project that tables get put into - this must already exist
opal_table_name = 'i2b2_import'
i2b2_data_file = 'sample_data/i2b2_data.csv'  #input i2b2 ontology file
temp_dir = 'temp'                    #temp dir where temp files get stored

#Make a temp directory to put all the temp JSON and CSV files.
#if not os.path.exists(temp_dir):
#    os.makedirs(temp_dir)


#with open(i2b2_data_file, 'r') as i2b2_file:
#    i2b2_data = csv.reader(i2b2_file)
#    for row in i2b2_data:
#        print row[0]

#Might have to add some munging here.

csv_data_file=i2b2_data_file

################################
#upload the data file
print 'Uploading data file'
#opal file --opal http://192.168.56.101:8080 --user administrator --password password -up hamlet.csv /home/administrator
cmd = 'opal file --opal http://'+opal_address+' --user '+opal_username+' --password '+opal_password+' -up '+csv_data_file+' /home/administrator'
os.system(cmd)

###############################
#import the data
print 'Importing the data'
#opal import-csv -o http://192.168.56.101:8080 -u administrator -p password -d bl --path /home/administrator/data.csv --type Book -v
cmd = 'opal import-csv -o http://'+opal_address+' --user '+opal_username+' --password '+opal_password+' --destination '+opal_project+' --table '+opal_table_name+' --path /home/administrator/'+os.path.basename(i2b2_data_file)+' --type Patient'
print cmd
os.system(cmd)
