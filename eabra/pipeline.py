import spacy
import pandas as pd
from eabra.extractors import length, lexical, syntactic, discourse

class EABRAPipeline:
    def __init__(self, model="en_core_web_sm"):
        """
        Initializes the EABRA Pipeline.
        Loads the specified spaCy model.
        """
        print(f"Loading spaCy model: {model}...")
        self.nlp = spacy.load(model)
        print("EABRA Pipeline initialized.")

    def process_text(self, text):
        """
        Processes a single string of text, computing all EABRA features.
        Returns a dictionary of features.
        """
        doc = self.nlp(text)
        
        features = {}
        
        # 1. Length-based features
        features.update(length.extract(doc))
        
        # 2. Lexical features
        features.update(lexical.extract(doc))
        
        # 3. Syntactic features
        features.update(syntactic.extract(doc))
        
        # 4. Discourse features
        features.update(discourse.extract(doc))
        
        return features
    
    def process_dataframe(self, df, text_column):
        """
        Processes a pandas DataFrame containing a column of texts.
        Returns a new DataFrame with all EABRA features appended as columns.
        """
        results = []
        for idx, row in df.iterrows():
            text = row[text_column]
            feats = self.process_text(text)
            results.append(feats)
            
        feat_df = pd.DataFrame(results)
        return pd.concat([df, feat_df], axis=1)
