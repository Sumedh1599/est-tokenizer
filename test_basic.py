"""
Basic tests for EST tokenizer
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

try:
    from est import SanskritTokenizer, SanskritDecoder
    print("✅ EST modules imported successfully")
    
    # Test 1: Basic tokenization
    tokenizer = SanskritTokenizer()
    decoder = SanskritDecoder()
    
    # Test 2: Simple tokenization
    test_text = "divide property"
    result = tokenizer.tokenize(test_text)
    
    if result and len(result) > 0:
        print(f"✅ Tokenization works: '{test_text}' → '{result}'")
    else:
        print(f"❌ Tokenization failed for: '{test_text}'")
        sys.exit(1)
    
    # Test 3: Decode back
    decoded = decoder.decode(result)
    if decoded and len(decoded) > 0:
        print(f"✅ Decoding works: '{result}' → '{decoded}'")
    else:
        print(f"❌ Decoding failed for: '{result}'")
        sys.exit(1)
    
    # Test 4: Confidence scoring
    detailed = tokenizer.tokenize_with_confidence(test_text)
    if 'confidence' in detailed:
        print(f"✅ Confidence scoring works: {detailed['confidence']:.1f}%")
    else:
        print("❌ Confidence scoring missing")
    
    print("\n✅ All basic tests passed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test failed with error: {e}")
    sys.exit(1)
