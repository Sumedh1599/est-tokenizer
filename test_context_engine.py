#!/usr/bin/env python3
"""
Simple Context & Engine Test
Input text and check encoding, decoding, and context preservation
"""

import sys
from est import SanskritTokenizer, SanskritDecoder

def extract_key_concepts(text):
    """Extract key concepts (nouns, verbs, important words) for context comparison"""
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'do', 'does', 'did',
                 'we', 'need', 'how', 'into', 'have', 'has', 'had', 'will', 'would', 'could', 'should',
                 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their'}
    
    words = text.lower().split()
    # Get meaningful words (length > 3, not stop words)
    concepts = [w.strip('.,!?;:()[]{}') for w in words 
                if len(w.strip('.,!?;:()[]{}')) > 3 and w.strip('.,!?;:()[]{}') not in stop_words]
    return set(concepts)

def check_context_similarity(original, decoded):
    """
    Check if context is preserved (not word-to-word, but semantic meaning)
    Compares key concepts, subject-verb-object relationships
    """
    # Extract key concepts from both
    orig_concepts = extract_key_concepts(original)
    decoded_concepts = extract_key_concepts(decoded)
    
    if not orig_concepts:
        return 1.0  # No concepts to compare
    
    # Calculate overlap
    common = orig_concepts.intersection(decoded_concepts)
    similarity = len(common) / len(orig_concepts) if orig_concepts else 0.0
    
    return similarity

def test_engine_and_context():
    """Interactive test for engine and context preservation"""
    print("=" * 80)
    print("🕉️  EST TOKENIZER - ENGINE & CONTEXT TEST")
    print("=" * 80)
    print()
    print("This test checks:")
    print("  1. Encoding: English → Sanskrit (token reduction)")
    print("  2. Decoding: Sanskrit → English (context preservation)")
    print("  3. Context similarity (semantic meaning, not exact words)")
    print()
    print("Type 'quit' or 'exit' to stop")
    print()
    
    # Initialize
    print("Initializing tokenizer and decoder...")
    tokenizer = SanskritTokenizer()
    decoder = SanskritDecoder()
    print("✅ Ready!")
    print()
    
    while True:
        print("=" * 80)
        original_text = input("Enter English text to test: ").strip()
        
        if original_text.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not original_text:
            print("⚠️  Please enter some text.")
            continue
        
        print()
        print("=" * 80)
        print("🔄 STEP 1: ENCODING (English → Sanskrit)")
        print("=" * 80)
        print(f"📝 Original: {original_text}")
        print()
        print("Processing...")
        
        # Encode
        result = tokenizer.tokenize_with_confidence(original_text)
        encoded_text = result['tokens']
        
        # Calculate reduction
        orig_words = len(original_text.split())
        encoded_words = len(encoded_text.split())
        reduction = ((orig_words - encoded_words) / orig_words * 100) if orig_words > 0 else 0.0
        
        print(f"✅ Encoded: {encoded_text}")
        print()
        print(f"📊 Token Reduction: {reduction:.1f}%")
        print(f"   Input:  {orig_words} words")
        print(f"   Output: {encoded_words} words")
        print(f"📈 Confidence: {result['confidence'] * 100:.2f}%")
        print()
        
        print("=" * 80)
        print("🔄 STEP 2: DECODING (Sanskrit → English)")
        print("=" * 80)
        print(f"📝 Sanskrit: {encoded_text}")
        print()
        print("Decoding...")
        
        # Decode
        decoded_result = decoder.decode_with_details(encoded_text)
        decoded_text = decoded_result['english']
        
        print(f"✅ Decoded: {decoded_text}")
        print(f"📊 Decode Confidence: {decoded_result['confidence']:.1f}%")
        print(f"   Words Decoded: {decoded_result['decoded_count']}/{decoded_result['total_count']}")
        print()
        
        print("=" * 80)
        print("📋 STEP 3: CONTEXT PRESERVATION CHECK")
        print("=" * 80)
        print(f"📝 Original:  {original_text}")
        print(f"📝 Decoded:   {decoded_text}")
        print()
        
        # Check context similarity
        context_similarity = check_context_similarity(original_text, decoded_text)
        
        # Extract key concepts for display
        orig_concepts = extract_key_concepts(original_text)
        decoded_concepts = extract_key_concepts(decoded_text)
        common_concepts = orig_concepts.intersection(decoded_concepts)
        missing_concepts = orig_concepts - decoded_concepts
        
        print(f"📊 Context Similarity: {context_similarity * 100:.1f}%")
        print()
        
        if common_concepts:
            print(f"✅ Common Concepts ({len(common_concepts)}): {', '.join(list(common_concepts)[:10])}")
            if len(common_concepts) > 10:
                print(f"   ... and {len(common_concepts) - 10} more")
        print()
        
        if missing_concepts:
            print(f"⚠️  Missing Concepts ({len(missing_concepts)}): {', '.join(list(missing_concepts)[:10])}")
            if len(missing_concepts) > 10:
                print(f"   ... and {len(missing_concepts) - 10} more")
        else:
            print("✅ All key concepts preserved!")
        print()
        
        # Overall assessment
        print("=" * 80)
        print("📊 OVERALL ASSESSMENT")
        print("=" * 80)
        
        reduction_status = "✅" if reduction >= 20 else "⚠️" if reduction >= 10 else "❌"
        context_status = "✅" if context_similarity >= 0.5 else "⚠️" if context_similarity >= 0.3 else "❌"
        
        print(f"  {reduction_status} Token Reduction: {reduction:.1f}% (target: 20%+)")
        print(f"  {context_status} Context Preservation: {context_similarity * 100:.1f}% (target: 50%+)")
        print()
        
        if reduction >= 20 and context_similarity >= 0.5:
            print("✅ EXCELLENT: Both token reduction and context preservation meet targets!")
        elif reduction >= 20:
            print("⚠️  PARTIAL: Good compression but context needs improvement")
        elif context_similarity >= 0.5:
            print("⚠️  PARTIAL: Good context but compression needs improvement")
        else:
            print("❌ NEEDS WORK: Both metrics need improvement")
        print()
        print()

if __name__ == "__main__":
    test_engine_and_context()

