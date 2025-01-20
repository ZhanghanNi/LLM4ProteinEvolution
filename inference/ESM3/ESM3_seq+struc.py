import numpy as np
import torch
import pandas as pd
from esm.utils.types import FunctionAnnotation
from esm.utils.structure.protein_chain import ProteinChain
from esm.models.esm3 import ESM3
from esm.sdk.api import ESMProtein, GenerationConfig

# Load pre-trained model
model = ESM3.from_pretrained("esm3_sm_open_v1", device=torch.device("cuda"))

# Load data
df = pd.read_csv("artificial_single_mutations.csv")
crmsd_results = []

# Process mutations
for i in range(len(df)):
    current_protein = df.loc[i, 'mutant']
    mask_positions = eval(df.loc[i, 'mutation_positions'])
    masked_sequence = df.loc[i, 'masked']

    # Load and encode ancestral protein
    protein = ESMProtein.from_pdb("ancestor.pdb")
    protein_tensor = model.encode(protein)

    # Prepare prompts
    sequence_prompt = masked_sequence
    protein_chain_positions = protein.to_protein_chain().atom37_positions
    structure_prompt = torch.tensor(protein_chain_positions)
    for index, char in enumerate(masked_sequence):
        if char == "_":
            structure_prompt[index] = torch.tensor([np.nan, np.nan, np.nan])

    # Function annotations for generation
    function_annotations = [
        FunctionAnnotation(label="stable", start=pos, end=pos) for pos in mask_positions
    ]

    protein_prompt = ESMProtein(sequence=sequence_prompt, coordinates=structure_prompt)

    # Generate sequence
    seq_config = GenerationConfig(track="sequence", num_steps=len(mask_positions), temperature=0.7)
    seq_gen = model.generate(protein_prompt, seq_config)

    # Predict structure from generated sequence
    struct_config = GenerationConfig(track="structure", num_steps=len(seq_gen.sequence) // 8, temperature=0)
    struct_prompt = ESMProtein(sequence=seq_gen.sequence)
    struct_pred = model.generate(struct_prompt, struct_config)

    # Save generated sequence and structure
    struct_pred.to_protein_chain().to_pdb(f"{current_protein}_sequence.pdb")
    struct_gen_config = GenerationConfig(track="structure", num_steps=len(mask_positions), temperature=0.7)
    struct_gen = model.generate(protein_prompt, struct_gen_config)
    struct_gen.to_protein_chain().to_pdb(f"{current_protein}_structure.pdb")

    # Generate sequence from structure
    seq_gen_config2 = GenerationConfig(track="sequence", num_steps=len(mask_positions), temperature=0)
    protein_prompt2 = ESMProtein(coordinates=struct_gen.coordinates)
    seq_gen2 = model.generate(protein_prompt2, seq_gen_config2)

    # Calculate cRMSD
    crmsd_struc = struct_gen.to_protein_chain().rmsd(protein.to_protein_chain())
    crmsd_seq = struct_pred.to_protein_chain().rmsd(protein.to_protein_chain())

    # Append results
    crmsd_results.append({
        'Protein': current_protein,
        'cRMSD Structure': crmsd_struc,
        'cRMSD Sequence': crmsd_seq,
        'Generated Sequence': seq_gen.sequence,
        'Generated Structure Sequence': seq_gen2.sequence,
    })

# Save results
results_df = pd.DataFrame(crmsd_results)
results_df.to_csv("crmsd_results.csv", index=False)