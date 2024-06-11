# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .. import Global_Utilities as gu

# Function definitions.

def plot_crossover_points( output_directory, resin_data, file_data, features_df, sample_array, samples_to_plot, specimens, mean ):

    specimen_mask = gu.produce_mask( sample_array, samples_to_plot )

    features_df_copy = features_df.iloc[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array_copy = sample_array[specimen_mask]

    if specimens:

        gu.plot_scatterplot_of_two_features( features_df_copy["Rhe_Crossover"].apply( lambda x: 10 ** x ), features_df_copy["Rhe_SMCrossover"].apply( lambda x: 10 ** x ), sample_array_copy, [f[2] for f in file_data_mask], line_of_best_fit = False, xlog = True, ylog = True, xlabel = "Angular Frequency [rad/s]", ylabel = "Storage/Loss Modulus [Pa]", savefig = True, filename = output_directory + "Rheology/Plots/Crossover_Point_Specimen.pdf" )

    if mean:

        mean_features = gu.extract_mean_features( features_df.to_numpy(), sample_array, samples_to_plot )

        mean_features_df = gu.array_with_column_titles_to_df( mean_features, features_df_copy.columns )

        gu.plot_scatterplot_of_two_features( mean_features_df["Rhe_Crossover"].apply( lambda x: 10 ** x ), mean_features_df["Rhe_SMCrossover"].apply( lambda x: 10 ** x ), sample_array_copy, [resin_data.loc[i]["Label"] for i in samples_to_plot], line_of_best_fit = False, xlog = True, ylog = True, xlabel = "Angular Frequency [rad/s]", ylabel = "Storage/Loss Modulus [Pa]", savefig = True, filename = output_directory + "Rheology/Plots/Crossover_Point_Mean.pdf" )

def plot_van_Gurp_Palmen_plot( output_directory, resin_data, file_data, data, sample_array, samples_present_array, samples_to_plot, specimens, mean, colours ):

    if specimens:

        for i in samples_to_plot:

            mask = np.where( sample_array == i )[0]

            for ind, j in enumerate( mask ):

                deriv = gu.derivative( np.log( np.array( data[3][j] ) * np.array( data[0] ) ), np.arctan( data[4][j] ) )

                plt.scatter( np.array( data[3][j] ) * np.array( data[0] ), np.array( data[4][j] ), label = file_data[j][2], color = colours[i] )

                # plt.scatter( np.array( data[3][j] )[1:-1] * np.array( data[0] )[1:-1], deriv, label = file_data[j][2], color = colours[i] )

        ax = plt.gca()
        ax.set_xscale( 'log' )
        plt.xlabel( "Complex Modulus [Pa]" )
        plt.ylabel( "Phase Angle [°]" )
        # plt.legend( ncol = 3, loc = 'lower right', borderaxespad = 0 )
        plt.tight_layout()

        plt.savefig( output_directory + "Rheology/Plots/vGP_Specimens.pdf" )

        plt.close()

    if mean:

        for i in samples_to_plot:

            index = np.where( samples_present_array == i )[0][0]

            plt.scatter( np.array( data[7][index] ), np.arctan( np.array( data[8][index] ) ) * 180 / np.pi, label = resin_data.loc[i]["Label"], color = colours[i] )

        ax = plt.gca()
        ax.set_xscale( 'log' )
        plt.xlabel( "Complex Modulus [Pa]" )
        plt.ylabel( "Phase Angle [°]" )
        plt.legend( ncol = 3, bbox_to_anchor = ( 0.880, 0 ), loc = 'lower center', borderaxespad = 0 )
        plt.tight_layout()

        plt.savefig( output_directory + "Rheology/Plots/vGP_Means.pdf" )

        plt.close()

def plot_data( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data, savefig = True ):

    perform_plot_crossover_points = False

    perform_van_Gurp_Palmen_plot = True

    perform_custom_plot = False

    resin_data = gu.get_list_of_resins_data( directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( output_directory + "Rheology/Features/Features.csv" )

    features_df = gu.array_with_column_titles_to_df( features, feature_names )

    # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    # samples_to_plot = [11, 14, 10, 13, 12, 15, 1, 2, 3, 6, 7, 9, 5]
    # samples_to_plot = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]
    # samples_to_plot = [18, 20, 21, 22, 23]
    # samples_to_plot = [16, 17, 19, 24]
    # samples_to_plot = [11, 14, 10, 13, 4]
    samples_to_plot = [23, 16, 24, 17, 7, 20, 3]

    specimens = True
    all_specimens = True
    specimen_mask = [0]

    mean = True

    deriv0 = True
    deriv1 = False
    deriv2 = False

    split = False
    num_splits = 2
    split_length = 120
    splits = [split_length * (i + 30 / 120) for i in range( num_splits )]
    # splits = [78, 82]

    log_graph = True

    radial_graph = False

    x, y = 1, 5

    if not split:

        splits = [int( data[0][len( data[0] ) - 1] ), int( data[0][0] )]

    colours = gu.list_of_colours()

    data_extraction = False

    if perform_plot_crossover_points:

        plot_crossover_points( output_directory, resin_data, file_data, features_df, sample_array, samples_to_plot, specimens, mean )

    if perform_van_Gurp_Palmen_plot:

        plot_van_Gurp_Palmen_plot( output_directory, resin_data, file_data, data, sample_array, samples_present_array, samples_to_plot, specimens, mean, colours )

    if perform_custom_plot:

        for s in range( len( splits ) - 1 ):

            data_extraction = []

            lower_bound, upper_bound = splits[s], splits[s + 1]

            if radial_graph:

                ax = plt.subplots( 1, 1, subplot_kw = dict( polar = True ) )[1]

                for i in samples_to_plot:

                    index = np.where( samples_present_array == i )[0][0]

                    freq_mask = np.where( (np.array( data[0] ) <= upper_bound) & (np.array( data[0] ) >= lower_bound) )[0]

                    # plt.scatter( np.array( data[5][index] )[freq_mask], np.array( data[6][index] )[freq_mask] )

                    alpha_scale = np.linspace( 0.3, 1, len( np.array( data[8][index] )[freq_mask] ) )

                    ax.scatter( np.arctan( np.array( data[8][index] )[freq_mask] ), np.array( data[7][index] )[freq_mask], label = resin_data.loc[i]["Label"], color = colours[i], alpha = alpha_scale, s = 25 )

                    # ax = plt.gca()
                    # ax.set_aspect( 'equal' )

                ax.set_rlim( 3, 170000 )
                ax.set_thetamin( 30 )
                ax.set_thetamax( 75 )
                ax.set_rscale( 'symlog' )

                r = np.arange( 0, 170000, 10 )
                theta = [np.pi / 4 for i in r]
                ax.plot( theta, r, "k--" )

            else:

                for i in samples_to_plot:

                    if specimens:

                        mask = np.where( sample_array == i )[0]

                        for ind, j in enumerate( mask ):

                            if (ind in specimen_mask) or all_specimens:

                                if deriv0:

                                    freq_mask = np.where( (np.array( data[0] ) <= upper_bound) & (np.array( data[0] ) >= lower_bound) )[0]

                                    # plt.plot( np.array( data[0] )[freq_mask], np.array( data[y][j] )[freq_mask], label = file_data[j][2], color = colours[i], linewidth = 2.5 )

                                    plt.plot( np.array( data[0] )[freq_mask], np.array( data[1][j] )[freq_mask], label = "Storage Modulus", color = colours[i] )
                                    plt.plot( np.array( data[0] )[freq_mask], np.array( data[2][j] )[freq_mask], label = "Loss Modulus", color = colours[i] )

                                    # m = (np.log( data[3][j][3] ) - np.log( data[3][j][1] )) / (np.log( data[0][3] ) - np.log( data[0][1] ))
                                    # b = np.log( data[3][j][2] / data[0][2] ** m )

                                    data_extraction.append( np.array( data[0] )[freq_mask] )
                                    data_extraction.append( np.array( data[1][j] )[freq_mask] )
                                    data_extraction.append( np.array( data[2][j] )[freq_mask] )

                                    # plt.plot( np.array( data[0] )[freq_mask], np.array( data[0] )[freq_mask] ** m * np.exp( b ), "--", color = colours[i], linewidth = 2.5 )

                                if deriv1:

                                    freq_mask = np.where( (np.array( first_derivative_data[0] ) <= upper_bound) & (np.array( first_derivative_data[0] ) >= lower_bound) )[0]

                                    # Minus sign for log graph!

                                    plt.plot( np.array( first_derivative_data[0] )[freq_mask], -np.array( first_derivative_data[3][j] )[freq_mask], label = file_data[j][2], color = colours[i] )

                                if deriv2:

                                    freq_mask = np.where( (np.array( second_derivative_data[0] ) <= upper_bound) & (np.array( second_derivative_data[0] ) >= lower_bound) )[0]

                                    plt.plot( np.array( second_derivative_data[0] )[freq_mask], np.array( second_derivative_data[3][j] )[freq_mask], label = file_data[j][2], color = colours[i] )

                    if mean:

                        index = np.where( samples_present_array == i )[0][0]

                        if deriv0:

                            # freq_mask = np.where( (np.array( data[0] ) <= upper_bound) & (np.array( data[0] ) >= lower_bound) )[0]
                            #
                            # plt.plot( np.array( data[7] )[freq_mask], np.array( data[8][index] )[freq_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                            plt.scatter( np.array( data[7][index] ), np.arctan( np.array( data[8][index] ) ), label = resin_data.loc[i]["Label"], color = colours[i] )

                        if deriv1:

                            freq_mask = np.where( (np.array( first_derivative_data[0] ) <= upper_bound) & (np.array( first_derivative_data[0] ) >= lower_bound) )[0]

                            plt.plot( np.array( first_derivative_data[0] )[freq_mask], np.array( first_derivative_data[5][index] )[freq_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                        if deriv2:

                            freq_mask = np.where( (np.array( second_derivative_data[0] ) <= upper_bound) & (np.array( second_derivative_data[0] ) >= lower_bound) )[0]

                            plt.plot( np.array( second_derivative_data[0] )[freq_mask], np.array( second_derivative_data[7][index] )[freq_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

            if log_graph:

                ax = plt.gca()
                ax.set_xscale( 'log' )
                ax.set_yscale( 'log' )

            # plt.legend( ncol = 3, bbox_to_anchor = ( 1.010, 0 ), loc = 'center', borderaxespad = 0 )
            leg = ax.get_legend()

            # for lh in leg.legendHandles:
            #
            #     lh.set_alpha(1)

            # plt.legend( ncol = 2, loc = 'upper right', borderaxespad = 0 )
            # plt.legend()

            # plt.xlabel( "Angular Frequency" )
            # plt.ylabel( "Complex Viscosity" )

            plt.tight_layout()

            # For overall pipeline figure.

            # ax = plt.gca()
            # ax.get_legend().remove()
            # plt.xlabel( "" )
            # plt.ylabel( "" )
            # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
            # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

            if savefig:

                plt.savefig( output_directory + "Rheology/Plots/Plot.pdf" )

            else:

                plt.show()

            plt.close()

            if data_extraction:

                array = data_extraction[0][:, np.newaxis]

                for i in range( 1, len( data_extraction ) ):

                    array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

                np.savetxt( output_directory + "Plot_Coords/Unnamed.txt", array )
