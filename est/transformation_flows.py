#!/usr/bin/env python3
"""
Transformation Flows - Phrase transformations for low-scoring chunks
"""

import re
from typing import List, Tuple, Dict

class TransformationFlows:
    def __init__(self):
        """Initialize transformation flows"""
        # Synonym mappings (basic - can be expanded)
        self.synonyms = {
            'divide': ['split', 'separate', 'share', 'distribute', 'portion'],
            'portion': ['part', 'share', 'piece', 'segment', 'division'],
            'share': ['divide', 'distribute', 'portion', 'part', 'allot'],
            'property': ['possession', 'asset', 'ownership', 'estate', 'belonging'],
            'inheritance': ['heritage', 'legacy', 'estate', 'bequest'],
            'fraction': ['portion', 'part', 'division', 'segment'],
            'calculate': ['compute', 'determine', 'figure', 'reckon'],
            'mathematical': ['numeric', 'arithmetic', 'computational'],
        }
    
    def transform_verb_object_pair(self, verb: str, obj: str) -> List[str]:
        """
        Transform verb-object pair semantically
        Returns: List of transformed phrases
        """
        transformations = []
        
        # Direct combination
        transformations.append(f"{verb} {obj}")
        
        # Add article variations
        transformations.append(f"{verb} a {obj}")
        transformations.append(f"{verb} the {obj}")
        
        # Reverse order (object-verb)
        transformations.append(f"{obj} {verb}")
        
        # Add synonyms
        verb_synonyms = self.synonyms.get(verb, [])
        obj_synonyms = self.synonyms.get(obj, [])
        
        for vs in verb_synonyms[:2]:  # Limit to 2 synonyms
            transformations.append(f"{vs} {obj}")
        
        for os in obj_synonyms[:2]:
            transformations.append(f"{verb} {os}")
        
        return transformations
    
    def semantic_transformation(self, phrase: str) -> List[str]:
        """
        Apply semantic transformations to phrase
        Returns: List of transformed phrases
        """
        transformations = [phrase]  # Original
        
        # Extract words
        words = phrase.split()
        
        if len(words) >= 2:
            # Try verb-object pattern
            verb = words[0]
            obj = words[-1]
            if verb and obj:
                verb_obj_transforms = self.transform_verb_object_pair(verb, obj)
                transformations.extend(verb_obj_transforms)
        
        # Add synonym variations
        synonym_phrases = self.apply_synonyms(phrase)
        transformations.extend(synonym_phrases)
        
        # Remove duplicates
        return list(dict.fromkeys(transformations))
    
    def apply_synonyms(self, phrase: str) -> List[str]:
        """Apply synonym replacements to phrase"""
        synonym_phrases = []
        words = phrase.split()
        
        for i, word in enumerate(words):
            if word in self.synonyms:
                for synonym in self.synonyms[word][:2]:  # Limit to 2 synonyms
                    new_words = words.copy()
                    new_words[i] = synonym
                    synonym_phrases.append(' '.join(new_words))
        
        return synonym_phrases
    
    def context_narrowing(self, phrase: str, context_words: List[str]) -> List[str]:
        """
        Narrow phrase context by adding context words
        Returns: List of narrowed phrases
        """
        narrowed = [phrase]
        
        for context in context_words[:3]:  # Limit to 3 context words
            # Add context before phrase
            narrowed.append(f"{context} {phrase}")
            # Add context after phrase
            narrowed.append(f"{phrase} {context}")
        
        return narrowed
    
    def expand_phrase(self, phrase: str) -> List[str]:
        """
        Expand phrase with variations
        Returns: List of expanded phrases
        """
        expansions = [phrase]
        
        # Add common modifiers
        modifiers = ['how to', 'way to', 'method to', 'process of']
        for modifier in modifiers:
            if not phrase.startswith(modifier):
                expansions.append(f"{modifier} {phrase}")
        
        return expansions
    
    def split_phrase(self, phrase: str) -> List[str]:
        """
        Split phrase into components
        Returns: List of phrase components
        """
        # Split by common connectors
        connectors = [' and ', ' or ', ' with ', ' from ', ' into ', ' to ']
        
        for connector in connectors:
            if connector in phrase:
                parts = phrase.split(connector)
                return [p.strip() for p in parts if p.strip()]
        
        # Split by spaces if long enough
        words = phrase.split()
        if len(words) > 3:
            # Return first half and second half
            mid = len(words) // 2
            return [' '.join(words[:mid]), ' '.join(words[mid:])]
        
        return [phrase]

def main():
    """Test transformation flows"""
    transformer = TransformationFlows()
    
    test_phrases = [
        "divide cake",
        "share resources",
        "property inheritance"
    ]
    
    print("Transformation Flows - Test")
    print("=" * 80)
    
    for phrase in test_phrases:
        print(f"\nOriginal: {phrase}")
        
        semantic = transformer.semantic_transformation(phrase)
        print(f"Semantic transformations: {semantic[:3]}")
        
        expanded = transformer.expand_phrase(phrase)
        print(f"Expanded: {expanded[:3]}")
        
        split = transformer.split_phrase(phrase)
        print(f"Split: {split}")

if __name__ == "__main__":
    main()

