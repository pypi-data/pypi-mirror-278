# Imports.

import numpy as np

from . import DSC_plotting

from .. import Global_Utilities as gu

# Function definitions.

def compute_derivatives( data, width = 1 ):
    '''Compute the derivatives.'''

    derivative_data = [data[0][width: -width], [], data[2][width: -width], [], [], []]

    for i in range( len( data[1] ) ):

        derivative_data[1].append( gu.derivative( data[0], data[1][i], width ) )
        derivative_data[3].append( gu.derivative( data[2], data[3][i], width ) )

    for i in range( len( data[4] ) ):

        derivative_data[4].append( gu.derivative( data[0], data[4][i], width ) )
        derivative_data[5].append( gu.derivative( data[2], data[5][i], width ) )

    return derivative_data

def half_peak_width( temp, heat_flow, melt = False ):

    heat_flow_array = np.array( heat_flow )
    temp_array = np.array( temp )

    if not melt:

        peak = heat_flow_array.max()

    else:

        peak = heat_flow_array.min()

    half_peak = peak / 2

    if not melt:

        mask = np.where( heat_flow_array >= half_peak )[0]

    else:

        mask = np.where( heat_flow_array <= half_peak )[0]

    new_temp = temp_array[mask]

    temp_max = new_temp.max()
    temp_min = new_temp.min()

    return temp_max - temp_min

