# Imports.

from . import Preprocessing
from . import Utilities as util
from . import TGA_plotting

# Main function definition.

def TGA_Analysis_Main( ip ):

    file_data, data = [], []

    if ip.read_files:

        file_data, data = Preprocessing.read_files_and_preprocess( ip.directory, ip.data_directory, ip.merge_groups )

    if ip.write_csv:

        Preprocessing.write_csv( ip.output_directory, file_data, data )

    if ip.read_csv:

        file_data, data = Preprocessing.read_csv( ip.directory, ip.output_directory, ip.merge_groups )

    # Data of form [[Time], Temp, [Weight (mg)], [Weight %], [Derivative Weight %/Temp]].

    print( str( len( data[3] ) ) + " files have been read." )

    if len( data[3] ) != 53:

        print( "Warning: 53 files have not been read." )

    if ip.remove_files:

        Preprocessing.remove_files( file_data, data )

    if ip.compute_mean:

        Preprocessing.compute_mean( ip.output_directory, file_data, data )

    if ip.read_mean:

        Preprocessing.read_mean( ip.output_directory, data )

    # Data now of form [..., [m]].

    if ip.derivative:

        first_derivative_data = util.compute_derivatives( data, width = 50 )
        second_derivative_data = util.compute_derivatives( first_derivative_data )

    if ip.extract_features:

        util.extract_TGA_features( ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )

    if ip.read_and_analyse_features:

        util.read_and_analyse_TGA_features( ip, file_data )

    if ip.plot_data:

        TGA_plotting.plot_data( ip.directory, ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )

    if ip.sandbox:

        util.sandbox( ip.directory, ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )
