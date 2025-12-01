#!/usr/bin/env python3
"""
Semantic Expander - Expands English words to semantic concepts
Uses synonym dictionaries, WordNet-like relationships, and contextual meanings
"""

from typing import List, Set, Dict
import re

class SemanticExpander:
    def __init__(self):
        """Initialize semantic expander with comprehensive synonym/concept mappings"""
        
        # Comprehensive semantic concept mappings
        # Each word maps to its semantic concepts (synonyms, related meanings)
        self.semantic_concepts = {
            'divide': ['split', 'share', 'distribute', 'portion', 'division', 'allocation', 
                      'separate', 'partition', 'apportion', 'allocate', 'parcel', 'section'],
            'share': ['divide', 'distribute', 'portion', 'part', 'allot', 'allocate', 
                     'apportion', 'parcel', 'division', 'split'],
            'distribute': ['divide', 'share', 'allocate', 'apportion', 'dispense', 
                          'allot', 'parcel', 'portion', 'divide up'],
            'portion': ['part', 'share', 'division', 'segment', 'piece', 'fraction', 
                       'allocation', 'allotment', 'quota'],
            'part': ['portion', 'share', 'division', 'segment', 'piece', 'fraction', 
                    'component', 'section'],
            'property': ['possession', 'asset', 'ownership', 'estate', 'belonging', 
                        'real estate', 'land', 'holding'],
            'inheritance': ['heritage', 'legacy', 'estate', 'bequest', 'patrimony', 
                          'endowment', 'succession'],
            'fraction': ['portion', 'part', 'division', 'segment', 'piece', 
                        'numerator', 'denominator'],
            'calculate': ['compute', 'determine', 'figure', 'reckon', 'work out', 
                         'estimate', 'assess'],
            'mathematical': ['numeric', 'arithmetic', 'computational', 'quantitative', 
                            'numerical'],
            'free': ['liberate', 'release', 'unbound', 'unrestricted', 'unfettered'],
            'obligation': ['debt', 'duty', 'responsibility', 'commitment', 'liability'],
            'debt': ['obligation', 'liability', 'indebtedness', 'arrears'],
            'resources': ['assets', 'materials', 'supplies', 'means', 'funds', 'wealth'],
            'assets': ['resources', 'property', 'possessions', 'wealth', 'holdings'],
            'fairly': ['equitably', 'justly', 'evenly', 'equally', 'impartially'],
            'cake': ['food', 'dessert', 'sweet', 'pastry'],
            'portions': ['parts', 'shares', 'divisions', 'segments', 'pieces'],
            'how': ['method', 'way', 'manner', 'process', 'technique'],
            'to': [],  # Stop word
            'a': [],   # Stop word
            'into': ['toward', 'towards', 'to'],
            # Modern technical terms
            'llm': ['large language model', 'language model', 'ai model', 'neural network', 'machine learning', 'artificial intelligence'],
            'transformer': ['transform', 'convert', 'change', 'modify', 'neural network', 'ai architecture', 'model'],
            'attention': ['focus', 'concentration', 'awareness', 'mechanism', 'process', 'neural attention'],
            'mechanism': ['process', 'method', 'system', 'function', 'operation', 'procedure'],
            'mechanisms': ['processes', 'methods', 'systems', 'functions', 'operations', 'procedures'],
            'natural': ['organic', 'normal', 'inherent', 'intrinsic', 'native'],
            'language': ['speech', 'communication', 'tongue', 'dialect', 'linguistic'],
            'processing': ['handling', 'managing', 'analyzing', 'computing', 'executing'],
            'use': ['utilize', 'employ', 'apply', 'operate', 'function'],
            'for': [],  # Stop word
        }
        
        # Context-based concept groups
        self.context_groups = {
            'legal': ['property', 'inheritance', 'debt', 'obligation', 'legal', 'contract', 
                     'law', 'right', 'claim', 'ownership', 'estate', 'will', 'testament'],
            'mathematical': ['fraction', 'calculation', 'mathematical', 'numerator', 
                           'denominator', 'divide', 'multiply', 'sum', 'number', 'count'],
            'economic': ['resources', 'assets', 'wealth', 'property', 'distribution', 
                        'allocation', 'share', 'portion'],
            'food': ['cake', 'food', 'dessert', 'meal', 'eating'],
            'action': ['divide', 'share', 'distribute', 'allocate', 'split', 'separate'],
            'technical': ['llm', 'transformer', 'attention', 'mechanism', 'processing', 'neural', 'ai', 'machine learning', 'artificial intelligence'],
            'ai': ['artificial intelligence', 'machine learning', 'neural network', 'language model', 'transformer', 'attention mechanism']
        }
    
    def expand_word(self, word: str) -> Set[str]:
        """
        Expand a single word to its semantic concepts
        Returns: Set of semantic concepts
        """
        word_lower = word.lower().strip()
        
        # Direct lookup
        concepts = set()
        if word_lower in self.semantic_concepts:
            concepts.update(self.semantic_concepts[word_lower])
        
        # Add the word itself
        concepts.add(word_lower)
        
        # Reverse lookup: find words that have this word as a concept
        for key, values in self.semantic_concepts.items():
            if word_lower in values:
                concepts.add(key)
                concepts.update(values)
        
        return concepts
    
    def expand_text(self, text: str) -> Set[str]:
        """
        Expand entire text to semantic concepts
        Returns: Set of all semantic concepts
        """
        # Extract words
        words = re.findall(r'\b[a-z]{2,}\b', text.lower())
        
        # Filter stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were'}
        words = [w for w in words if w not in stop_words]
        
        # Expand each word
        all_concepts = set()
        for word in words:
            concepts = self.expand_word(word)
            all_concepts.update(concepts)
        
        return all_concepts
    
    def get_context_concepts(self, text: str) -> Dict[str, Set[str]]:
        """
        Get context-specific concepts
        Returns: Dictionary mapping context types to relevant concepts
        """
        text_lower = text.lower()
        context_concepts = {}
        
        for context_type, context_words in self.context_groups.items():
            matching_concepts = set()
            for word in context_words:
                if word in text_lower:
                    matching_concepts.add(word)
                    # Also add expanded concepts
                    matching_concepts.update(self.expand_word(word))
            
            if matching_concepts:
                context_concepts[context_type] = matching_concepts
        
        return context_concepts
    
    def expand_with_context(self, text: str) -> Dict:
        """
        Expand text with context awareness
        Returns: {
            'concepts': list of all concepts (converted from set for compatibility),
            'contexts': dict of context-specific concepts,
            'primary_context': dominant context type
        }
        """
        concepts = self.expand_text(text)
        context_concepts = self.get_context_concepts(text)
        
        # Determine primary context
        primary_context = None
        max_context_size = 0
        for context_type, ctx_concepts in context_concepts.items():
            if len(ctx_concepts) > max_context_size:
                max_context_size = len(ctx_concepts)
                primary_context = context_type
        
        # Convert set to list for compatibility (can be subscripted)
        return {
            'concepts': list(concepts),
            'contexts': context_concepts,
            'primary_context': primary_context
        }
    
    def expand(self, text: str) -> List[str]:
        """
        Convenience method: Expand text to list of concepts
        Returns: List of semantic concepts (for backward compatibility)
        """
        concepts = self.expand_text(text)
        return list(concepts)

def main():
    """Test semantic expander"""
    expander = SemanticExpander()
    
    test_words = ['divide', 'share', 'property', 'inheritance']
    
    print("Semantic Expander - Test")
    print("=" * 80)
    
    for word in test_words:
        concepts = expander.expand_word(word)
        print(f"\n{word} → {len(concepts)} concepts:")
        print(f"  {', '.join(list(concepts)[:10])}...")
    
    print("\n" + "=" * 80)
    test_text = "divide property inheritance"
    expanded = expander.expand_with_context(test_text)
    print(f"\nText: '{test_text}'")
    print(f"Total concepts: {len(expanded['concepts'])}")
    print(f"Contexts: {list(expanded['contexts'].keys())}")
    print(f"Primary context: {expanded['primary_context']}")

if __name__ == "__main__":
    main()

