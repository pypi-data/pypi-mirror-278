# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( directory, output_directory, file_data, data, savefig = False ):

    resin_data = gu.get_list_of_resins_data( directory )

    # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    # samples_to_plot = samples_present
    samples_to_plot = [1, 3, 6, 8, 9, 12, 15, 17, 18, 20, 24]

    specimens = False
    mean = True

    split = False

    if not split:

        splits = [0, 100]

    colours = gu.list_of_colours()

    data_extraction = False

    plt.figure( figsize = (10, 8) )

    for s in range( len( splits ) - 1 ):

        data_extraction = []

        lower_bound, upper_bound = splits[s], splits[s + 1]

        for i in samples_to_plot:

            if mean:

                mask = np.where( sample_array == i )[0]

                for j in mask:

                    if file_data[j][0] == 3 or file_data[j][0] == 9:

                        plt.plot( np.array( data[2] ), np.array( data[1][j] )[[3, 6, 7, 8]], label = resin_data.loc[i]["Label"], color = colours[i] )

                    else:

                        plt.plot( np.array( data[0] ), np.array( data[1][j] ), label = resin_data.loc[i]["Label"], color = colours[i] )

        plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0, fontsize = 18 )
        # plt.legend( ncol = 2, fontsize = 18, bbox_to_anchor = ( 1.05, 1 ) )

        plt.xlabel( "Time [Hours]", fontsize = 18 )
        plt.ylabel( "Bottle Success Rate [%]", fontsize = 18 )
        plt.xticks( fontsize = 18 )
        plt.yticks( fontsize = 18 )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( output_directory + "ESCR/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( output_directory + "Plot_Coords/Unnamed.txt", array )
