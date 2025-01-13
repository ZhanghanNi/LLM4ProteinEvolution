import requests
import pandas as pd

def generate_ec_numbers():
    """Generate EC numbers."""
    ranges = {'1.1.1': 120}
    return [f'{key}.{i}' for key, count in ranges.items() for i in range(1, count + 1)]

def fetch_uniprot_metadata(ec_number):
    """Fetch metadata for EC number."""
    url = f"https://rest.uniprot.org/uniprotkb/search?query=ec:{ec_number}&format=tsv"
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def fetch_uniprot_sequence(ec_number):
    """Fetch sequence for EC number."""
    url = f"https://rest.uniprot.org/uniprotkb/search?query=ec:{ec_number}&format=tsv&fields=sequence,length"
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def main():
    ec_numbers = generate_ec_numbers()
    results = []

    for ec in ec_numbers:
        metadata = fetch_uniprot_metadata(ec)
        sequence_data = fetch_uniprot_sequence(ec)

        if metadata and sequence_data:
            meta_lines = metadata.strip().split('\n')
            seq_lines = sequence_data.strip().split('\n')

            meta_header = meta_lines[0].split('\t')
            seq_header = seq_lines[0].split('\t')

            for meta_line, seq_line in zip(meta_lines[1:], seq_lines[1:]):
                meta_values = meta_line.split('\t')
                seq_values = seq_line.split('\t')

                if meta_values[-1] == seq_values[-1]:  # Match lengths
                    combined = meta_values + seq_values[:-1]
                    result = dict(zip(meta_header + seq_header[:-1], combined))
                    result['EC Number'] = ec
                    results.append(result)
        else:
            results.append({'EC Number': ec, 'Data': 'Incomplete data'})

    pd.DataFrame(results).to_csv('ec_data.csv', index=False)

if __name__ == "__main__":
    main()