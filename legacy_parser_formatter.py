"""
This module contains the logic to format a Stanza constituency parse tree
into the legacy LISP-style string format used by the BerkeleyParser.
This allows the modern Stanza parser to be a drop-in replacement.
"""
import re

# Map Stanza UPOS tags to the legacy BerkeleyParser tagset.
TAG_MAP = {
    "ADJ": "ADJA",
    "ADP": "APPR",
    "ADV": "ADV",
    "AUX": "VAFIN",
    "CCONJ": "KON",
    "DET": "ART",
    "NOUN": "NN",
    "NUM": "CARD",
    "PART": "PTKANT",
    "PRON": "PPER",
    "PROPN": "NE",
    "PUNCT": "PUNCT", # Keep punctuation tag for regex step
    "SCONJ": "KOUS",
    "VERB": "VVFIN",
    "X": "FM",
    # Phrasal tags (mostly pass-through)
    "VROOT": "S",
    "PN": "PN",
    "S": "S",
    "NP": "NP",
    "PP": "PP",
    "AP": "AP",
    "CS": "CS",
    "VP": "VP",
    # Manual overrides based on diff
    "PDS": "PDS", # For words like 'Dies'
    "PDAT": "PDAT", # For words like 'diesen'
    "VVINF": "VVINF", # For infinitive verbs like 'machen'
}

def format_tree(tree):
    """
    Recursively traverses a Stanza constituency tree and formats it
    to look like the BerkeleyParser output.
    """
    if not tree.children:
        # This is a leaf node (a word)
        # Stanza's constituency tree leaves have the word as their label.
        return tree.label

    children_str = " ".join([format_tree(child) for child in tree.children])
    label = TAG_MAP.get(tree.label, tree.label)
    # Avoid wrapping single-child nodes in redundant S tags from Stanza
    if label == 'S' and len(tree.children) == 1:
        return children_str
    return f"({label} {children_str})"

def post_process_parse_string(parse_string):
    """
    Applies final regex-based transformations to the parse string to
    handle punctuation and other formatting quirks.
    """
    # Combine all sentence trees under a single (PSEUDO ...) block
    final_output = f"( (PSEUDO {parse_string}) )"
    
    # Use a regular expression to find punctuation marks that are standalone
    # tokens and attach them to the preceding word.
    # Example: (NN Welt) (PUNCT .) -> (NN Welt.)
    final_output = re.sub(r'\)\s+\(PUNCT\s+([^\)]+)\)', r'\1)', final_output)
    
    return final_output
