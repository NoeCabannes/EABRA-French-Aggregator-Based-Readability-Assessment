from lexical_diversity import lex_div as ld
from eabra.aggregators import aggregate_feature_dict

def extract(doc):
    """
    Extracts Lexical variables.
    Currently implements a subset of Lexical diversity variables.
    Equivalent to FABRA Family: Lexical Variables
    """
    features = {}
    
    # We will compute lexical diversity on a document level first, 
    # but the aggregators expect arrays (e.g., per sentence). 
    # In FABRA, TTR is computed considering all tokens in the text, 
    # and there's no aggregator needed if it's a single value per text.
    # We will simulate this by returning single values.
    
    # Let's extract tokens for lexical diversity
    tokens = [token.text.lower() for token in doc if not token.is_punct and not token.is_space]
    lemmas = [token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space]
    
    if len(tokens) == 0:
        return {}
    
    # LEXdvrWLT: TTR of all types of lemma forms of all words in the text
    ttr_lemma = ld.ttr(lemmas)
    
    # LEXdvrWLD: MTLD of all types of lemma forms of all words in the text
    mtld_lemma = ld.mtld(lemmas)
    
    # LEXdvrWLL: LogTTR of all types of lemma forms
    log_ttr_lemma = ld.log_ttr(lemmas)

    # Surface forms
    ttr_surface = ld.ttr(tokens)
    mtld_surface = ld.mtld(tokens)
    log_ttr_surface = ld.log_ttr(tokens)
    
    # Note: These are text-level features, not aggregated over sentences, 
    # so we return them directly without 'aggregate_feature_dict' unless we compute them per sentence
    features.update({
        'LEXdvrWLT': ttr_lemma,
        'LEXdvrWLD': mtld_lemma,
        'LEXdvrWLL': log_ttr_lemma,
        'LEXdvrWST': ttr_surface,
        'LEXdvrWSD': mtld_surface,
        'LEXdvrWSL': log_ttr_surface,
    })
    
    return features
