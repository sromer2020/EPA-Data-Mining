'''---------------------------------------------------------------------------------------------------------------------
Description: This file contains all the computational functions to be used in conjunction with CLEANED eGRID data sets
to compute and retrieve all necessary statistical variables for both analysis and visualization.
Project: CS 383 -- Data Mining Final Project -- eGRID 1996-2016 Plant Emission Analysis
Author: Stephen W. Romer
Co-Author: Andrew Kuczma
Date Created: 05/11/2019
Last Updated: 10/12/2019
---------------------------------------------------------------------------------------------------------------------'''

# TODO: CURRENTLY ONLY WORKS WITH PRE-PROCESSED DATA SETS
#  THIS IS DUE TO FORMAT DISCREPANCIES BETWEEN YEARS IN RAW DATA (GOV'T HAS BAD QA)
# Importation call of the libraries needed to compute stats on functional command.
import xlrd                     # Parses .xls file data
import numpy as np              # Functions for most stats (Mean, Median)
from scipy import stats as sc   # Functions for stats not included in Numpy. (N

# Call to function in pre-processing script that pulls data from sheets.
# Used to compute statistics directly from the 'raw' data in order to minimize data manipulation/human error.
from Data_Cleaning_Test import Pull_Tuple_Info
from Data_Cleaning_Test import Scrape_Dataset
from Data_Cleaning_Test import Data_Files # (TODO write function that passed cleaned data into that variable)


# TODO: Make functional so user can not be lost on how to select tuples for statistics
# Used as an exception handler for attributes that are not available for statistical analysis
def Check_Atrribute(attribute):

    if attribute is None or attribute == '':
        print('Please enter a valid attribute value (3+): ')
        return False

    elif attribute < 2:
        print('ERROR!: ' + str(attribute) + ' is not quantifiable; please select number higher: ')
        return False

    else:
        print('Attribute Valid: ' + str(attribute))
        return True

# TODO: CHANGE HOW ATTRIBUTES ARE ARGUED FOR BETTER FUNCTIONALITY IN THE FUTURE,
#  CURRENTLY ONLY WORKS BY KNOWING WHAT THE TUPLES COL INDEX IS!!!!!
# Calculates Mean of designated attribute, takes book by file location, sheet name and attribute by index.
def Calc_Mean_Of_Attribute(book, sheet, attribute):
    # workbook = xlrd.open_workbook(book)
    # worksheet = workbook.sheet_by_name(sheet)

    # Checks to see if attribute argued has a computable average
    Check_Atrribute(attribute)

    # Calls Scrape_Dataset in order to get specified sheet into 2D numpy array form.
    sheet_array = np.array(Scrape_Dataset(book, sheet))

    # Calculates the mean of the suggested attribute, ignoring all NaN values. (WITHIN 99% Margin of Error)
    mean = np.nanmean(sheet_array[:, attribute])

    return mean

# Function Test:
# print(Calc_Mean_Of_Attribute(Data_Files[0],'1996', 7))

# TODO CHANGE HOW ATTRIBUTES ARE DETERMINED FOR BETTER FUNCTIONALITY IN THE FUTURE,
#  CURRENTLY ONLY WORKS BY KNOWING COL INDEX
# Calculates Median of designated attribute, takes book by file location, sheet name and attribute by index.
def Calc_Median_Of_Atrribute(book, sheet, attribute):
    # workbook = xlrd.open_workbook(book)
    # worksheet = workbook.sheet_by_name(sheet)

    # Checks to see if attribute argued has a computable average
    Check_Atrribute(attribute)

    sheet_array = np.array(Scrape_Dataset(book, sheet))
    median = np.nanmedian(sheet_array[:, attribute])

    return median

# Function Test:
# print(Calc_Median_Of_Atrribute(Data_Files[0], '1996', 4))

# TODO CHANGE HOW ATTRIBUTES ARE DETERMINED FOR BETTER FUNCTIONALITY IN THE FUTURE,
#  CURRENTLY ONLY WORKS BY KNOWING COL INDEX
# Calculates Mode of designated attribute, takes book by file location, sheet name and attribute by index.
def Calc_Mode_Of_Atrribute(book, sheet, attribute):
    workbook = xlrd.open_workbook(book)
    worksheet = workbook.sheet_by_name(sheet)

    Check_Atrribute(attribute)

    sheet_array = np.array(Scrape_Dataset(book, sheet))
    mode = sc.mode(sheet_array[:, attribute], 0)

    return mode

# Function Test:
# print(Calc_Mode_Of_Atrribute(Data_Files[0], '1998', 3))

# Calculates Sum of designated attribute, takes book by file location, sheet name and attribute by index.
def Calc_Sum_Of_Attribute(book, sheet, attribute):
    workbook = xlrd.open_workbook(book)
    worksheet = workbook.sheet_by_name(sheet)

    Check_Atrribute(attribute)

    sheet_array = np.array(Scrape_Dataset(book, sheet))
    attribute_sum = np.nansum(sheet_array[:, attribute], 0)

    return attribute_sum

# print(Calc_Sum_Of_Attribute(Data_Files[0], '1996', 4))

# Calculates CO2 Equivalence Average, takes in book and sheets from our processed data
def Calc_CO2_Equivalence_Average(book,sheet):
    workbook = xlrd.open_workbook(book)
    worksheet = workbook.sheet_by_name(sheet)

    # Pulls from sheet tuple, quicker if you know what tuples are needed
    CO2AN = np.nanmean(Pull_Tuple_Info(worksheet, 5))           # 5 = index of CO2AN col
    NETCH4AN = np.nanmean(Pull_Tuple_Info(worksheet, 6))        # 6 = index of CH4AN col
    N20AN = np.nanmean(Pull_Tuple_Info(worksheet, 7))           # 7 = index of N20AN col

    CO2EQ = ((1*CO2AN)+(21*(NETCH4AN/2000))+(310*(N20AN/2000))) # Formula for average CO2 equivalence of that year.

    return CO2EQ

# TODO FINISH IMPLEMENTING THE EQUATION FOR CO2 EMISSION RATE FOR EACH YEAR, MUST CALL UPON PREVIOUS FUNCTION FOR CO2EQ
def Calc_CO2_Equivalent_Emission_Rate(book, sheet):

    CO2EQ = Calc_CO2_Equivalence_Average(book, sheet)
    PLNGENAN = Pull_Tuple_Info(sheet, 3)

    PLC2ERTA = 2000 * (CO2EQ / PLNGENAN)
    return PLC2ERTA

# TODO REGRESSION FUNCTION FOR FUTURE PREDICTION AND VISUALIZATION
#def Linear_Regression():
#   return Regressed_Data