def extract_DSC_features( output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    # Temp and Heat Flow of maximum of cryst second derivative between 120-130.

    feature_1, feature_2 = [], []

    temp_mask = np.where( (np.array( second_derivative_data[0] ) <= 130) & (np.array( second_derivative_data[0] ) >= 120) )[0]

    for i in range( len( file_data ) ):

        array = np.array( second_derivative_data[1][i] )[temp_mask]

        feature_1.append( array.max() )
        feature_2.append( np.array( second_derivative_data[0] )[temp_mask][np.argmax( array )] )

    features = np.array( feature_1 )[:, np.newaxis]

    features = np.hstack( (features, np.array( feature_2 )[:, np.newaxis]) )

    feature_names = ["DSC_HFC_120", "DSC_TC_120"]

    # Minimum of cryst first derivative between 80 and 90.

    feature_1 = []

    temp_mask = np.where( (np.array( first_derivative_data[0] ) <= 90) & (np.array( first_derivative_data[0] ) >= 80) )[0]

    for i in range( len( file_data ) ):

        array = np.array( first_derivative_data[1][i] )[temp_mask]

        feature_1.append( array.min() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_HFC_80" )

    # Temp and Heat Flow at maximum cryst heat flow and maximum melt heat flow.

    feature_1, feature_2, feature_3, feature_4 = [], [], [], []

    for i in range( len( file_data ) ):

        feature_1.append( data[0][np.argmax( np.array( data[1][i] ) )] )
        feature_2.append( np.array( data[1][i] ).max() )
        feature_3.append( data[2][np.argmin( np.array( data[3][i] ) )] )
        feature_4.append( np.array( data[3][i] ).min() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis], np.array( feature_2 )[:, np.newaxis], np.array( feature_3 )[:, np.newaxis], np.array( feature_4 )[:, np.newaxis]) )

    feature_names.append( "DSC_TC_Max" )
    feature_names.append( "DSC_HFC_Max" )
    feature_names.append( "DSC_TM_Max" )
    feature_names.append( "DSC_HFM_Max" )

    # Max second derivative between 160 and 170.

    feature_1 = []

    temp_mask = np.where( (np.array( second_derivative_data[2] ) <= 170) & (np.array( second_derivative_data[2] ) >= 160) )[0]

    for i in range( len( file_data ) ):

        array = np.array( second_derivative_data[3][i] )[temp_mask]

        feature_1.append( array.max() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_HFM_160" )

    # Cryst and melt half-peak widths.

    feature_1, feature_2 = [], []

    for i in range( len( file_data ) ):

        feature_1.append( half_peak_width( data[0], data[1][i] ) )
        feature_2.append( half_peak_width( data[2], data[3][i], melt = True ) )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis], np.array( feature_2 )[:, np.newaxis]) )

    feature_names.append( "DSC_C_HalfPeak" )
    feature_names.append( "DSC_M_HalfPeak" )

    # Minimum of cryst second derivative between 102 and 106.

    feature_1 = []

    temp_mask = np.where( (np.array( second_derivative_data[0] ) <= 106) & (np.array( second_derivative_data[0] ) >= 102) )[0]

    for i in range( len( file_data ) ):

        array = np.array( second_derivative_data[1][i] )[temp_mask]

        feature_1.append( array.min() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_HFC_102" )

    # Cryst onset temperature.

    feature_1 = []

    for i in range( len( file_data ) ):

        feature_1.append( first_derivative_data[0][np.where( (np.array( first_derivative_data[1][i] ) < -0.2) )[0][0]] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_C_Onset" )

    # Melt onset temperature.

    feature_1 = []

    temp_mask = np.where( (np.array( first_derivative_data[2] ) <= 145) )[0]

    for i in range( len( file_data ) ):

        array = np.where( (np.array( first_derivative_data[3][i] )[temp_mask] > 0.1) )[0]

        feature_1.append( np.array( first_derivative_data[2] )[temp_mask][array[len( array ) - 1]] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_M_Onset" )

    df = gu.array_with_column_titles_to_df( features, feature_names )

    df.to_csv( output_directory + "DSC/Features/Features.csv" )

def read_and_analyse_features( ip, file_data ):

    add_crystallinity = True

    plot_specimen_bars = False
    plot_mean_bars = False
    plot_specimen_features = True
    plot_mean_features = True
    plot_specimen_distance_matrix = True
    plot_mean_distance_matrix = True
    plot_specimen_dendrogram = True
    plot_mean_dendrogram = True

    resin_data = gu.get_list_of_resins_data( ip.directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "DSC/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    if not ip.sample_mask:

        ip.sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    sample_mask = ip.sample_mask

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    if not ip.feature_selection:

        # ip.feature_selection = [i for i in range( len( feature_names ) )]
        ip.feature_selection = [7, 8, 9, 10]

    feature_selection = ip.feature_selection

    features = features[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features = features[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    feature_weights = [1 for i in range( len( feature_selection ) )]

    gu.normalise_features( features, feature_weights )

    mean_features = gu.extract_mean_features( features, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    if add_crystallinity:

        crystallinity = [0, 65.5, 64.3, 66, 64.1, 61.3, 61.8, 62.6, 58.5, 61.7, 60.7, 60, 68.2, 60.5, 65.2, 74.1, 66.3, 69, 59.4, 73, 62.4, 62.5, 61.2, 51.1, 66.7]

        mean_features, mean_feature_names = gu.add_mean_feature( mean_features, mean_feature_names, sample_mask, crystallinity, "DSC_Crystallininty", weight = 1 )

    std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

    if add_crystallinity:

        std_of_features = np.hstack( (std_of_features, np.zeros( len( sample_mask ) )[:, np.newaxis]) )

    distance_matrix = gu.distance_matrix_from_features( features )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "DSC/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "DSC/Features/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( ip.output_directory + "DSC/Features/Distance_Matrix.csv" )

    if plot_specimen_bars:

        for i in range( len( features[0] ) ):

            gu.plot_barchart_of_feature( features[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = ip.output_directory + "DSC/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    if plot_mean_bars:

        for i in range( len( mean_features[0] ) ):

            gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = ip.output_directory + "DSC/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

    if plot_specimen_features:

        gu.plot_features( ip.output_directory, features, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "DSC/Features/", title = "Specimen_Features.pdf" )

    if plot_mean_features:

        gu.plot_features( ip.output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "DSC/Features/", title = "Means_Features.pdf" )

    if plot_specimen_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "DSC/Features/", title = "Specimen_Distance_Matrix.pdf" )

    if plot_mean_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "DSC/Features/", title = "Means_Distance_Matrix.pdf" )

    if plot_specimen_dendrogram:

        gu.plot_dendrogram( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, subdirectory = "DSC/Features/", title = "Specimen_Dendrogram.pdf" )

    if plot_mean_dendrogram:

        gu.plot_dendrogram( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "DSC/Features/", title = "Means_Dendrogram.pdf" )

def comparison_with_virgin( directory, output_directory, file_data, data ):

    resin_data = gu.get_list_of_resins_data( directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    mask = np.where( sample_array == 24 )[0]

    range_c, high_point_c, low_point_c, median_c, mean_c, std_c = gu.compute_range_mean_std( data[1], mask )
    range_m, high_point_m, low_point_m, median_m, mean_m, std_m = gu.compute_range_mean_std( data[3], mask )

    virgin_median_c = np.array( median_c )
    virgin_median_m = np.array( median_m )

    integral_c = np.zeros( len( sample_mask ) )
    integral_m = np.zeros( len( sample_mask ) )

    for i, s in enumerate( sample_mask ):

        mask = np.where( sample_array == s )[0]

        range_c, high_point_c, low_point_c, median_c, mean_c, std_c = gu.compute_range_mean_std( data[1], mask )
        range_m, high_point_m, low_point_m, median_m, mean_m, std_m = gu.compute_range_mean_std( data[3], mask )

        median_c = np.array( median_c )
        median_m = np.array( median_m )

        abs_dist_c = np.absolute( virgin_median_c - median_c )
        abs_dist_m = np.absolute( virgin_median_m - median_m )

        integral_c[i] = gu.integral_3( np.array( abs_dist_c ), 0.1 )
        integral_m[i] = gu.integral_3( np.array( abs_dist_m ), 0.1 )

    gu.plot_barchart_of_feature( integral_c, [resin_data.loc[i]["Label"] for i in sample_mask], colour = True, colour_mask = sample_mask, filename = output_directory + "DSC/Sandbox/Virgin_Comparison/BarCrystV.pdf", savefig = True )
    gu.plot_barchart_of_feature( integral_m, [resin_data.loc[i]["Label"] for i in sample_mask], colour = True, colour_mask = sample_mask, filename = output_directory + "DSC/Sandbox/Virgin_Comparison/BarMeltV.pdf", savefig = True )
    gu.plot_scatterplot_of_two_features( integral_c, integral_m, sample_mask, [resin_data.loc[i]["Label"] for i in sample_mask], savefig = True, filename = output_directory + "DSC/Sandbox/Virgin_Comparison/VarianceCorrV.pdf" )

def variance_analysis( directory, output_directory, file_data, data ):

    resin_data = gu.get_list_of_resins_data( directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    num_samples = len( sample_mask )

    max_range_c = np.zeros( len( data[1][0] ) )
    max_range_m = np.zeros( len( data[3][0] ) )

    integral_c = np.zeros( num_samples )
    integral_m = np.zeros( num_samples )

    for i, s in enumerate( sample_mask ):

        mask = np.where( sample_array == s )[0]

        range_c, high_point_c, low_point_c, median_c, mean_c, std_c = gu.compute_range_mean_std( data[1], mask )
        range_m, high_point_m, low_point_m, median_c, mean_m, std_m = gu.compute_range_mean_std( data[3], mask )

        DSC_plotting.plot_variance( output_directory, data, mask, s, std_c, std_m )

        if len( mask ) >= 3:

            integral_c[i] = gu.integral_3( np.array( std_c ), 0.1 )
            integral_m[i] = gu.integral_3( np.array( std_m ), 0.1 )

        for a, r in enumerate( np.array( range_c ) ):

            if r > max_range_c[a]:

                max_range_c[a] = r

        for a, r in enumerate( np.array( range_m ) ):

            if r > max_range_m[a]:

                max_range_m[a] = r

    DSC_plotting.plot_maximum_range( output_directory + "DSC/Sandbox/Variance/", data, max_range_c, max_range_m )

    DSC_plotting.plot_variance_barchart_and_variance_correlation( output_directory + "DSC/Sandbox/Variance/", integral_c, integral_m, sample_mask )

def identify_anomalies( file_data, data ):

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    for s in sample_mask:

        mask = np.where( sample_array == s )[0]

        if len( mask ) < 3:

            print( "Less than three specimens of sample {} so no specimens removed".format( s ) )

            continue

        for i in mask:

            anomalous_cryst, anomalous_melt = False, False

            other_specimens = [j for j in mask if j != i]

            range_s, high_point, low_point, median, mean, std = gu.compute_range_mean_std( data[1], other_specimens )

            for j in range( len( data[1][0] ) ):

                value = data[1][i][j]

                error = 0.6 + 3 * std[j]

                if value < mean[j] - error or value > mean[j] + error:

                    anomalous_cryst = True

                    print( file_data[i][2], "should be removed due to value {} during crystallisation at {}".format( value, data[0][j] ) )

                    for l in mask:

                        print( data[1][l][j] )

                    print( mean[j], error )

                    break

            range_s, high_point, low_point, median, mean, std = gu.compute_range_mean_std( data[3], other_specimens )

            for j in range( len( data[3][0] ) ):

                value = data[3][i][j]

                error = 0.6 + 3 * std[j]

                if value < mean[j] - error or value > mean[j] + error:

                    anomalous_melt = True

                    print( file_data[i][2], "should be removed due to value {} during melt at {}".format( value, data[2][j] ) )

                    for l in mask:

                        print( data[3][l][j] )

                    print( mean[j], error )

                    break

            if anomalous_melt and anomalous_cryst:

                print( file_data[i], "should be removed." )

def sandbox( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    distance_to_virgin = False

    perform_variance_analysis = True # Perform computations relating to variance.

    perform_identify_anomalies = False

    if distance_to_virgin:

        comparison_with_virgin( directory, output_directory, file_data, data )

    if perform_variance_analysis:

        variance_analysis( directory, output_directory, file_data, data )

    if perform_identify_anomalies:

        identify_anomalies( file_data, data )
