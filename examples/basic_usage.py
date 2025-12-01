#!/usr/bin/env python3
"""
Basic usage examples for EST Tokenizer
"""

from est import SanskritTokenizer

def example_basic():
    """Basic tokenization example"""
    print("=" * 60)
    print("Example 1: Basic Tokenization")
    print("=" * 60)
    
    tokenizer = SanskritTokenizer()
    
    text = "divide property inheritance fairly"
    result = tokenizer.tokenize(text)
    
    print(f"Input:  {text}")
    print(f"Output: {result}")
    print()

def example_with_confidence():
    """Tokenization with confidence scores"""
    print("=" * 60)
    print("Example 2: Tokenization with Confidence")
    print("=" * 60)
    
    tokenizer = SanskritTokenizer()
    
    text = "divide property"
    result = tokenizer.tokenize_with_confidence(text)
    
    print(f"Input:  {text}")
    print(f"Output: {result['tokens']}")
    print(f"Confidence: {result['confidence'] * 100:.2f}%")
    print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
    print(f"Iteration: {result['iteration']}")
    print()

def example_compression():
    """Text compression example"""
    print("=" * 60)
    print("Example 3: Text Compression")
    print("=" * 60)
    
    tokenizer = SanskritTokenizer()
    
    text = "divide property inheritance"
    result = tokenizer.compress(text)
    
    print(f"Original: {text}")
    print(f"Compressed: {result['compressed']}")
    print(f"Token Reduction: {result['reduction_percentage']}")
    print()

def example_context_analysis():
    """Context analysis example"""
    print("=" * 60)
    print("Example 4: Context Analysis")
    print("=" * 60)
    
    tokenizer = SanskritTokenizer()
    
    text = "property inheritance laws"
    context = tokenizer.analyze_context(text)
    
    print(f"Text: {text}")
    print(f"Primary Context: {context['primary']}")
    print(f"Confidence: {context['confidence'] * 100:.1f}%")
    print(f"Context Scores: {context['scores']}")
    print()

def example_detailed_analysis():
    """Detailed analysis example"""
    print("=" * 60)
    print("Example 5: Detailed Analysis")
    print("=" * 60)
    
    tokenizer = SanskritTokenizer()
    
    text = "divide cake into portions"
    analysis = tokenizer.analyze(text)
    
    print(f"Text: {text}")
    print(f"Tokens: {analysis['tokens']}")
    print(f"Confidence: {analysis['confidence'] * 100:.2f}%")
    print(f"Context: {analysis['context']['primary']}")
    print(f"Iterations Used: {analysis['iterations_used']}")
    print(f"Semantic Concepts: {len(analysis['semantic_expansion']['concepts'])}")
    print()

if __name__ == "__main__":
    example_basic()
    example_with_confidence()
    example_compression()
    example_context_analysis()
    example_detailed_analysis()

