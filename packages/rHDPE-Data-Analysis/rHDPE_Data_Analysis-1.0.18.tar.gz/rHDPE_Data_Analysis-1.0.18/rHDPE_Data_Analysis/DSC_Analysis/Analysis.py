# Imports.

from . import Preprocessing
from . import Utilities as util
from . import DSC_plotting

# Main function definition.

def DSC_Analysis_Main( ip ):

    file_data, data = [], []

    if ip.read_files:

        file_data, data = Preprocessing.read_files_and_preprocess( ip.directory, ip.data_directory, ip.merge_groups )

    if ip.write_csv:

        Preprocessing.write_csv( ip.output_directory, file_data, data )

    if ip.read_csv:

        file_data, data = Preprocessing.read_csv( ip.directory, ip.output_directory, ip.merge_groups )

    # Data of form [Temp_2, [HF_2], Temp_4, [HF_4]].

    print( str( len( data[1] ) ) + " files have been read." )

    if len( data[1] ) != 159:

        print( "Warning: 159 files have not been read." )

    if ip.remove_files:

        Preprocessing.remove_files( file_data, data )

    if ip.compute_mean:

        Preprocessing.compute_mean( ip.output_directory, file_data, data )

    if ip.read_mean:

        Preprocessing.read_mean( ip.output_directory, data )

    # Data now of form [Temp_2, [HF_2], Temp_4, [HF_4], [HF_2_Means], [HF_4_Means]].

    if ip.derivative:

        first_derivative_data = util.compute_derivatives( data, width = 150 )
        second_derivative_data = util.compute_derivatives( first_derivative_data, width = 50 )

    if ip.extract_features:

        util.extract_DSC_features( ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )

    if ip.read_and_analyse_features:

        util.read_and_analyse_features( ip, file_data )

    data_to_plot = []

    if ip.plot_data:

        data_to_plot = DSC_plotting.plot_data( ip.directory, ip.output_directory, file_data, data, first_derivative_data, second_derivative_data, ip.shiny, ip.shiny_samples_to_plot, ip.shiny_split )

    if ip.sandbox:

        util.sandbox( ip.directory, ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )

    return data_to_plot
