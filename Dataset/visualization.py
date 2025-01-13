from Bio import Phylo

# Path to the Newick tree file
tree_file_path = "/home/tonyni/ESM3/EC/1.1.1.treefile"
pruned_tree_file_path = "/home/tonyni/ESM3/EC/1.1.1.treefile.pruned.noDup"

# Load the Newick tree from the file
tree = Phylo.read(tree_file_path, "newick")

def collapse_monophyletic_groups(clade):
    # This function is designed to work recursively
    if not clade.clades:  # If no sub-clades, it's a leaf
        return

    if len(clade.clades) == 2:  # Check if it's a binary node
        child1, child2 = clade.clades
        if not child1.clades and not child2.clades:  # Both are leaves
            ec1 = child1.name.split('_')[0] if '_' in child1.name else None
            ec2 = child2.name.split('_')[0] if '_' in child2.name else None
            if ec1 == ec2 and ec1 is not None:
                # Collapse the node
                new_name = f"{ec1}_cluster"
                clade.name = new_name
                clade.clades = []  # Remove children

    # Recursive call for all sub-clades that still exist
    for subclade in clade.clades:
        collapse_monophyletic_groups(subclade)

# Start the processing from the root
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)
collapse_monophyletic_groups(tree.root)

def remove_leaves(tree, keyword):
    # Create a list of leaves to remove
    to_remove = [leaf for leaf in tree.get_terminals() if keyword not in leaf.name]
    
    # Remove the specified leaves
    for leaf in to_remove:
        tree.prune(leaf)


remove_leaves(tree, "cluster")


def remove_cluster_suffix(tree):
    # Iterate through each terminal node (leaf)
    for leaf in tree.get_terminals():
        # Replace '_cluster' with an empty string in the leaf name
        if '_cluster' in leaf.name:
            leaf.name = leaf.name.replace('_cluster', '')


remove_cluster_suffix(tree)



from collections import Counter
def remove_duplicate_leaves(tree):
    # Find all leaf names
    leaf_names = [leaf.name for leaf in tree.get_terminals()]
    
    # Count each name
    name_count = Counter(leaf_names)
    
    # Find names that appear more than once
    duplicates = [name for name, count in name_count.items() if count > 1]
    
    # Create a list of all leaves to be removed (all instances of duplicates)
    to_remove = [leaf for leaf in tree.get_terminals() if leaf.name in duplicates]
    
    # Remove the specified leaves
    for leaf in to_remove:
        tree.prune(leaf)

remove_duplicate_leaves(tree)


# Save the modified tree to a new file
Phylo.write(tree, pruned_tree_file_path, "newick")

print(f"Modified tree saved to {pruned_tree_file_path}")

