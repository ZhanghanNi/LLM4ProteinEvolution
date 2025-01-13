import csv
from itertools import combinations

# Define ancestral sequence and amino acids
ancestral_sequence = "GLTEEQKQEIREAFDLFDTDGSGTIDAKELKVAMRALGFEPKKEEIKKMISEIDKDGSGTIDFEEFLTMMTA"
amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

def generate_mutations(sequence):
    """Generate single and double mutations."""
    single_mutations, double_mutations = [], []

    # Single mutations
    for pos in range(len(sequence)):
        original = sequence[pos]
        for aa in amino_acids:
            if aa != original:
                single_mutations.append({
                    "mutant": f"{original}{pos + 1}{aa}",
                    "mutated_sequence": sequence[:pos] + aa + sequence[pos + 1:],
                    "masked": sequence[:pos] + '_' + sequence[pos + 1:],
                    "mutation_positions": [pos + 1],
                    "number_of_mutations": 1
                })

    # Double mutations
    for pos1, pos2 in combinations(range(len(sequence)), 2):
        original1, original2 = sequence[pos1], sequence[pos2]
        for aa1 in amino_acids:
            if aa1 != original1:
                for aa2 in amino_acids:
                    if aa2 != original2:
                        double_mutations.append({
                            "mutant": f"{original1}{pos1 + 1}{aa1}:{original2}{pos2 + 1}{aa2}",
                            "mutated_sequence": sequence[:pos1] + aa1 + sequence[pos1 + 1:pos2] + aa2 + sequence[pos2 + 1:],
                            "masked": sequence[:pos1] + '_' + sequence[pos1 + 1:pos2] + '_' + sequence[pos2 + 1:],
                            "mutation_positions": [pos1 + 1, pos2 + 1],
                            "number_of_mutations": 2
                        })
    return single_mutations, double_mutations

# Generate mutations
single_mutations, double_mutations = generate_mutations(ancestral_sequence)

with open("single_mutations.csv", mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["mutant", "mutated_sequence", "masked", "mutation_positions", "number_of_mutations"])
    writer.writeheader()
    writer.writerows(single_mutations)

with open("double_mutations.csv", mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["mutant", "mutated_sequence", "masked", "mutation_positions", "number_of_mutations"])
    writer.writeheader()
    writer.writerows(double_mutations)