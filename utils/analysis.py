import os
import csv
from Bio import SearchIO

# Define the directory containing the .txt files
directory = '/workspace/data/nit/real_tree/trees_hmm'  # Replace with your directory path

# Output CSV file
output_csv = '/workspace/data/nit/real_tree/trees_hmm/hmmsearch_averages.csv'

# Initialize a list to store the results
results = []

# Iterate over all .txt files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        print(f"Processing file: {filename}")
        
        # Parse the HMMER output file
        try:
            qresults = SearchIO.parse(filepath, 'hmmer3-text')
        except Exception as e:
            print(f"Error parsing file {filename}: {e}")
            continue  # Skip this file if there's an error
        
        # Initialize lists to store E-values, scores, and biases
        evalues = []
        scores = []
        biases = []
        
        # Iterate over query results
        for qresult in qresults:
            # Iterate over hits
            for hit in qresult.hits:
                # Full sequence data is in hit.hsps
                for hsp in hit.hsps:
                    # Extract E-value, score, and bias
                    evalues.append(hsp.evalue)
                    scores.append(hsp.bitscore)
                    biases.append(hsp.bias)
        
        # Compute averages if lists are not empty
        if evalues:
            avg_evalue = sum(evalues) / len(evalues)
            avg_score = sum(scores) / len(scores)
            avg_bias = sum(biases) / len(biases)
        else:
            avg_evalue = None
            avg_score = None
            avg_bias = None
        
        # Append the results
        results.append({
            'filename': filename,
            'avg_evalue': avg_evalue,
            'avg_score': avg_score,
            'avg_bias': avg_bias
        })

# Write results to CSV
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['filename', 'avg_evalue', 'avg_score', 'avg_bias']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Results have been written to {output_csv}")
