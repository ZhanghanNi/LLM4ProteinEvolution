import os
from Bio import PDB

def collect_sequences_from_pdb(directory):
    parser = PDB.PDBParser()
    sequences = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
  
        filepath = os.path.join(directory, filename)
        try:
            # Parse the PDB file
            structure = parser.get_structure('PDB', filepath)
            for model in structure:
                for chain in model:
                    sequence = ''
                    for residue in chain.get_residues():
                        if PDB.is_aa(residue):  # Check if it is an amino acid
                            sequence += PDB.Polypeptide.three_to_one(residue.get_resname())
                    sequences.append((filename, chain.id, sequence))
        except Exception as e:
            print(f"Failed to parse {filename}: {e}")

    return sequences

# Specify the directory containing PDB files
pdb_directory = "/home/tonyni/ESM3/protein-gym/ESM3_substitution_results/Artificial_Single_noText_CATR_CHLRE_Tsuboyama_2023_2AMI"
sequences = collect_sequences_from_pdb(pdb_directory)

# Print the collected sequences
for file, chain_id, seq in sequences:
    print(f"File: {file}, Chain: {chain_id}, Sequence: {seq}")
