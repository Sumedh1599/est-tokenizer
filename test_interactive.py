#!/usr/bin/env python3
"""
Interactive Test Script for EST Tokenizer
Allows users to test encoding and decoding interactively
"""

from est import SanskritTokenizer, SanskritDecoder
import sys

def print_separator():
    """Print a visual separator"""
    print("=" * 80)

def print_section(title):
    """Print a section header"""
    print()
    print_separator()
    print(f"  {title}")
    print_separator()
    print()

def main():
    print_separator()
    print("  🕉️  EST TOKENIZER - INTERACTIVE TEST")
    print_separator()
    print()
    print("This script allows you to:")
    print("  1. Enter English text")
    print("  2. See it tokenized to Sanskrit")
    print("  3. Optionally decode back to English")
    print()
    print("Type 'quit' or 'exit' to stop")
    print()
    
    # Initialize components
    print("Initializing tokenizer and decoder...")
    print("(This may take a few seconds on first run)")
    print()
    
    try:
        tokenizer = SanskritTokenizer()
        decoder = SanskritDecoder()
        print("✅ Tokenizer and decoder ready!")
        print()
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        sys.exit(1)
    
    # Interactive loop
    while True:
        print_separator()
        
        # Get user input
        english_text = input("Enter English text to tokenize: ").strip()
        
        # Check for exit commands
        if english_text.lower() in ['quit', 'exit', 'q', '']:
            print()
            print("👋 Goodbye!")
            break
        
        if not english_text:
            print("⚠️  Please enter some text.")
            continue
        
        print()
        print_section("ENCODING: English → Sanskrit")
        
        try:
            # Tokenize
            print(f"📝 Input: {english_text}")
            print()
            print("🔄 Processing...")
            
            result = tokenizer.tokenize_with_confidence(english_text)
            sanskrit_output = result['tokens']
            confidence = result['confidence']
            processing_time = result['processing_time_ms']
            
            print()
            print(f"✅ Sanskrit Output: {sanskrit_output}")
            print(f"📊 Confidence: {confidence * 100:.2f}%")
            print(f"⏱️  Processing Time: {processing_time:.2f}ms")
            print(f"🔄 Iteration Used: {result['iteration']}")
            print(f"📋 Decision: {result['decision']}")
            
            # Show breakdown if available
            if result.get('breakdown'):
                breakdown = result['breakdown']
                print()
                print("📈 Score Breakdown:")
                print(f"   • Semantic Frame: {breakdown.get('semantic_frame', 0):.2f}")
                print(f"   • Contextual Triggers: {breakdown.get('contextual_triggers', 0):.2f}")
                print(f"   • Conceptual Anchors: {breakdown.get('conceptual_anchors', 0):.2f}")
                print(f"   • Frequency Index: {breakdown.get('frequency_index', 0):.2f}")
            
        except Exception as e:
            print(f"❌ Error during tokenization: {e}")
            import traceback
            traceback.print_exc()
            continue
        
        # Ask about decoding
        print()
        print_separator()
        decode_choice = input("Decode back to English? (yes/y or no/n): ").strip().lower()
        
        if decode_choice in ['yes', 'y', '']:
            print()
            print_section("DECODING: Sanskrit → English")
            
            try:
                print(f"📝 Sanskrit Input: {sanskrit_output}")
                print()
                print("🔄 Decoding...")
                
                # Decode with details
                decode_result = decoder.decode_with_details(sanskrit_output)
                english_back = decode_result['english']
                decode_confidence = decode_result['confidence']
                decoded_count = decode_result['decoded_count']
                total_count = decode_result['total_count']
                
                print()
                print(f"✅ English Output: {english_back}")
                print(f"📊 Decode Confidence: {decode_confidence:.1f}%")
                print(f"📊 Words Decoded: {decoded_count}/{total_count}")
                
                # Show word-by-word details
                if decode_result.get('words'):
                    print()
                    print("📋 Word-by-Word Translation:")
                    for word_info in decode_result['words']:
                        sanskrit_word = word_info['sanskrit']
                        english_word = word_info.get('english', '[Unknown]')
                        found = word_info.get('found', False)
                        status = "✅" if found else "❌"
                        print(f"   {status} {sanskrit_word} → {english_word}")
                
                # Show unknown words if any
                if decode_result.get('unknown_words'):
                    print()
                    print(f"⚠️  Unknown Words: {', '.join(decode_result['unknown_words'])}")
                
                # Compare original vs decoded
                print()
                print_separator()
                print("📊 COMPARISON:")
                print(f"   Original:  {english_text}")
                print(f"   Encoded:   {sanskrit_output}")
                print(f"   Decoded:   {english_back}")
                
            except Exception as e:
                print(f"❌ Error during decoding: {e}")
                import traceback
                traceback.print_exc()
        
        else:
            print("⏭️  Skipping decode step.")
        
        print()
        print("Press Enter to continue or type 'quit' to exit...")
        _ = input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("👋 Interrupted by user. Goodbye!")
        sys.exit(0)

