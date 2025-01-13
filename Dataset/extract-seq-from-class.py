import pandas as pd

def extract_sequences_for_ec_number(file_path, ec_number, output_file):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Filter the DataFrame for the specified EC number
    filtered_df = df[df['EC Number'] == ec_number]

    # Get the sequences
    sequences = filtered_df['Sequence'].tolist()

    # Save the sequences to a text file, each sequence on a new line
    with open(output_file, "w") as file:
        for sequence in sequences:
            file.write(sequence + "\n")

    print(f"Sequences for EC Number {ec_number} have been saved to {output_file}.")

# Example usage
file_path = "/home/tonyni/ESM3/EC/1.1.1.csv"
ec_number = "1.1.1.14"  # Specify the EC number you want to extract
output_file = "/home/tonyni/ESM3/EC/sequences_1.1.1.14.txt"
extract_sequences_for_ec_number(file_path, ec_number, output_file)
