#!/usr/bin/env python3
"""
Context Detector - Understands WHAT is being described
Detects context types (legal, mathematical, economic, etc.) from English input
"""

from typing import Dict, List, Set
import re
from .semantic_expander import SemanticExpander

class ContextDetector:
    def __init__(self):
        """Initialize context detector"""
        self.expander = SemanticExpander()
        
        # Context patterns and keywords
        self.context_patterns = {
            'legal': {
                'keywords': ['property', 'inheritance', 'debt', 'obligation', 'legal', 'contract', 
                            'law', 'right', 'claim', 'ownership', 'estate', 'will', 'testament',
                            'heir', 'co-heir', 'ancestral'],
                'weight': 1.0
            },
            'mathematical': {
                'keywords': ['fraction', 'calculation', 'mathematical', 'numerator', 'denominator',
                            'divide', 'multiply', 'sum', 'number', 'count', 'calculate', 'compute'],
                'weight': 1.0
            },
            'economic': {
                'keywords': ['resources', 'assets', 'wealth', 'property', 'distribution',
                            'allocation', 'share', 'portion', 'fairly', 'equitably'],
                'weight': 1.0
            },
            'food': {
                'keywords': ['cake', 'food', 'dessert', 'meal', 'eating', 'cooking'],
                'weight': 0.5  # Lower weight for food context
            },
            'action': {
                'keywords': ['divide', 'share', 'distribute', 'allocate', 'split', 'separate'],
                'weight': 0.8
            },
            'social': {
                'keywords': ['people', 'family', 'relative', 'community', 'society'],
                'weight': 0.9
            },
            'technical': {
                'keywords': ['llm', 'transformer', 'attention', 'mechanism', 'processing', 'neural', 'ai', 'machine learning', 'artificial intelligence'],
                'weight': 1.0
            },
            'ai': {
                'keywords': ['artificial intelligence', 'machine learning', 'neural network', 'language model', 'transformer', 'attention mechanism'],
                'weight': 1.0
            }
        }
    
    def detect_context(self, text: str) -> Dict:
        """
        Detect context from text
        Returns: {
            'primary_context': context type,
            'context_scores': dict of context scores,
            'context_keywords': dict of matched keywords per context
        }
        """
        text_lower = text.lower()
        context_scores = {}
        context_keywords = {}
        
        for context_type, context_info in self.context_patterns.items():
            keywords = context_info['keywords']
            weight = context_info['weight']
            
            matched_keywords = []
            for keyword in keywords:
                if keyword in text_lower:
                    matched_keywords.append(keyword)
            
            # Calculate score based on matched keywords
            score = (len(matched_keywords) / len(keywords)) * weight if keywords else 0.0
            
            if matched_keywords:
                context_scores[context_type] = score
                context_keywords[context_type] = matched_keywords
        
        # Determine primary context
        primary_context = None
        if context_scores:
            primary_context = max(context_scores.items(), key=lambda x: x[1])[0]
        
        return {
            'primary_context': primary_context,
            'context_scores': context_scores,
            'context_keywords': context_keywords
        }
    
    def detect(self, text: str) -> str:
        """
        Convenience method: Detect primary context from text
        Returns: Primary context type as string (for backward compatibility)
        """
        context_info = self.detect_context(text)
        return context_info.get('primary_context', 'general')
    
    def get_context_priority(self, text: str, sanskrit_word: str, word_data: Dict) -> float:
        """
        Get context priority score for a Sanskrit word given English text
        Higher score = better context match
        """
        detected_context = self.detect_context(text)
        primary_context = detected_context.get('primary_context')
        
        if not primary_context:
            return 0.5  # Neutral priority
        
        # Check if Sanskrit word's Usage_Frequency_Index matches detected context
        frequency_index = word_data.get('usage_frequency_index', '').strip()
        if frequency_index:
            # Check if primary context appears in frequency index
            if primary_context in frequency_index.lower():
                # Extract weight for this context
                for part in frequency_index.split('|'):
                    if ':' in part:
                        context, weight_str = part.rsplit(':', 1)
                        if context.strip().lower() == primary_context:
                            try:
                                weight = float(weight_str)
                                return weight  # Return the weight as priority
                            except ValueError:
                                pass
        
        # Check Contextual_Triggers for context match
        triggers = word_data.get('contextual_triggers', '').strip()
        if triggers:
            context_keywords = detected_context.get('context_keywords', {}).get(primary_context, [])
            trigger_words = [t.strip().lower() for t in triggers.split('|')]
            
            # Count matches
            matches = len(set(context_keywords) & set(trigger_words))
            if matches > 0:
                return 0.7  # Good context match
        
        return 0.3  # Low context match
    
    def context_aware_filter(self, text: str, sanskrit_candidates: List[tuple], word_data: Dict) -> List[tuple]:
        """
        Filter and re-rank Sanskrit candidates based on context
        Returns: Re-ranked list of (sanskrit, score, breakdown) tuples
        """
        detected_context = self.detect_context(text)
        primary_context = detected_context.get('primary_context')
        
        if not primary_context:
            return sanskrit_candidates  # No context detected, return as-is
        
        # Re-score candidates with context priority
        re_scored = []
        for sanskrit, score, breakdown in sanskrit_candidates:
            word_info = word_data.get(sanskrit, {})
            context_priority = self.get_context_priority(text, sanskrit, word_info)
            
            # Boost score based on context priority
            boosted_score = score * (0.7 + context_priority * 0.3)
            
            re_scored.append((sanskrit, boosted_score, breakdown))
        
        # Sort by boosted score
        re_scored.sort(key=lambda x: x[1], reverse=True)
        
        return re_scored

def main():
    """Test context detector"""
    detector = ContextDetector()
    
    test_texts = [
        "divide property inheritance",
        "divide cake into portions",
        "share resources fairly",
        "mathematical fraction calculation"
    ]
    
    print("Context Detector - Test")
    print("=" * 80)
    
    for text in test_texts:
        context_info = detector.detect_context(text)
        print(f"\nText: '{text}'")
        print(f"Primary context: {context_info['primary_context']}")
        print(f"Context scores: {context_info['context_scores']}")

if __name__ == "__main__":
    main()

