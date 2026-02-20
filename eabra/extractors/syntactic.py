from eabra.aggregators import aggregate_feature_dict

def get_tree_depth(token):
    """Recursively calculates the depth of the dependency tree starting from a token."""
    if not list(token.children):
        return 1
    return 1 + max(get_tree_depth(child) for child in token.children)

def extract(doc):
    """
    Extracts Syntactic variables.
    Equivalent to FABRA Family: Syntactic Variables
    """
    features = {}
    
    # Language development (Sentence Depth)
    # SYNdevHGT: sentence depth in the text.
    sentence_depths = []
    
    # Dependency Relations
    # SYNdepNSUBJ, SYNdepOBJ, SYNdepAMOD, etc.
    # We will count these per sentence and aggregate
    
    # Initialize trackers
    dep_counts = {
        'nsubj': [], 'obj': [], 'amod': [], 'advmod': [], 
        'ccomp': [], 'xcomp': [], 'aux': [], 'punct': []
    }
    
    for sent in doc.sents:
        # Sentence depth
        root = sent.root
        sentence_depths.append(get_tree_depth(root))
        
        # Dependency relation counts for this sentence
        sent_dep_counts = {k: 0 for k in dep_counts.keys()}
        for token in sent:
            dep = token.dep_.lower()
            if dep in sent_dep_counts:
                sent_dep_counts[dep] += 1
                
        # Append to document trackers
        for k in dep_counts.keys():
            dep_counts[k].append(sent_dep_counts[k])
            
    # Aggregate Language Development features
    features.update(aggregate_feature_dict('SYNdevHGT', sentence_depths))
    
    # Aggregate Dependency Relations
    for dep, counts in dep_counts.items():
        feat_name = f"SYNdep{dep.upper()}"
        features.update(aggregate_feature_dict(feat_name, counts))
        
    return features
