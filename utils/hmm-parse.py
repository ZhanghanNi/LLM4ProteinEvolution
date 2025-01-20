import os
import csv
from Bio import SearchIO

# Input directory and output file paths
directory = 'trees_hmm'
output_csv = 'hmmsearch_averages.csv'

results = []

# Process .txt files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        print(f"Processing: {filename}")
        
        try:
            qresults = SearchIO.parse(filepath, 'hmmer3-text')
        except Exception as e:
            print(f"Error in {filename}: {e}")
            continue
        
        evalues, scores, biases = [], [], []
        
        for qresult in qresults:
            for hit in qresult.hits:
                for hsp in hit.hsps:
                    evalues.append(hsp.evalue)
                    scores.append(hsp.bitscore)
                    biases.append(hsp.bias)
        
        avg_evalue = sum(evalues) / len(evalues) if evalues else None
        avg_score = sum(scores) / len(scores) if scores else None
        avg_bias = sum(biases) / len(biases) if biases else None
        
        results.append({
            'filename': filename,
            'avg_evalue': avg_evalue,
            'avg_score': avg_score,
            'avg_bias': avg_bias
        })

# Save results to CSV
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['filename', 'avg_evalue', 'avg_score', 'avg_bias']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to {output_csv}")