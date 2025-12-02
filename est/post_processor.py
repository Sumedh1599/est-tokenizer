#!/usr/bin/env python3
"""
Post-Processor Block
Merge duplicate tokens, preserve grammar, output formatting
"""

from typing import List, Dict, Tuple
from collections import Counter

class PostProcessor:
    def __init__(self):
        """Initialize post-processor"""
        pass
    
    def merge_duplicate_tokens(self, tokens: List[Dict]) -> List[Dict]:
        """
        Merge duplicate tokens
        Returns: List of merged tokens with counts
        """
        token_counts = Counter()
        token_data = {}
        
        for token_info in tokens:
            sanskrit = token_info.get('sanskrit', '')
            if sanskrit:
                token_counts[sanskrit] += 1
                # Keep best score data
                if sanskrit not in token_data or token_info.get('score', 0.0) > token_data[sanskrit].get('score', 0.0):
                    token_data[sanskrit] = token_info
        
        # Build merged list
        merged = []
        for sanskrit, count in token_counts.items():
            token_info = token_data[sanskrit].copy()
            token_info['count'] = count
            merged.append(token_info)
        
        return merged
    
    def preserve_grammar(self, original_text: str, sanskrit_tokens: List[str]) -> str:
        """
        Preserve grammar structure from original text
        Returns: Formatted output with grammar preserved
        """
        # Simple approach: maintain word order and spacing
        # More sophisticated: analyze grammar and apply to Sanskrit
        
        # For now, just join tokens with spaces
        output = ' '.join(sanskrit_tokens)
        
        # Preserve capitalization pattern (first word capitalized if original was)
        if original_text and original_text[0].isupper():
            if output:
                output = output[0].upper() + output[1:] if len(output) > 1 else output.upper()
        
        # Preserve punctuation at end
        if original_text and original_text[-1] in '.!?':
            if output and output[-1] not in '.!?':
                output += original_text[-1]
        
        return output
    
    def format_output(self, results: List[Dict], original_text: str) -> Dict:
        """
        Format final output
        Returns: Formatted output dictionary
        """
        # Extract Sanskrit tokens
        sanskrit_tokens = []
        for result in results:
            sanskrit = result.get('sanskrit')
            if sanskrit:
                sanskrit_tokens.append(sanskrit)
        
        # Merge duplicates
        merged_tokens = self.merge_duplicate_tokens(results)
        
        # Preserve grammar
        formatted_output = self.preserve_grammar(original_text, sanskrit_tokens)
        
        # Calculate statistics
        total_tokens = len(sanskrit_tokens)
        unique_tokens = len(merged_tokens)
        avg_confidence = sum(r.get('score', 0.0) for r in results) / len(results) if results else 0.0
        
        return {
            'original_text': original_text,
            'sanskrit_output': formatted_output,
            'tokens': sanskrit_tokens,
            'unique_tokens': unique_tokens,
            'total_tokens': total_tokens,
            'average_confidence': avg_confidence,
            'token_details': merged_tokens
        }
    
    def handle_unmatched_words(self, original_text: str, matched_tokens: List[str], 
                              unmatched_words: List[str]) -> str:
        """
        Handle unmatched words in output
        Returns: Output with unmatched words preserved
        """
        # Simple approach: append unmatched words
        output_parts = matched_tokens.copy()
        
        if unmatched_words:
            output_parts.extend(unmatched_words)
        
        return ' '.join(output_parts)
    
    def optimize_output(self, output: str) -> str:
        """
        Optimize output formatting
        Returns: Optimized output string
        """
        # Remove extra spaces
        output = ' '.join(output.split())
        
        # Ensure proper spacing around punctuation
        output = output.replace(' .', '.').replace(' ,', ',')
        output = output.replace(' !', '!').replace(' ?', '?')
        
        return output.strip()

def main():
    """Test post-processor"""
    processor = PostProcessor()
    
    tokens = [
        {'sanskrit': 'aMSaH', 'score': 0.75, 'chunk': 'divide portions'},
        {'sanskrit': 'aMSaH', 'score': 0.80, 'chunk': 'share'},
        {'sanskrit': 'aMSakaH', 'score': 0.70, 'chunk': 'property'}
    ]
    
    original = "How to divide a cake into portions"
    
    result = processor.format_output(tokens, original)
    
    print("Post-Processor - Test")
    print("=" * 80)
    print(f"Original: {original}")
    print(f"Output: {result['sanskrit_output']}")
    print(f"Unique tokens: {result['unique_tokens']}")
    print(f"Average confidence: {result['average_confidence']:.2%}")

if __name__ == "__main__":
    main()

