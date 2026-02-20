from eabra.aggregators import aggregate_feature_dict
import pyphen

dic = pyphen.Pyphen(lang='en')

def count_syllables(word):
    """Fallback simple syllable counter using pyphen."""
    return len(dic.inserted(word).split('-'))

def extract(doc):
    """
    Extracts Length-based variables.
    Equivalent to FABRA Family: Length based
    """
    features = {}
    
    # Sentence Length (Words per sentence)
    # FABRA: LENsntWRD (Number of token per sentence, excluding punctuation)
    snt_lengths = []
    for sent in doc.sents:
        # Punctuation filter
        words = [token for token in sent if not token.is_punct]
        snt_lengths.append(len(words))
    
    features.update(aggregate_feature_dict('LENsntWRD', snt_lengths))
    
    # Word Length (Letters per word, Stem, Syllables)
    # FABRA: 
    # LENwrdLETTERS Number of letters per word.
    # LENwrdSTEM Length of stem (lemma in our case) in letters per word.
    # LENwrdSYL Number of syllables per word.
    word_lengths = []
    lemma_lengths = []
    syl_counts = []
    
    for token in doc:
        if token.is_punct or token.is_space:
            continue
        word_lengths.append(len(token.text))
        lemma_lengths.append(len(token.lemma_))
        syl_counts.append(count_syllables(token.text.lower()))
        
    features.update(aggregate_feature_dict('LENwrdLETTERS', word_lengths))
    features.update(aggregate_feature_dict('LENwrdSTEM', lemma_lengths))
    features.update(aggregate_feature_dict('LENwrdSYL', syl_counts))

    return features
