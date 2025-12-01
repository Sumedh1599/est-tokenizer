#!/usr/bin/env python3
"""
Test script to verify word preservation in tokenizer
Tests that unmatched words are kept in English
"""

import sys
sys.path.insert(0, '.')

from est import SanskritTokenizer

def test_word_preservation():
    """Test that unmatched words are preserved"""
    print("=" * 80)
    print("TESTING WORD PRESERVATION")
    print("=" * 80)
    print()
    
    tokenizer = SanskritTokenizer()
    
    test_cases = [
        "how do we need to cut the cake into perfect 8 pieces",
        "divide property inheritance",
        "share resources fairly",
        "calculate mathematical fraction"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"Test {i}: {test_text}")
        print("-" * 80)
        
        result = tokenizer.tokenize(test_text)
        print(f"Output: {result}")
        
        # Check word preservation
        words_in = test_text.split()
        words_out = result.split()
        
        # Count how many original words are preserved
        preserved = 0
        for word in words_in:
            word_clean = word.lower().strip('.,!?;:()[]{}')
            # Check if word appears in output (either as English or Sanskrit)
            if word_clean in result.lower() or word in result:
                preserved += 1
        
        print(f"Input words: {len(words_in)}")
        print(f"Output words: {len(words_out)}")
        print(f"Words preserved: {preserved}/{len(words_in)}")
        
        # Verify unmatched words are in output
        unmatched_found = 0
        for word in words_in:
            word_clean = word.lower().strip('.,!?;:()[]{}')
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                         'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'do', 'does', 'did',
                         'we', 'need', 'how', 'into', 'have', 'has', 'had'}
            if word_clean not in stop_words:
                # Check if this word appears in output (should be preserved if not matched)
                if word.lower() in result.lower():
                    unmatched_found += 1
        
        print(f"Unmatched words found in output: {unmatched_found}")
        print()
    
    print("=" * 80)
    print("✅ Word preservation test complete")
    print("=" * 80)

if __name__ == "__main__":
    test_word_preservation()

