# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data, shiny, shiny_samples_to_plot, shiny_split, shiny_cryst, shiny_melt, shiny_specimen, shiny_mean, savefig = False ):

    resin_data = gu.get_list_of_resins_data( directory )

    # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    # samples_to_plot = samples_present[:-7]
    samples_to_plot = [8, 15]

    if shiny:

        samples_to_plot = shiny_samples_to_plot

        if type( samples_to_plot ) == int:

            samples_to_plot = [samples_to_plot]

    specimens = True
    all_specimens = True
    specimen_mask = [1, 3]

    mean = False

    deriv0 = True
    deriv1 = False
    deriv2 = False

    cryst = True
    melt = True

    split = False
    num_splits = 15
    split_length = 10
    splits = [split_length * (i + 2) for i in range( num_splits )]
    splits = [130, 145]

    if not split:

        splits = [int( data[2][0] ), int( data[2][len( data[2] ) - 1] )]

    if shiny:

        splits = shiny_split
        melt = shiny_melt
        cryst = shiny_cryst
        mean = shiny_mean
        specimens = shiny_specimen

    colours = gu.list_of_colours()

    data_extraction = False
    shiny_data_extraction = False
    shiny_de = [samples_to_plot]

    if shiny:

        shiny_data_extraction = True

    for s in range( len( splits ) - 1 ):

        data_extraction = []

        lower_bound, upper_bound = splits[s], splits[s + 1]

        for i in samples_to_plot:

            if specimens:

                mask = np.where( sample_array == i )[0]

                for ind, j in enumerate( mask ):

                    if (ind in specimen_mask) or all_specimens:

                        if deriv0:

                            if cryst:

                                temp_mask = np.where( (np.array( data[0] ) <= upper_bound) & (np.array( data[0] ) >= lower_bound) )[0]

                                shiny_de.append( np.array( data[0] )[temp_mask] )
                                shiny_de.append( np.array( data[1][j] )[temp_mask] )

                                plt.plot( np.array( data[0] )[temp_mask], np.array( data[1][j] )[temp_mask], label = file_data[j][2] )

                            if melt:

                                temp_mask = np.where( (np.array( data[2] ) <= upper_bound) & (np.array( data[2] ) >= lower_bound) )[0]

                                shiny_de.append( np.array( data[2] )[temp_mask] )
                                shiny_de.append( np.array( data[3][j] )[temp_mask] )

                                plt.plot( np.array( data[2] )[temp_mask], np.array( data[3][j] )[temp_mask], label = file_data[j][2] )

                        if deriv1:

                            if cryst:

                                temp_mask = np.where( (np.array( first_derivative_data[0] ) <= upper_bound) & (np.array( first_derivative_data[0] ) >= lower_bound) )[0]

                                plt.plot( np.array( first_derivative_data[0] )[temp_mask], np.array( first_derivative_data[1][j] )[temp_mask], label = file_data[j][2] )

                            if melt:

                                temp_mask = np.where( (np.array( first_derivative_data[2] ) <= upper_bound) & (np.array( first_derivative_data[2] ) >= lower_bound) )[0]

                                plt.plot( np.array( first_derivative_data[2] )[temp_mask], np.array( first_derivative_data[3][j] )[temp_mask], label = file_data[j][2] )

                        if deriv2:

                            if cryst:

                                temp_mask = np.where( (np.array( second_derivative_data[0] ) <= upper_bound) & (np.array( second_derivative_data[0] ) >= lower_bound) )[0]

                                plt.plot( np.array( second_derivative_data[0] )[temp_mask], np.array( second_derivative_data[1][j] )[temp_mask], label = file_data[j][2] )

                            if melt:

                                temp_mask = np.where( (np.array( second_derivative_data[2] ) <= upper_bound) & (np.array( second_derivative_data[2] ) >= lower_bound) )[0]

                                plt.plot( np.array( second_derivative_data[2] )[temp_mask], np.array( second_derivative_data[3][j] )[temp_mask], label = file_data[j][2] )

            if mean:

                index = np.where( samples_present_array == i )[0][0]

                if deriv0:

                    if cryst:

                        temp_mask = np.where( (np.array( data[0] ) <= upper_bound) & (np.array( data[0] ) >= lower_bound) )[0]

                        # data_extraction.append( np.array( data[0] )[temp_mask] )
                        # data_extraction.append( np.array( data[4][index] )[temp_mask] )

                        plt.plot( np.array( data[0] )[temp_mask], np.array( data[4][index] )[temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    if melt:

                        temp_mask = np.where( (np.array( data[2] ) <= upper_bound) & (np.array( data[2] ) >= lower_bound) )[0]

                        data_extraction.append( np.array( data[2] )[temp_mask] )
                        data_extraction.append( np.array( data[5][index] )[temp_mask] )

                        plt.plot( np.array( data[2] )[temp_mask], np.array( data[5][index] )[temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                if deriv1:

                    if cryst:

                        temp_mask = np.where( (np.array( first_derivative_data[0] ) <= upper_bound) & (np.array( first_derivative_data[0] ) >= lower_bound) )[0]

                        plt.plot( np.array( first_derivative_data[0] )[temp_mask], np.array( first_derivative_data[4][index] )[temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    if melt:

                        temp_mask = np.where( (np.array( first_derivative_data[2] ) <= upper_bound) & (np.array( first_derivative_data[2] ) >= lower_bound) )[0]

                        plt.plot( np.array( first_derivative_data[2] )[temp_mask], np.array( first_derivative_data[5][index] )[temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                if deriv2:

                    if cryst:

                        temp_mask = np.where( (np.array( second_derivative_data[0] ) <= upper_bound) & (np.array( second_derivative_data[0] ) >= lower_bound) )[0]

                        plt.plot( np.array( second_derivative_data[0] )[temp_mask], np.array( second_derivative_data[4][index] )[temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    if melt:

                        temp_mask = np.where( (np.array( second_derivative_data[2] ) <= upper_bound) & (np.array( second_derivative_data[2] ) >= lower_bound) )[0]

                        plt.plot( np.array( second_derivative_data[2] )[temp_mask], np.array( second_derivative_data[5][index] )[temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

        plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
        # plt.legend()

        plt.xlabel( "Temperature °C" )
        plt.ylabel( "Heat Flow" )

        if shiny:

            plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
            plt.xticks( fontsize = 14 )
            plt.yticks( fontsize = 14 )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if shiny:

            savefig = True

        if savefig:

            if shiny:

                plt.savefig( output_directory + "DSC/Plots/Plot.png" )

            else:

                plt.savefig( output_directory + "DSC/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( output_directory + "Plot_Coords/Unnamed.txt", array )

        return shiny_de

def plot_variance( output_directory, data, mask, s, std_c, std_m ):

    plt.gca().set_prop_cycle( cycler( color = ['c', 'c', 'm', 'm', 'y', 'y', 'k', 'k', 'g', 'g'] ) )

    for i in mask:

        plt.plot( data[0], data[1][i], linewidth = 1 )
        plt.plot( data[2], data[3][i], linewidth = 1, label = i )

    x_axis_1 = np.linspace( 0, 0, len( data[0] ) )
    x_axis_2 = np.linspace( 0, 0, len( data[2] ) )

    plt.gca().set_prop_cycle( cycler( color = ['c', 'm'] ) )

    plt.fill_between( data[0], std_c, x_axis_1, linewidth = 1.5 )
    plt.fill_between( data[2], -np.array( std_m ), x_axis_2, linewidth = 1.5 )

    plt.title( "PCR Sample " + str( s ) )
    plt.xlabel( "Temperature (°C)" )
    plt.ylabel( "Normalised Heat Flow" )
    plt.legend()
    plt.savefig( output_directory + str( s ) + ".pdf" )
    plt.close()

def plot_maximum_range( output_directory, data, max_range_c, max_range_m ):

    plt.plot( data[0], max_range_c )
    plt.plot( data[2], -max_range_m )

    plt.xlabel( "Temperature" )
    plt.ylabel( "Range in Heat Flow" )
    plt.title( "Maximum range between specimens of the same sample" )
    plt.savefig( output_directory + "MaxRange.pdf" )
    plt.close()

def plot_variance_barchart_and_variance_correlation( output_directory, integral_c, integral_m, sample_mask ):

    nonzero_mask = np.nonzero( integral_c )[0]

    integral_c = integral_c[nonzero_mask]

    sample_mask_c = np.array( sample_mask )[nonzero_mask]

    gu.plot_barchart_of_feature( integral_c, sample_mask_c, colour = True, colour_mask = sample_mask_c, xlabel = "PCR Sample", ylabel = "Integral of Standard Deviation", title = "Variance of Samples during Crystallisation", filename = output_directory + "BarCryst.pdf", savefig = True )

    nonzero_mask = np.nonzero( integral_m )[0]

    integral_m = integral_m[nonzero_mask]

    sample_mask_m = np.array( sample_mask )[nonzero_mask]

    gu.plot_barchart_of_feature( integral_m, sample_mask_m, colour = True, colour_mask = sample_mask_m, xlabel = "PCR Sample", ylabel = "Integral of Standard Deviation", title = "Variance of Samples during Melt", filename = output_directory + "BarMelt.pdf", savefig = True )

    gu.plot_scatterplot_of_two_features( integral_c, integral_m, sample_mask_m, sample_mask_m, savefig = True, filename = output_directory + "VarianceCorr.pdf" )
