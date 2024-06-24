import os
import pandas as pd

# Directory containing the CSV files
input_dir = '../Daten/oszi'
output_dir = '../Daten/clean'

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each CSV file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        # Construct full file path
        file_path = os.path.join(input_dir, filename)
        
        # Load the CSV file, using the first line as the header
        data = pd.read_csv(file_path, skiprows=1)
        
        # Drop rows with missing values
        data = data.dropna()
        
        # Save the cleaned data to a new CSV file in the output directory
        output_path = os.path.join(output_dir, filename)
        data.to_csv(output_path, index=False)
        
        print(f"Processed and cleaned {filename}")

print("All files have been processed and cleaned.")