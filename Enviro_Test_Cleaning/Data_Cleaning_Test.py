'''---------------------------------------------------------------------------------------------------------------------
Description: This file contains all the base functions used for data pre-processing and the automated cleaning of the
eGRID raw data. Flexible enough to be called in future scripts for cohesive use.
Project: CS 383 -- Data Mining Final Project -- eGRID 1996-2016 Plant Emission Analysis
Author: Stephen W. Romer
Co-Author: Andrew Kuczma
Date Created: 02/11/2019
Date Last Updated: 10/12/2019
---------------------------------------------------------------------------------------------------------------------'''

# Importation call of the libraries needed to read raw data and process cleaned data
import xlrd         # used to read .xls & .xlsx files
import xlwt         # used to create new .xls and .xlsx files
import numpy as np  # advanced computational array library
from os import path


# Arrays containing the locations of all the data used; will get rid of manual path names using os.path later
# TODO: Streamline file paths using os.path^^

# TODO FIGURE OUT A WAY TO MAKE RAW DATA PARSEABLE BY SCRIPTS!?!?
# Current location of raw, unchanged data sets directly eGRID (NOT USABLE YET)
Raw_Data_Files = ["C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID1996_plant.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID1997_plant.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID1998_plant.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID1999_plant.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2000_plant.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2004_plant.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2005_plant.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2007_plant.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2009_data.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2010_data.xls",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2012_data.xlsx",    # CHANGE IN FILE TYPE?
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2014_data.xlsx",
                  "C:/Users/romer/Desktop/egrid2016_all_files_since_1996/eGRID2016_data.xlsx"]

# Location of hand-processed data sets (mostly necessary due to numerous formatting changes,
# lack of consistency in-between years, loose file naming conventions, exponential # of outliers, etc...)
Data_Files = ["C://Users//romer//Desktop//NOT_RAW_DATA/DATA_1996-2000.xlsx",
              "C://Users//romer//Desktop//NOT_RAW_DATA//DATA_2004.xlsx",
              "C://Users//romer//Desktop//NOT_RAW_DATA//DATA_2005-2016.xlsx"]

# General information of all books and all their sheets contained within; prints report of total row and column #'s
# found, as well as book location in memory (no way to grab book by name in xlrd yet...)
def Get_Data_Size():

    for book in Raw_Data_Files:
        workbook = xlrd.open_workbook(book)
        print(workbook)

        for sheet in workbook.sheets():
            worksheet = workbook.sheet_by_name(sheet.name)
            print('Sheet Name: ' + worksheet.name)
            print('# of Rows: ' + str(worksheet.nrows), '\n# of Columns: ' + str(worksheet.ncols))

# Pulls entire Tuple/Attribute values and adds each one to a list that is
# returned for easy pass through to statistical, regression and visualization functions.
def Pull_Tuple_Info(sheet, col_index):

    row_vals = []   # initializes as empty list
    for row_index in range(2, sheet.nrows):                 # starts at 2 due to the labels present for the first 2 rows
        cell_obj = sheet.cell(row_index, col_index)

        # Conditional check that catches empty cells in data sheets TODO (Look at 1997 plant data)
        if cell_obj.value == '' or cell_obj.value is None or cell_obj.value == 'N/A':      # Used to ignore empty cells during data pull
            cell_obj.value = np.nan                             # sets empty to values to nan (Not a number),
            row_vals.append(cell_obj.value)                     # WARNING MIGHT MESS WITH np.array type matching sync


        # Adds determinable value to the list
        else:
            row_vals.append(cell_obj.value)

    return row_vals     # returns regular python list; can be easily converted to numpy array using,
                        # np.array(Pull_Tuple_Info(worksheet, columns), dtype='object')

