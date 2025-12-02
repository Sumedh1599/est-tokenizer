#!/usr/bin/env python3
"""
Encode-Decode Example
Demonstrates full cycle: English → Sanskrit → English
"""

from est import SanskritTokenizer, SanskritDecoder

def main():
    print("=" * 60)
    print("🔄 ENCODE-DECODE CYCLE EXAMPLE")
    print("=" * 60)
    print()
    
    # Initialize
    tokenizer = SanskritTokenizer()
    decoder = SanskritDecoder()
    
    # Test cases
    test_cases = [
        "divide property",
        "share resources",
        "calculate fraction",
        "property inheritance"
    ]
    
    for i, english_text in enumerate(test_cases, 1):
        print(f"Test {i}: {english_text}")
        print("-" * 60)
        
        # Encode: English → Sanskrit
        sanskrit = tokenizer.tokenize(english_text)
        print(f"  English → Sanskrit: {sanskrit}")
        
        # Decode: Sanskrit → English
        english_back = decoder.decode(sanskrit)
        print(f"  Sanskrit → English: {english_back}")
        
        # Detailed decode
        details = decoder.decode_with_details(sanskrit)
        print(f"  Confidence: {details['confidence']:.1f}%")
        print(f"  Words decoded: {details['decoded_count']}/{details['total_count']}")
        
        print()
    
    print("=" * 60)
    print("✅ Encode-Decode cycle complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

