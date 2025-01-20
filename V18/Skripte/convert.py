import pandas as pd

def spe_to_csv(input_file, output_file):
    # Read the file content
    with open(input_file, 'r') as file:
        file_content = file.readlines()

    # Locate the $DATA section
    data_start = file_content.index('$DATA:\n') + 1
    data_range = file_content[data_start].strip()  # The range (e.g., "0 8191")
    data_lines = file_content[data_start + 1:]  # The counts data starts after the range line

    # Parse the range to determine channel numbers
    start_channel, end_channel = map(int, data_range.split())
    channels = list(range(start_channel, end_channel + 1))

    # Extract counts from data_lines and pair them with channels
    counts = [int(line.strip()) for line in data_lines[: len(channels)]]  # Trim to match the channel range

    # Create a DataFrame
    df = pd.DataFrame({"Channel": channels, "Counts": counts})

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)
    print(f"Converted file saved to: {output_file}")

# Example usage
input_file = '../Daten/Uran.Spe'  # Replace with the path to your .Spe file
output_file = '../Daten/Uran.csv'  # Replace with the desired output CSV path
spe_to_csv(input_file, output_file)
