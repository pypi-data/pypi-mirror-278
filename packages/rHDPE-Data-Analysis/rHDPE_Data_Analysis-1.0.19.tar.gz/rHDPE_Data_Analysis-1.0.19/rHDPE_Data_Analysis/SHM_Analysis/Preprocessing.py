# Imports.

import os
import glob
import re
import numpy as np
import pandas as pd

from .. import Global_Utilities as gu

# Function definitions.

def read_raw_data_file_1( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    with open( filename, 'r' ) as file:

        column_data = [[], []]

        lines = file.readlines()

        linenumber = 0

        for line in lines:

            if linenumber < 2:

                linenumber += 1
                continue

            if line.rstrip():

                a_list = line.replace( '"', '' ).rstrip().split( "," )

                column_data[0].append( float( a_list[3] ) )
                column_data[1].append( float( a_list[5] ) )

            else:

                break

    for i in range( 2 ):

        data[i].append( column_data[i] )

    data[2].append( list( np.array( column_data[0] ) * np.array( column_data[0] ) - 1 / np.array( column_data[0] ) ) )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    resins = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + "*" )], key = gu.sort_raw_files_1 )

    file_data, data = [], [[], [], []]

    pattern = re.compile( r"^Resin(\d+)" )

    for r in resins:

        filenames = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + r + "/*" )], key = gu.sort_raw_files_2 )

        resin = int( pattern.search( r ).groups()[0] )

        for f in filenames:

            read_raw_data_file_1( data_directory + r + "/" + f, f, resin_data, file_data, data )

    return file_data, data

def standardise_data( data ):
    '''Standardise data.'''

    pass

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    # Add s for curves that are too short.

    specimens = {2:[2], 3:[3], 4:[0, 2, 4], 8:[3], 13:[0], 17:[5], 18:[0, 3], 23:[1]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "s"

def read_files_and_preprocess( directory, data_directory, merge_groups ):
    '''Read files and preprocess data.'''

    file_data, data = extract_raw_data( directory, data_directory )

    standardise_data( data )

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def write_csv( output_directory, file_data, data ):
    '''Write read and preprocessed data to a .csv file.'''

    pass

def read_csv( directory, output_directory, merge_groups ):
    '''Read the preprocessed .csv files.'''

    return [], []

def remove_files( file_data, data ):
    '''Remove files not needed/wanted for analysis by searching for letters in file descriptions.'''

    files_to_remove = []

    for i in range( len( file_data ) ):

        s = file_data[i][3]

        if s.find( "s" ) > -0.5:

            files_to_remove.append( i )

    files_to_remove.reverse()

    for r in files_to_remove:

        file_data.pop( r )
        data[0].pop( r )
        data[1].pop( r )
        data[2].pop( r )

def compute_mean( output_directory, file_data, data):
    '''Compute the mean data for each resin.'''

    pass

def read_mean( output_directory, data ):
    '''Read the computed means for each resin from a file.'''

    pass
