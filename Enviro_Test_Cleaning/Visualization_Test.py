'''---------------------------------------------------------------------------------------------------------------------
Description: This file contains functions for the visual processing of eGRID statistics
and the creation of graphical images for data visualization.
Project: CS 383 -- Data Mining Final Project -- eGRID 1996-2016 Plant Emission Analysis
Author: Stephen W. Romer
Date Created: 10/12/2019
Last Updated: 10/12/2019
---------------------------------------------------------------------------------------------------------------------'''
# Importation call for plotly: a python library for graphical analysis and generation.
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from scipy import stats

# Imports paths for files
from Data_Cleaning_Test import Data_Files

from Statistics_Test import Calc_Mean_Of_Attribute, Calc_Sum_Of_Attribute
from Statistics_Test import Check_Atrribute


# --------------------------------------------------------------------------------------------------
# TODO: SPEED THIS UP!!! WASTES TIME CALLING (THREE) SEPARATE SCRIPTS FOR DATA
#  AND FOR RECALCULATING/EVALUATING EVERY SINGLE TIME
#---------------------------------------------------------------------------------------------------

def Graph_Averages_Alltime(graph_type, yaxis_label, graph_title, graph_color, attribute_index):

    # Checks for correct attribute input
    gate = Check_Atrribute(attribute_index)
    if gate is False:
        return

    else:
        years = np.array([1996, 1997, 1998, 1999, 2000, 2004, 2005, 2007, 2009, 2010, 2012, 2014, 2016])

        # print(np.size(years))

        # TODO REPLACE WITH FOR LOOP
        averages = np.array([Calc_Mean_Of_Attribute(Data_Files[0], '1996', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[0], '1997', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[0], '1998', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[0], '1999', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[0], '2000', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[1], '2004', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[2], '2005', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[2], '2007', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[2], '2009', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[2], '2010', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[2], '2012', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[2], '2014', attribute_index),
                             Calc_Mean_Of_Attribute(Data_Files[2], '2016', attribute_index)])

        slope, intercept, r_value, p_value, std_err = stats.linregress(years, averages)
        print(str(slope), str(intercept), str(r_value), str(p_value), str(std_err))
        line = slope*years+intercept

        graph_type = str(graph_type.upper())
        # print(graph_type)

        if graph_type == 'LINE':
            trace1 = go.Scatter(x=years,
                                y=averages,
                                mode='markers',
                                marker_color=str(graph_color))
            trace2 = go.Scatter(x=years,
                                y=line,
                                mode='lines',
                                marker_color='black')

            data = [trace1, trace2]

            fig = go.Figure(data=data)

            fig.show()

            '''fig.update_layout(
                title=str(graph_title),
                titlefont_size=32,
                xaxis_tickfont_size=16,
                yaxis=dict(
                    title=str(yaxis_label),
                    titlefont_size=16,
                    tickfont_size=16, ))
            fig.show()'''

        elif graph_type == 'BAR':
            fig = go.Figure(
                data=[go.Bar(x=years, y=averages, marker_color=str(graph_color))])

            fig.update_layout(
                title=str(graph_title),
                xaxis_tickfont_size=16,
                yaxis=dict(
                    title=str(yaxis_label),
                    titlefont_size=32,
                    tickfont_size=16, ))
            fig.show()

        elif graph_type == 'SCAT':
            fig = px.scatter(x=years, y=averages, labels={'x': 'Years', 'y': str(yaxis_label)})
            fig.show()

        else:
            print('ERROR!: Choose a valid graph type')
            return

# Graphs Total Sum of attribute passed / all years
def Graph_Sums_Alltime(graph_type, yaxis_label, graph_title, graph_color, attribute_index):

    # Checks for correct attribute input
    gate = Check_Atrribute(attribute_index)
    if gate is False:
        return

    else:
        years = np.array([1996, 1997, 1998, 1999, 2000, 2004, 2005, 2007, 2009, 2010, 2012, 2014, 2016])

        # print(np.size(years))

        # TODO REPLACE WITH FOR LOOP
        sums = np.array([Calc_Sum_Of_Attribute(Data_Files[0], '1996', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[0], '1997', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[0], '1998', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[0], '1999', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[0], '2000', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[1], '2004', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[2], '2005', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[2], '2007', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[2], '2009', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[2], '2010', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[2], '2012', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[2], '2014', attribute_index),
                             Calc_Sum_Of_Attribute(Data_Files[2], '2016', attribute_index)])


        # print(np.size(averages))

        graph_type = str(graph_type.upper())
        # print(graph_type)

        # Graphs Line Graph
        if graph_type == 'LINE':
            fig = go.Figure(
                data=[go.Line(x=years, y=sums, line_color=str(graph_color))])

            fig.update_layout(
                title=str(graph_title),
                titlefont_size=32,
                xaxis_tickfont_size=16,
                yaxis=dict(
                    title=str(yaxis_label),
                    titlefont_size=16,
                    tickfont_size=16, ))
            fig.show()

        # Graphs Bar Graph
        elif graph_type == 'BAR':
            fig = go.Figure(
                data=[go.Bar(x=years, y=sums, marker_color=str(graph_color))])

            fig.update_layout(
                title=str(graph_title),
                titlefont_size=32,
                xaxis_tickfont_size=16,
                yaxis=dict(
                    title=str(yaxis_label),
                    titlefont_size=16,
                    tickfont_size=16,))

            fig.show()

        # Graphs Scatter Plot
        elif graph_type == 'SCAT':
            fig = px.scatter(x=years, y=sums, labels={'x': 'Years', 'y': str(yaxis_label)},
                             color=years, title=str(graph_title))
            fig.show()

        else:
            print('ERROR!: Choose a valid graph type')
            return

# def Graph_Regression():

# TODO: CONTINUE VISUALIZATION FOR ALL NECESSARY INFO (WORK ON REGRESSION!!!!!!!!!!!!!!!)
# Graph_Averages_Alltime('bar', 'TEST', 0)

# Graphs of totals
#Graph_Sums_Alltime('BAR', 'MEGAWATT HOURS (MWh)', 'TOTAL NET ELECTRICAL OUTPUT', 'darkgoldenrod', 2)
#Graph_Sums_Alltime('BAR', 'EMISSIONS (TONS)', 'TOTAL ANNUAL NET NOx EMISSIONS.', 'firebrick', 3)
#Graph_Sums_Alltime('BAR', 'EMISSIONS (TONS)', 'TOTAL ANNUAL NET SO2 EMISSIONS.', 'forestgreen', 4)
#Graph_Sums_Alltime('BAR', 'EMISSIONS (TONS)', 'TOTAL OF ANNUAL NET C02 EMISSIONS.', 'navy', 5)

# Graphs of Averages
#Graph_Averages_Alltime('LINE', '(lbs / MWh)', 'AVERAGE NOx EMISSION RATES', 'darkgoldenrod', 2)
Graph_Averages_Alltime('LINE', '(lbs / MWh)', 'AVERAGE NOx EMISSION RATES', 'firebrick', 3)
Graph_Averages_Alltime('LINE', '(lbs / MWh)', 'AVERAGE NOx EMISSION RATES', 'forestgreen', 4)
Graph_Averages_Alltime('LINE', '(lbs / MWh)', 'AVERAGE NOx EMISSION RATES', 'navy', 5)

#Graph_Averages_Alltime('LINE', '(lbs / MWh)', 'AVERAGE S02 EMISSION RATES', 'green', 7)
#Graph_Averages_Alltime('LINE', '(lbs / MWh)', 'AVERAGE C02 EMISSION RATES', 'blue', 8)