# TODO: ADD NEW VERSION TO PASS ANY BOOK AND SHEET TO SAVE TO NUMPY ARRAY FOR STATISTICAL FURTHERING
#  (NOTE: DUE TO FORMATTING CHANGES BETWEEN YEARS 2000-04-10,
#  COL CONVENTIONS CHANGED AND TWEAKING IS REQUIRED FOR RAW DATA PASSING)
# Processes every cleaned data table and scrapes all data sheets attributes; saves each sheet scraped to a
# 2d numpy array for possible statistical advantages later on.
def Scrape_All_Datasets():

    for book in Data_Files:
        # opens book from file list
        workbook = xlrd.open_workbook(book)

        for sheet in workbook.sheets():
            # opens worksheets from current book in order
            # worksheet = workbook.sheet_by_index(currentIndex)      # worksheet = Contents, etc... (BY INDEX!!!)
            worksheet = workbook.sheet_by_name(sheet.name)           # worksheet = Contents, etc... (BY NAME!!!)
            print(worksheet.name)

            # Listed like this to just to remind which years share the same formats
            year = ['1996', '1997', '1998', '1999', '2000',
                    '2004',
                    '2005', '2007', '2009',
                    '2010', '2012', '2014', '2016']

            # iterates through each year in the list of wanted years
            for element in year:

                # Compares the given sheet with our next wanted year to check if they match
                if worksheet.name == element:
                    # print('# of Rows:%d' % worksheet.ncols)
                    # print('# of Cols:%d' % worksheet.nrows)

                    # creates a 2d numpy array based on our sheets dimensions, starting from the 1st row that contains
                    # actual information
                    sheet_array = np.zeros([int(worksheet.nrows-2), int(worksheet.ncols-2)]) #, dtype='object')

                    # Debug prints--------------
                    # print(sheet_array)
                    # print(sheet_array.shape)
                    # --------------------------

                    # Detailed dimensions for each attribute
                    for columns in range(2, worksheet.ncols-2):
                        scraped_values_list = np.array(Pull_Tuple_Info(worksheet, columns)) #, dtype='object')
                        sheet_array[:, columns] = scraped_values_list
                        # print(sheet_array)
                # Prints data set as an array
                    print(sheet_array)

# Function to scrape a specific data set passed by the user.
def Scrape_Dataset(book, sheet):

        workbook = xlrd.open_workbook(book)
        worksheet = workbook.sheet_by_name(sheet)           # worksheet = Contents, etc... (BY NAME!!!)
        print(worksheet.name)

        # TODO REMEMBER!!!!! CHANGE -x TO COLUMN SELECTOR VALUE
        sheet_array = np.zeros([int(worksheet.nrows-2), int(worksheet.ncols-2)], dtype='float64')   #-2 due to NaN data
        print(sheet_array)

        # print(sheet_array.shape)

        # TODO REMEMBER!!!!! CHANGE RANGE START VALUE AND -x VALUE TO COLUMN SELECTOR VALUE
        # Detailed dimensions for each attribute
        for columns in range(2, worksheet.ncols-2):
            scraped_values_list = np.array(Pull_Tuple_Info(worksheet, columns), dtype='float64')
            sheet_array[:, columns] = scraped_values_list
            # print(np.size(scraped_values_list))

        # Prints data set as an array
        return sheet_array

# TODO: Write func taking RAW data and producing new .xls or .xlsx wth a sheet for each year's cleaned data (might cut)
#def Write_Clean_Data():
#   newBook = xlwt.Workbook()                       #creates new empty book (maybe seperate function)
#   newBook.save('Cleaned_Data.xls')                   #Saves new data as a new book (Might add to other fucntion below)
    #Cleaned_Data = []
    #return Cleaned_Data

''''--------------------------------------------------------------
# Test calls for each function (ONLY RUN ONE AT A TIME!!!!!!)
#Get_Data_Size()

#Scrape_All_Datasets()

#workbook = xlrd.open_workbook(Data_Files[0])
#worksheet = workbook.sheet_by_name('1996')
#Pull_Tuple_Info(worksheet, 0)
------------------------------------------------------------------'''

# Get_Data_Size()
#print(Scrape_Dataset(Data_Files[0], '2000'))