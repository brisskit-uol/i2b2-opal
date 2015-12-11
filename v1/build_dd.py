#!/usr/bin/env python

#Take a dump of the i2b2 data and munge it to have it import the data dictionary into opal.
#Everything is hard coded in this, and requires the user to manually upload the
#output to the opal web interface.

#Olly Butters
#9/3/15

import csv
import xlsxwriter

#####################################################
#Read in the data from the i2b2 export file and store it in some lists.
#####################################################
label = []
snomed = []
valuetype = []

#read in the i2b2 dd and munge it.
with open('i2b2_ont.csv', 'r') as i2b2_file:
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


######################################################
#Start to build the output xlsx file
######################################################

#Define the excel file with relevent tabs
workbook = xlsxwriter.Workbook('dd.xlsx')
variables = workbook.add_worksheet('Variables')
Categories = workbook.add_worksheet('Categories')

#Define the headers
headers = (['table','name','valueType','entityType','refernceEntityType','mimeType','unit','repeatable','occurenceGroup','label:en','snomed:en'])


# Iterate over the data and write it out row by row.
col=0
for cell in (headers):
    variables.write(0, col, cell)
    col += 1

#Write the i2b2 data to the xlsx file
for i in range(0, len(label)):
    name='hack_'+str(i)
    variables.write(i+1,0,'hack') #table
    variables.write(i+1,1,name) #name
    variables.write(i+1,2,'text') #valueType
    variables.write(i+1,3,'Participant') #entityType
    variables.write(i+1,4,'') #referenceEntityType
    variables.write(i+1,5,'') #mimeType
    variables.write(i+1,6,'') #unit
    variables.write(i+1,7,'') #repeatable
    variables.write(i+1,8,'') #occurence
    variables.write(i+1,9,label[i]) #label:en
    variables.write(i+1,10,snomed[i]) #snomed:en

workbook.close()
