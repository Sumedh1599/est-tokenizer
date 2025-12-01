#!/usr/bin/env python3
"""
Pre-Processor Block
Tokenize English words, stemming/lemmatization, phrase pattern detection, stop word filtering
"""

import re
from typing import List, Dict, Tuple

class PreProcessor:
    def __init__(self):
        """Initialize pre-processor"""
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their'
        }
        
        # Simple stemming rules (basic implementation)
        self.stemming_rules = {
            'ing': '', 'ed': '', 'er': '', 'est': '', 'ly': '',
            's': '', 'es': '', 'ies': 'y', 'ied': 'y'
        }
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Split by whitespace and punctuation
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def stem_word(self, word: str) -> str:
        """Simple stemming (can be enhanced with NLTK)"""
        word_lower = word.lower()
        
        # Apply stemming rules
        for suffix, replacement in self.stemming_rules.items():
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                return word_lower[:-len(suffix)] + replacement
        
        return word_lower
    
    def stem_text(self, text: str) -> List[str]:
        """Stem all words in text"""
        words = self.tokenize(text)
        return [self.stem_word(word) for word in words]
    
    def filter_stop_words(self, words: List[str]) -> List[str]:
        """Remove stop words"""
        return [w for w in words if w not in self.stop_words]
    
    def detect_phrases(self, text: str) -> List[Tuple[str, str]]:
        """
        Detect common phrase patterns
        Returns: List of (phrase, pattern_type) tuples
        """
        phrases = []
        text_lower = text.lower()
        
        # Common phrase patterns
        patterns = [
            (r'how to \w+', 'how_to'),
            (r'\w+ into \w+', 'into_pattern'),
            (r'\w+ and \w+', 'and_pattern'),
            (r'\w+ or \w+', 'or_pattern'),
            (r'\w+ of \w+', 'of_pattern'),
            (r'\w+ with \w+', 'with_pattern'),
            (r'\w+ from \w+', 'from_pattern'),
            (r'\w+ to \w+', 'to_pattern'),
            (r'\w+ \w+ \w+', 'three_word'),
            (r'\w+ \w+', 'two_word'),
        ]
        
        for pattern, pattern_type in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                phrases.append((match, pattern_type))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_phrases = []
        for phrase, ptype in phrases:
            if phrase not in seen:
                seen.add(phrase)
                unique_phrases.append((phrase, ptype))
        
        return unique_phrases
    
    def extract_verb_object_pairs(self, text: str) -> List[Tuple[str, str]]:
        """Extract verb-object pairs from text"""
        # Simple pattern matching for verb-object pairs
        # Pattern: verb + (article) + noun
        pattern = r'(\w+)\s+(?:a|an|the)?\s*(\w+)'
        matches = re.findall(pattern, text.lower())
        
        pairs = []
        for verb, obj in matches:
            if verb not in self.stop_words and obj not in self.stop_words:
                pairs.append((verb, obj))
        
        return pairs
    
    def process(self, text: str) -> Dict:
        """
        Complete pre-processing pipeline
        Returns: {
            'original': original text,
            'tokens': tokenized words,
            'stemmed': stemmed words,
            'filtered': filtered words (no stop words),
            'phrases': detected phrases,
            'verb_object_pairs': verb-object pairs
        }
        """
        tokens = self.tokenize(text)
        stemmed = self.stem_text(text)
        filtered = self.filter_stop_words(tokens)
        phrases = self.detect_phrases(text)
        verb_object_pairs = self.extract_verb_object_pairs(text)
        
        return {
            'original': text,
            'tokens': tokens,
            'stemmed': stemmed,
            'filtered': filtered,
            'phrases': phrases,
            'verb_object_pairs': verb_object_pairs
        }

def main():
    """Test pre-processor"""
    processor = PreProcessor()
    
    test_text = "How to divide a cake into portions"
    result = processor.process(test_text)
    
    print("Pre-Processing Results:")
    print(f"Original: {result['original']}")
    print(f"Tokens: {result['tokens']}")
    print(f"Stemmed: {result['stemmed']}")
    print(f"Filtered: {result['filtered']}")
    print(f"Phrases: {result['phrases']}")
    print(f"Verb-Object Pairs: {result['verb_object_pairs']}")

if __name__ == "__main__":
    main()

