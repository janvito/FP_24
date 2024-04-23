import os
import csv

def convert_uxd_to_csv(input_filename, output_filename):
    with open(input_filename, 'r') as uxd_file:
        lines = uxd_file.readlines()

    start_line = lines.index('_2THETACOUNTS\n')
    theta_counts_data = [line.strip().split() for line in lines[start_line+1:]]
    theta_counts_data = [[float(entry[0]), int(entry[1])] for entry in theta_counts_data]

    with open(output_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Theta', 'Counts'])
        writer.writerows(theta_counts_data)

def batch_convert_uxd_to_csv(input_folder, output_folder):
    # Ensure the output folder exists, create if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.UXD'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.UXD', '.csv'))
            convert_uxd_to_csv(input_path, output_path)

# Set input and output folders
input_folder = '../Daten'
output_folder = '../Daten/CSV_Output'

# Convert all .uxd files in input folder to .csv files in output folder
batch_convert_uxd_to_csv(input_folder, output_folder)
