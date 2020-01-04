# Nima Namjouyan Capgemini Task 27/10/2019

import mysql.connector
from pandas import DataFrame
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import re
from mysql.connector import Error
import numpy as np
from fpdf import FPDF

# This function handles connecting to database

def Connect_2_Db(database_name):
	mydb = mysql.connector.connect(
		host="localhost",
		database= database_name,
		user="root",
		passwd="nima"
		)
	return mydb

# This function returns the percentage of unspecified data, missing/empty data
# in form of dictionaries and otherwise
def Total_Unspec_Empty(df):
	Total_Unspec = 0
	Total_Empty = 0
	Total_Points = 0
	field_Unspec_dict = {}
	field_Empty_dict = {}
	field_Total_dict = {}
	field_Unspec_list = []
	field_Empty_list = []
	field_Total_list = []

	for column in df.columns[1:]:
		field_Unspec_list.append(round((df[column].str.count('XX*')).sum()/len(df.index)*100, 1))
		field_Empty_list.append(round((df[column].values == '').sum()/len(df.index)*100, 1))
		Total_Unspec = Total_Unspec + (df[column].str.count('XX*')).sum()
		Total_Empty = Total_Empty + (df[column].values == '').sum()

	Total_Empty_Percent = round(Total_Empty/(df.size - len(df.index))*100, 1)
	Total_Unspec_Percent = round(Total_Unspec/(df.size - len(df.index))*100, 1)
	field_Total_list = [x + y for x, y in zip(field_Unspec_list, field_Empty_list)]

	field_Unspec_dict = dict(zip(df.columns[1:], field_Unspec_list))
	field_Empty_dict = dict(zip(df.columns[1:], field_Empty_list))
	field_Total_dict = dict(zip(df.columns[1:], field_Total_list))

	Total_Points = df.size - len(df.index)

	return Total_Empty_Percent, Total_Unspec_Percent, field_Unspec_dict, field_Empty_dict, field_Total_dict, Total_Points

# This function used for making barcharts of dictionary data
def do_dict_bargraph(data, x_label, y_label, title, fig_title):
	fig = plt.figure()
	fig.clf()
	ax = fig.add_subplot(111)


	plt.bar(range(len(data)), data.values(), align = "center")
	plt.xticks(range(len(data)), list(data.keys()))

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel(y_label)
	ax.set_xlabel(x_label)
	ax.set_title(title)

	fig.autofmt_xdate()

	for i, v in enumerate(data.values()):
		ax.text(i-0.4, v+0.01 , str(v), color='red', fontweight='bold')
	fig.savefig(fig_title+'.png', bbox_inches='tight')



SQL_2015_Casuality_Table_Sel = "select * from 2015_sa_casualty" #Query on casualty table columns from 2015
SQL_2015_Crash_Table_Sel = "select * from 2015_sa_crash" #Query on crash table columns from 2015
SQL_2015_Units_Table_Sel = "select * from 2015_sa_units" #Query on units table columns from 2015

try:
	Yr_2015_Db = Connect_2_Db('year_2015') #Connect to year 2015 database constructed in MySQL

	# Set up a cursor and make a dataframe forcasualty table
	cursor = Yr_2015_Db.cursor()
	cursor.execute(SQL_2015_Casuality_Table_Sel)
	records = cursor.fetchall()
	df_Casualty = DataFrame(records)
	df_Casualty.columns = cursor.column_names


	Cas_Total_Unspec_Empty_2015 = Total_Unspec_Empty(df_Casualty) #Uses Total_Unspec_Empty function to find information about missing/empty data
	
    # Finding the most common hospital
	Most_Com_Hospital = df_Casualty['Hospital'].value_counts().to_dict()
	Most_Com_Hospital = {k: v for k, v in Most_Com_Hospital.items() if ((k.startswith('XX') == False) and (k != ''))}

	Age_df = pd.to_numeric(df_Casualty['Age'], errors='coerce') #This dataframe is used to calculate mean and standard diviation of ages in reporting

	# Set up a cursor and make a dataframe for crash table
	cursor.execute(SQL_2015_Crash_Table_Sel)
	records = cursor.fetchall()
	df_Crash = DataFrame(records)
	df_Crash.columns = cursor.column_names

	Crash_Total_Unspec_Empty_2015 = Total_Unspec_Empty(df_Crash) #Uses Total_Unspec_Empty function to find information about missing/empty data

	CrashVsTime_dict = df_Crash['Month'].value_counts().to_dict() #Used to plot crashes vs time in reporting section

	# Set up a cursor and make a dataframe for units table
	cursor.execute(SQL_2015_Units_Table_Sel)
	records = cursor.fetchall()
	df_Units = DataFrame(records)
	df_Units.columns = cursor.column_names

	Units_Total_Unspec_Empty_2015 = Total_Unspec_Empty(df_Units)#Uses Total_Unspec_Empty function to find information about missing/empty data

	####################################################################################
	# Plotting Unspecified Entries (i.e. 'X's) For Each Field For 2015 Casualties Table
	####################################################################################
	do_dict_bargraph(Cas_Total_Unspec_Empty_2015[2], 'Fields', 'Number Of Unspecified Entries (%)', 'Unspecified Entries In Each Field - 2015 Casualties Table', '2015_Casualty_Unspec')
	

	####################################################################################
	# Plotting Missing Entries (i.e. Empty spaces) For Each Field For 2015 Casualties 
	####################################################################################
	do_dict_bargraph(Cas_Total_Unspec_Empty_2015[3], 'Fields', 'Number Of Missing Entries (%)', 'Missing Entries In Each Field - 2015 Casualties Table', '2015_Casualty_Missing')

	#########################################################################################################
	# Plotting Missing + Unspecified Entries (i.e. Empty spaces And 'X's) For Each Field For 2015 Casualties 
	#########################################################################################################
	do_dict_bargraph(Cas_Total_Unspec_Empty_2015[4], 'Fields', 'Number Of Missing Plus Unspecified Entries (%)', 'Missing Plus Unspecified Entries In Each Field - 2015 Casualties Table', '2015_Casualty_Combo')


	#########################################################################################################
	# Plotting Number Of Crashes Vs Time For 2015 
	#########################################################################################################
	do_dict_bargraph(CrashVsTime_dict, 'Months', 'Number Of Crashes', 'Number Of Crashes Vs Time - 2015 Crash Table', '2015_CrashesVsTime')


except Error as e:
    print("Error reading data from MySQL table", e)


#########################################################################################################
# Report Generation From 2015 Data
#########################################################################################################
pdf = FPDF('P', 'mm', 'A4')
pdf.add_page()
pdf.set_xy(105-55, 0)
pdf.set_font('arial', 'BU', 20)
pdf.cell(110, 30, "Capgemini Road Crash Report", 0, 0, 'C')
pdf.set_xy(10, 20)
pdf.set_font('arial', 'BU', 16)
pdf.cell(50, 10, "Year 2015 Data Quality:", 0, 0, 'C')

pdf.set_xy(5, 40)
pdf.set_font('arial', 'B', 16)
pdf.cell(40, 10, 'Table', 1, 0, 'C')
pdf.cell(50, 10, 'Total Data Points', 1, 0, 'C')
pdf.cell(50, 10, 'Unspecified (%)', 1, 0, 'C')
pdf.cell(50, 10, 'Missing (%)', 1, 0, 'C')

pdf.set_xy(5, 50)
pdf.cell(40, 10, 'Casualty', 1, 0, 'C')
pdf.cell(50, 10, str(Cas_Total_Unspec_Empty_2015[5]), 1, 0, 'C')
pdf.cell(50, 10, str(Cas_Total_Unspec_Empty_2015[1]), 1, 0, 'C')
pdf.cell(50, 10, str(Cas_Total_Unspec_Empty_2015[0]), 1, 0, 'C')

pdf.set_xy(5, 60)
pdf.cell(40, 10, 'Crash', 1, 0, 'C')
pdf.cell(50, 10, str(Crash_Total_Unspec_Empty_2015[5]), 1, 0, 'C')
pdf.cell(50, 10, str(Crash_Total_Unspec_Empty_2015[1]), 1, 0, 'C')
pdf.cell(50, 10, str(Crash_Total_Unspec_Empty_2015[0]), 1, 0, 'C')

pdf.set_xy(5, 70)
pdf.cell(40, 10, 'Units', 1, 0, 'C')
pdf.cell(50, 10, str(Units_Total_Unspec_Empty_2015[5]), 1, 0, 'C')
pdf.cell(50, 10, str(Units_Total_Unspec_Empty_2015[1]), 1, 0, 'C')
pdf.cell(50, 10, str(Units_Total_Unspec_Empty_2015[0]), 1, 0, 'C')

pdf.set_xy(5, 90)
pdf.image('2015_Casualty_Unspec.png', x = None, y = None, w = 0, h = 0, type = '', link = '')

pdf.add_page()

pdf.set_xy(5, 50)
pdf.image('2015_Casualty_Missing.png', x = None, y = None, w = 0, h = 0, type = '', link = '')

pdf.add_page()

pdf.set_xy(0, 50)
pdf.image('2015_Casualty_Combo.png', x = None, y = None, w = 0, h = 0, type = '', link = '')

pdf.add_page()

pdf.set_xy(10, 5)
pdf.set_font('arial', 'BU', 16)
pdf.cell(50, 10, "Year 2015 Most Common Hospital:", 0, 0, 'L')
pdf.set_font('arial', 'B', 12)
pdf.set_xy(10, 20)
pdf.cell(50, 10, str(max(Most_Com_Hospital, key=Most_Com_Hospital.get)), 1, 0, 'C')

pdf.set_xy(10, 40)
pdf.set_font('arial', 'BU', 16)
pdf.cell(50, 10, "Year 2015 Age Average:", 0, 0, 'L')
pdf.set_font('arial', 'B', 12)
pdf.set_xy(10, 55)
pdf.cell(50, 10, str("{0:.2f}".format(Age_df.mean(axis = 0 , skipna = True))), 1, 0, 'C')

pdf.set_xy(10, 70)
pdf.set_font('arial', 'BU', 16)
pdf.cell(50, 10, "Year 2015 Age STD:", 0, 0, 'L')
pdf.set_font('arial', 'B', 12)
pdf.set_xy(10, 85)
pdf.cell(50, 10, str("{0:.2f}".format(Age_df.std(axis = 0 , skipna = True))), 1, 0, 'C')

pdf.set_xy(10, 100)
pdf.set_font('arial', 'BU', 16)
pdf.cell(50, 10, "Year 2015 Number Of Crashes Vs Time:", 0, 0, 'L')

pdf.set_xy(0, 110)
pdf.image('2015_CrashesVsTime.png', x = None, y = None, w = 0, h = 0, type = '', link = '')


pdf.output('CapGemini Report.pdf', 'F')