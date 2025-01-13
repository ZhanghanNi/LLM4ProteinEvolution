from Bio import Phylo
from collections import Counter

tree_file_path = "input_tree.newick"
pruned_tree_file_path = "pruned_tree.newick"
tree = Phylo.read(tree_file_path, "newick")

def collapse_monophyletic_groups(clade):
    """Collapse monophyletic groups with the same EC number."""
    if not clade.clades:
        return
    if len(clade.clades) == 2:
        child1, child2 = clade.clades
        if not child1.clades and not child2.clades:
            ec1 = child1.name.split('_')[0] if '_' in child1.name else None
            ec2 = child2.name.split('_')[0] if '_' in child2.name else None
            if ec1 == ec2 and ec1:
                clade.name, clade.clades = f"{ec1}_cluster", []
    for subclade in clade.clades:
        collapse_monophyletic_groups(subclade)

def remove_leaves(tree, keyword):
    """Remove leaves not containing the keyword."""
    for leaf in [leaf for leaf in tree.get_terminals() if keyword not in leaf.name]:
        tree.prune(leaf)

def remove_cluster_suffix(tree):
    """Remove '_cluster' suffix from leaf names."""
    for leaf in tree.get_terminals():
        if '_cluster' in leaf.name:
            leaf.name = leaf.name.replace('_cluster', '')

def remove_duplicate_leaves(tree):
    """Remove duplicate leaves."""
    leaf_names = [leaf.name for leaf in tree.get_terminals()]
    duplicates = {name for name, count in Counter(leaf_names).items() if count > 1}
    for leaf in [leaf for leaf in tree.get_terminals() if leaf.name in duplicates]:
        tree.prune(leaf)

# Process the tree
collapse_monophyletic_groups(tree.root)
remove_leaves(tree, "cluster")
remove_cluster_suffix(tree)
remove_duplicate_leaves(tree)

Phylo.write(tree, pruned_tree_file_path, "newick")
print(f"Modified tree saved to {pruned_tree_file_path}")