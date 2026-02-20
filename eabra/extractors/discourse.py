from eabra.aggregators import aggregate_feature_dict

def extract(doc):
    """
    Extracts Discourse variables.
    Equivalent to FABRA Family: Discourse Variables
    """
    features = {}
    
    # Referential expressions
    # DISrefPN: Proportion of pronouns to all nouns.
    # We compute this per sentence (or document). Let's do per sentence, then aggregate.
    
    pron_props = []
    def_props = []
    
    for sent in doc.sents:
        num_nouns = sum(1 for token in sent if token.pos_ == 'NOUN')
        num_prons = sum(1 for token in sent if token.pos_ == 'PRON')
        num_words = len([t for t in sent if not t.is_punct])
        
        # definite articles (the)
        num_def = sum(1 for token in sent if token.text.lower() == 'the' and token.pos_ == 'DET')
        
        if num_nouns > 0:
            pron_props.append(num_prons / num_nouns)
            def_props.append(num_def / num_nouns)
        else:
            pron_props.append(0.0)
            def_props.append(0.0)
            
    # Aggregate
    features.update(aggregate_feature_dict('DISrefPN', pron_props))
    features.update(aggregate_feature_dict('DISrefDN', def_props))
    
    return features
