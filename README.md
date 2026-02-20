# EABRA: English Aggregator-Based Readability Assessment

EABRA is a Python toolkit designed to evaluate the readability of English texts. It is the English counterpart to the French FABRA toolkit. It automatically extracts a wide array of language features (Length, Lexical, Syntactic, and Discourse) from your text and calculates 18 statistical aggregators for each feature, providing an extremely detailed linguistic profile of the input. It resues the language variables and aggregators from FABRA.

## Features Extracted

EABRA groups its extractions into the following families:
1. **Length-based Variables**: Sentence length (words per sentence), Word length (letters per word, syllables per word).
2. **Lexical Variables**: Lexical diversity measures including TTR (Type-Token Ratio), MTLD, and LogTTR.
3. **Syntactic Variables**: Parse tree depths, and counts of Universal Dependency relations (e.g., nominal subjects, adjectival modifiers).
4. **Discourse Variables**: Referential expressions (proportion of pronouns and definite articles to nouns).

All sentence-level and word-level features are passed through **18 statistical aggregators** (Sum, Min, Max, Length, Median, Q1, Q3, 80th Percentile, 90th Percentile, Average, Mode, Variance, Standard Deviation, Relative Standard Deviation, Interquartile Range, Dolch Metric, Skewness, and Kurtosis).

---

## 🛠️ Prerequisites & Installation

### 1. Python Version
**Important:** EABRA utilizes `spaCy` under the hood for advanced NLP tasks. `spaCy` relies on compiled C-extensions. Therefore, it is highly recommended to use **Python 3.11, 3.12, or 3.13**. 
*(Using brand new versions like Python 3.14 may cause installation errors as pre-built wheels might not be available yet).*

### 2. Install Dependencies
Open your terminal or command prompt and run the following command to install the required Python libraries:

```bash
pip install spacy pydantic pyphen lexical-diversity textstat pandas scipy numpy "setuptools<70.0.0"
```

### 3. Download the spaCy Language Model
EABRA requires the English language model for `spaCy`. Download it by running:

```bash
python -m spacy download en_core_web_sm
```

---

## 🚀 How to Use EABRA

You can use EABRA to process a single text string or process an entire dataset (Pandas DataFrame) at once.

### Processing a Pandas DataFrame (Recommended)

This is the most efficient way to process multiple texts.

```python
import pandas as pd
from eabra.pipeline import EABRAPipeline

# 1. Initialize the pipeline
print("Initializing EABRA...")
pipeline = EABRAPipeline()

# 2. Prepare your data in a Pandas DataFrame
data = {
    'text_id': [1, 2],
    'text': [
        "The cat sat on the mat. It was a very nice mat. The cat liked the mat.",
        "Concurrently, the economic ramifications of implementing such a substantial quantitative easing program are profound, significantly altering the macroeconomic landscape."
    ]
}
df = pd.DataFrame(data)

# 3. Process the dataframe
# Specify the dataframe and the name of the column containing the text
print("Extracting features...")
results_df = pipeline.process_dataframe(df, text_column='text')

# 4. View results
print(f"Extraction complete! Found {len(results_df.columns)} columns.")

# Print a specific metric, e.g., Average Parse Tree Depth
print(results_df[['text_id', 'SYNdevHGT_avg']])
```

### Processing a Single Text String

```python
from eabra.pipeline import EABRAPipeline

# 1. Initialize the pipeline
pipeline = EABRAPipeline()

# 2. Process your text
text = "The quick brown fox jumps over the lazy dog."
features = pipeline.process_text(text)

# The result is a dictionary containing hundreds of aggregated features
print("Average Syllables per word:", features['LENwrdSYL_avg'])
print("Lexical Diversity (TTR):", features['LEXdvrWLT'])
```

## Troubleshooting

- **ModuleNotFoundError: No module named 'pkg_resources'**: This occurs in newer Python versions with certain libraries like `lexical-diversity`. Ensure you have installed `setuptools<70.0.0` as specified in the installation steps.
- **spaCy Build Errors**: If `pip install spacy` fails during the "Building wheels" step, ensure you are not using an unsupported or overly-new version of Python (like 3.14). Downgrading to Python 3.13 or 3.12 will fix this.

## Language variables / aggregators description

We kept the same names from FABRA. FABRA documentation is available here. https://cental.uclouvain.be/fabra/docs.html (webpage archive in PDF format can be found in the repository)
