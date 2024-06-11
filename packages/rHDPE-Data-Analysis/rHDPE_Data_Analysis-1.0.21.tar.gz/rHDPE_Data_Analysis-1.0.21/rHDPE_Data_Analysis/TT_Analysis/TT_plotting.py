# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data, savefig = False ):

    resin_data = gu.get_list_of_resins_data( directory )

    # # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 2

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    samples_to_plot = [16, 23]
    # samples_to_plot = samples_present

    specimens = True
    all_specimens = True
    specimen_mask = [0, 1, 3]

    mean = False

    deriv0 = True
    deriv1 = False
    deriv2 = False

    split = False
    num_splits = 28
    split_length = 20
    splits = [split_length * (i + 2) for i in range( num_splits )]
    # splits = [78, 82]

    step = 1

    if not split:

        # splits = [0, 600]
        splits = [0, 300]

    colours = gu.list_of_colours()

    data_extraction = False

    for s in range( len( splits ) - 1 ):

        data_extraction = []

        lower_bound, upper_bound = splits[s], splits[s + 1]

        for i in samples_to_plot:

            if specimens:

                mask = np.where( sample_array == i )[0]

                for ind, j in enumerate( mask ):

                    if (ind in specimen_mask) or all_specimens:

                        if deriv0:

                            strain_mask = np.where( (np.array( data[5][j] ) <= upper_bound) & (np.array( data[5][j] ) >= lower_bound) )[0]

                            # data_extraction.append( np.array( data[5][j] )[strain_mask] )
                            # data_extraction.append( np.array( data[4][j] )[strain_mask] )

                            plt.plot( np.array( data[5][j] )[strain_mask], np.array( data[4][j] )[strain_mask], label = file_data[j][2], color = colours[i] )

                        if deriv1:

                            strain_mask = np.where( (np.array( first_derivative_data[5][j] ) <= upper_bound) & (np.array( first_derivative_data[5][j] ) >= lower_bound) )[0]

                            plt.plot( np.array( first_derivative_data[5][j] )[strain_mask][::step], np.array( first_derivative_data[4][j] )[strain_mask][::step], label = file_data[j][2], color = colours[i] )

                        if deriv2:

                            strain_mask = np.where( (np.array( second_derivative_data[5][j] ) <= upper_bound) & (np.array( second_derivative_data[5][j] ) >= lower_bound) )[0]

                            plt.plot( np.array( second_derivative_data[5][j] )[strain_mask], np.array( second_derivative_data[4][j] )[strain_mask], label = file_data[j][2], color = colours[i] )

        # plt.legend( ncol = 2, borderaxespad = 0 )
        # plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
        plt.legend( ncol = 2, loc = 'upper right', borderaxespad = 0, fontsize = 20 )
        # plt.legend()

        plt.xlabel( "Strain [%]", fontsize = 20 )
        plt.ylabel( "Stress [MPa]", fontsize = 20 )
        plt.xticks( fontsize = 20 )
        plt.yticks( fontsize = 20 )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( output_directory + "TT/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( output_directory + "Plot_Coords/Unnamed.txt", array )

            # df = pd.DataFrame( data_extraction )
            #
            # df = df.transpose()
            #
            # df.to_csv( directory + "Output/Plot_Coords/Unnamed.csv" )
