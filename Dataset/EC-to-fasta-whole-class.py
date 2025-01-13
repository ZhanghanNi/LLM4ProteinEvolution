import pandas as pd

# Load the CSV file
df = pd.read_csv("/home/tonyni/ESM3/EC/1.1.1.csv")

# Filter for specific EC numbers
specific_ec_numbers = ['1.1.1.1', '1.1.1.14']
filtered_df = df[df['EC Number'].isin(specific_ec_numbers)]

# Select the required columns
fasta_df = filtered_df[['Sequence', 'EC Number', 'Entry']]

# Format the data into FASTA format
fasta_content = ""
for idx, row in fasta_df.iterrows():
    header = f">EC_Number_{row['EC Number']}_{row['Entry']}"
    sequence = row['Sequence']
    fasta_content += f"{header}\n{sequence}\n"

# Save to a FASTA file
with open("/home/tonyni/ESM3/EC/1.1.1.1_14.fasta", "w") as file:
    file.write(fasta_content)

print("Filtered FASTA file has been created successfully.")
