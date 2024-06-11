# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data, savefig = False ):

    resin_data = gu.get_list_of_resins_data( directory )

    # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    # samples_to_plot = [1, 3, 12, 15, 6, 9]
    samples_to_plot = samples_present

    specimens = False
    all_specimens = True
    specimen_mask = [0, 1, 3]

    mean = True

    deriv0 = True
    deriv1 = False
    deriv2 = False

    step = 40

    split = True
    num_splits = 25
    split_length = 20
    splits = [split_length * (i + 5) for i in range( num_splits )]
    # splits = [400, 450]

    if not split:

        splits = [int( data[1][0] ), int( data[1][len( data[1] ) - 1] )]

    colours = gu.list_of_colours()

    data_extraction = False

    for s in range( len( splits ) - 1 ):

        data_extraction = []

        lower_bound, upper_bound = splits[s], splits[s + 1]

        # if not (upper_bound < 160 or lower_bound > 180):
        #
        #     plt.axvspan( 160, 180, alpha = 0.5, color = 'red' )
        #
        # if not (upper_bound < 300 or lower_bound > 320):
        #
        #     plt.axvspan( 300, 320, alpha = 0.5, color = 'red' )
        #
        # if not (upper_bound < 380 or lower_bound > 400):
        #
        #     plt.axvspan( 380, 400, alpha = 0.5, color = 'red' )
        #
        # if not (upper_bound < 460 or lower_bound > 480):
        #
        #     plt.axvspan( 460, 480, alpha = 0.5, color = 'red' )
        #
        # if not (upper_bound < 480 or lower_bound > 500):
        #
        #     plt.axvspan( 480, 500, alpha = 0.5, color = 'red' )

        for i in samples_to_plot:

            if specimens:

                mask = np.where( sample_array == i )[0]

                for ind, j in enumerate( mask ):

                    if (ind in specimen_mask) or all_specimens:

                        if deriv0:

                            temp_mask = np.where( (np.array( data[1] ) <= upper_bound) & (np.array( data[1] ) >= lower_bound) )[0]

                            plt.plot( np.array( data[1] )[temp_mask], np.array( data[3][j] )[temp_mask], label = file_data[j][2], color = colours[i] )

                        if deriv1:

                            temp_mask = np.where( (np.array( first_derivative_data[1] ) <= upper_bound) & (np.array( first_derivative_data[1] ) >= lower_bound) )[0]

                            # scaler = 0.91

                            # if j == mask.max():
                            #
                            #     temp_mask = np.where( (np.array( first_derivative_data[1] ) * scaler <= upper_bound) & (np.array( first_derivative_data[1] ) * scaler >= lower_bound) )[0]
                            #
                            #     plt.plot( np.array( first_derivative_data[1] )[temp_mask][::step] * scaler, np.array( first_derivative_data[3][j] )[temp_mask][::step], label = file_data[j][2], color = colours[i] )
                            #
                            # else:

                            plt.plot( np.array( first_derivative_data[1] )[temp_mask][::step], np.array( first_derivative_data[3][j] )[temp_mask][::step], label = file_data[j][2], color = colours[i] )

                        if deriv2:

                            temp_mask = np.where( (np.array( second_derivative_data[1] ) <= upper_bound) & (np.array( second_derivative_data[1] ) >= lower_bound) )[0]

                            plt.plot( np.array( second_derivative_data[1] )[temp_mask], np.array( second_derivative_data[3][j] )[temp_mask], label = file_data[j][2], color = colours[i] )

            if mean:

                index = np.where( samples_present_array == i )[0][0]

                if deriv0:

                    temp_mask = np.where( (np.array( data[1] ) <= upper_bound) & (np.array( data[1] ) >= lower_bound) )[0]

                    data_extraction.append( np.array( data[1] )[temp_mask] )
                    data_extraction.append( np.array( data[5][index] )[temp_mask] )

                    plt.plot( np.array( data[1] )[temp_mask], np.array( data[5][index] )[temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                if deriv1:

                    temp_mask = np.where( (np.array( first_derivative_data[1] ) <= upper_bound) & (np.array( first_derivative_data[1] ) >= lower_bound) )[0]

                    plt.plot( np.array( first_derivative_data[1] )[temp_mask][::step], np.array( first_derivative_data[5][index] )[temp_mask][::step], label = resin_data.loc[i]["Label"], color = colours[i] )

                if deriv2:

                    temp_mask = np.where( (np.array( second_derivative_data[1] ) <= upper_bound) & (np.array( second_derivative_data[1] ) >= lower_bound) )[0]

                    plt.plot( np.array( second_derivative_data[1] )[temp_mask], np.array( second_derivative_data[5][index] )[temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

        plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
        # plt.legend( ncol = 2 )

        plt.xlabel( "Temperature °C" )
        plt.ylabel( "Percentage Weight" )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( output_directory + "TGA/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( directory + "Plot_Coords/Unnamed.txt", array )
