# import pandas as pd

# def select_closest_to_median(df):
#     """Select the entry closest to the median sequence length for each EC number."""
#     # Calculate the median length for each EC group
#     median_lengths = df.groupby('EC Number')['Length'].median().reset_index(name='Median Length')
#     # Merge median lengths back to the original dataframe
#     df = pd.merge(df, median_lengths, on='EC Number')
#     # Calculate the absolute difference from the median
#     df['Diff from Median'] = (df['Length'] - df['Median Length']).abs()
#     # Sort by difference and keep the first entry which is closest to the median
#     df = df.sort_values(by=['EC Number', 'Diff from Median'])
#     # Drop duplicates to keep only the entry closest to the median for each EC number
#     return df.drop_duplicates(subset='EC Number', keep='first')

# def csv_to_fasta(csv_file, fasta_file):
#     # Load the CSV file into a DataFrame
#     df = pd.read_csv(csv_file)

#     # Select the entry closest to the median sequence length for each EC number
#     df = select_closest_to_median(df)
    
#     # Open the FASTA file to write
#     with open(fasta_file, 'w') as fasta:
#         for index, row in df.iterrows():
#             # Create a FASTA header with EC number
#             header = f">{row['EC Number']} | {row['Entry Name']} | {row['Organism']}"
#             # Write the header and sequence to the FASTA file
#             fasta.write(f"{header}\n{row['Sequence']}\n")

# def main():
#     csv_file = 'enzyme_data_combined.csv'  # Input CSV file
#     fasta_file = 'sampled_enzymes.fasta'  # Output FASTA file
#     csv_to_fasta(csv_file, fasta_file)
#     print(f"Sampling by median length complete. The FASTA file is saved as {fasta_file}")

# if __name__ == "__main__":
#     main()


# import pandas as pd

# def count_unique_ec_numbers(csv_file):
#     # Load the CSV file into a DataFrame
#     df = pd.read_csv(csv_file)
    
#     # Count unique EC numbers
#     unique_count = df['EC Number'].nunique()
    
#     return unique_count

# def main():
#     csv_file = 'enzyme_data_combined.csv'  # Input CSV file
#     unique_ec_numbers = count_unique_ec_numbers(csv_file)
#     print(f"The number of unique EC numbers in the file is: {unique_ec_numbers}")

# if __name__ == "__main__":
#     main()





import pandas as pd

def select_closest_to_median(df, num_samples=3):
    """Select the entry closest to the median sequence length for each EC number."""
    # Calculate the median length for each EC group
    median_lengths = df.groupby('EC Number')['Length'].median().reset_index(name='Median Length')
    # Merge median lengths back to the original dataframe
    df = pd.merge(df, median_lengths, on='EC Number')
    # Calculate the absolute difference from the median
    df['Diff from Median'] = (df['Length'] - df['Median Length']).abs()
    # Sort by difference and keep the first entries which are closest to the median
    df = df.sort_values(by=['EC Number', 'Diff from Median'])
    # Drop duplicates to keep only the specified number of entries closest to the median for each EC number
    return df.groupby('EC Number').head(num_samples)

def csv_to_fasta(csv_file, output_directory):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Select the entries closest to the median sequence length for each EC number
    df = select_closest_to_median(df)

    # Group by third-level EC number (assuming EC number format is x.x.x)
    grouped = df.groupby(df['EC Number'].str.extract(r'(\d+\.\d+\.\d+)')[0])

    # Create a FASTA file for each third-level EC number group
    for ec_third_level, group in grouped:
        fasta_file = f"{output_directory}/{ec_third_level}.fasta"
        with open(fasta_file, 'w') as fasta:
            for index, row in group.iterrows():
                # Create a FASTA header with EC number
                header = f">{row['EC Number']}_{row['Entry Name']}_{row['Organism']}"
                # Write the header and sequence to the FASTA file
                fasta.write(f"{header}\n{row['Sequence']}\n")
            print(f"FASTA file created for EC {ec_third_level} at: {fasta_file}")

def main():
    csv_file = 'enzyme_data_combined.csv'  # Specify your input CSV file
    output_directory = 'fasta_files'  # Specify your output directory for FASTA files
    csv_to_fasta(csv_file, output_directory)

if __name__ == "__main__":
    main()
