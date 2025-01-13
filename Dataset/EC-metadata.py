import requests
import pandas as pd

def generate_ec_numbers():
    """Generate a list of EC numbers based on specified ranges."""
    ec_numbers = []
    # Defining ranges for each subclass
    ranges = {
        # '2.7.1': 239,
        # '2.7.2': 19,
        # '2.7.3': 13,
        # '2.7.4': 34
        '1.1.1' : 120,

    }
    for key, count in ranges.items():
        for i in range(1, count + 1):
            ec_numbers.append(f'{key}.{i}')
    return ec_numbers

def fetch_uniprot_metadata(ec_number):
    """Fetch metadata from UniProt for a given EC number."""
    url = f"https://rest.uniprot.org/uniprotkb/search?query=ec:{ec_number}&format=tsv"
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def fetch_uniprot_sequence(ec_number):
    """Fetch sequence data from UniProt for a given EC number."""
    url = f"https://rest.uniprot.org/uniprotkb/search?query=ec:{ec_number}&format=tsv&fields=sequence,length"
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def main():
    ec_numbers = generate_ec_numbers()
    results = []

    for ec in ec_numbers:
        metadata = fetch_uniprot_metadata(ec)
        sequence_data = fetch_uniprot_sequence(ec)
        #print(metadata)
        #print(sequence_data)

        if metadata and sequence_data:
            # Parse the TSV responses
            meta_lines = metadata.strip().split('\n')
            seq_lines = sequence_data.strip().split('\n')
            
            # Combine based on the length column
            meta_header = meta_lines[0].split('\t')
            seq_header = seq_lines[0].split('\t')

            for meta_line, seq_line in zip(meta_lines[1:], seq_lines[1:]):
                meta_values = meta_line.split('\t')
                seq_values = seq_line.split('\t')
                
                if meta_values[-1] == seq_values[-1]:  # Assuming last column is 'length' and they match
                    combined = meta_values + seq_values[:-1]  # Exclude duplicate length column from sequence data
                    result = dict(zip(meta_header + seq_header[:-1], combined))
                    result['EC Number'] = ec
                    results.append(result)
                    print(results)
        else:
            results.append({'EC Number': ec, 'Data': 'Incomplete data'})
            print("fail")

    # Save results to a CSV file
    df = pd.DataFrame(results)
    df.to_csv('1.1.1.csv', index=False)

if __name__ == "__main__":
    main()
