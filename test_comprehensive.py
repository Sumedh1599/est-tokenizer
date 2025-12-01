#!/usr/bin/env python3
"""
Comprehensive Test Suite
Tests token reduction and context preservation across 10 texts (10-256 words)
"""

import sys
import time
from est import SanskritTokenizer, SanskritDecoder

# Test texts of varying lengths (10 to 256 words)
TEST_TEXTS = [
    # 10 words
    "The quick brown fox jumps over the lazy dog in the park.",
    
    # 25 words
    "Machine learning algorithms process large amounts of data to identify patterns and make predictions. These systems learn from experience and improve their performance over time through training.",
    
    # 50 words
    "Property inheritance laws govern how assets are distributed when someone passes away. Legal documents like wills and trusts specify who receives what portion of the estate. Courts may need to intervene if disputes arise among family members about the distribution of property and financial resources.",
    
    # 75 words
    "Artificial intelligence and machine learning technologies are transforming how we interact with computers and process information. Large language models can understand context and generate human-like text responses. These systems use neural networks with millions of parameters to learn patterns from vast datasets. Researchers continue to improve model accuracy and reduce computational requirements. The applications span from natural language processing to computer vision and autonomous systems.",
    
    # 100 words
    "The ancient Sanskrit language contains rich semantic structures that allow single words to convey complex meanings. Scholars study how Sanskrit's morphological system enables precise expression through compound words and inflections. Modern computational linguistics applies these principles to develop more efficient natural language processing systems. The dhātu system with its verbal roots generates millions of word forms through systematic transformations. This linguistic density makes Sanskrit ideal for semantic tokenization and text compression applications.",
    
    # 125 words
    "Mathematical calculations involve complex operations that require careful attention to detail. Engineers use computational methods to solve problems in fields ranging from structural analysis to signal processing. Algorithms for matrix multiplication, numerical integration, and optimization play crucial roles in scientific computing. Researchers develop new mathematical models to understand physical phenomena and predict system behavior. The accuracy of these calculations depends on proper implementation and validation of computational procedures.",
    
    # 150 words
    "Legal systems around the world establish frameworks for resolving disputes and maintaining social order. Courts interpret laws and apply precedents to make decisions in civil and criminal cases. Lawyers represent clients by preparing arguments based on legal principles and evidence. Judges must consider multiple factors including statutes, case law, and constitutional provisions when rendering verdicts. The justice system aims to ensure fairness and protect individual rights while serving the public interest.",
    
    # 175 words
    "Economic systems determine how resources are allocated and distributed within societies. Markets facilitate exchange between buyers and sellers through price mechanisms that reflect supply and demand conditions. Governments implement policies to regulate economic activity and address market failures. Financial institutions provide services for saving, borrowing, and investing money. Economic growth depends on factors like productivity, innovation, and efficient resource utilization. International trade allows countries to specialize and benefit from comparative advantages.",
    
    # 200 words
    "Scientific research advances our understanding of natural phenomena through systematic observation and experimentation. Researchers formulate hypotheses and design experiments to test theoretical predictions. Peer review ensures that published findings meet rigorous standards for validity and reproducibility. Scientific knowledge accumulates over time as new discoveries build upon previous work. Collaboration across disciplines enables breakthroughs that would be impossible for individual researchers working in isolation. Funding agencies support research projects that address important questions and have potential for significant impact.",
    
    # 256 words
    "The development of artificial intelligence represents one of the most significant technological advances in human history. Machine learning systems can now perform tasks that previously required human intelligence, including image recognition, natural language understanding, and strategic decision-making. These capabilities emerge from training neural networks on massive datasets using sophisticated optimization algorithms. Large language models demonstrate remarkable abilities to generate coherent text, answer questions, and assist with various cognitive tasks. However, these systems also raise important questions about bias, transparency, and the future of work. Researchers continue to explore ways to make AI systems more interpretable, fair, and aligned with human values. The integration of AI into various industries promises to increase efficiency and enable new applications, but also requires careful consideration of ethical implications and societal impacts. As computational power increases and algorithms improve, we can expect AI capabilities to expand further, potentially transforming how we work, learn, and interact with technology."
]

def count_words(text):
    """Count words in text"""
    return len(text.split())

def calculate_reduction(original, compressed):
    """Calculate token reduction percentage"""
    orig_count = count_words(original)
    comp_count = count_words(compressed)
    if orig_count == 0:
        return 0.0
    return ((orig_count - comp_count) / orig_count) * 100

def simple_context_similarity(original, decoded):
    """Simple context similarity check - checks for key concepts"""
    orig_lower = original.lower()
    decoded_lower = decoded.lower()
    
    # Extract key words (non-stop words, length > 3)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'do', 'does', 'did',
                 'we', 'need', 'how', 'into', 'have', 'has', 'had', 'will', 'would', 'could', 'should',
                 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their'}
    
    orig_words = set(w.lower() for w in original.split() if len(w) > 3 and w.lower() not in stop_words)
    decoded_words = set(w.lower() for w in decoded.split() if len(w) > 3 and w.lower() not in stop_words)
    
    if not orig_words:
        return 1.0  # No meaningful words to compare
    
    # Calculate overlap
    common = orig_words.intersection(decoded_words)
    similarity = len(common) / len(orig_words) if orig_words else 0.0
    
    return similarity

def test_comprehensive():
    """Run comprehensive tests"""
    print("=" * 80)
    print("COMPREHENSIVE TEST SUITE - Token Reduction & Context Preservation")
    print("=" * 80)
    print()
    
    # Initialize tokenizer and decoder
    print("Initializing tokenizer and decoder...")
    tokenizer = SanskritTokenizer()
    decoder = SanskritDecoder()
    print("✅ Ready!")
    print()
    
    results = []
    
    for i, original_text in enumerate(TEST_TEXTS, 1):
        word_count = count_words(original_text)
        print(f"{'=' * 80}")
        print(f"TEST {i}/10 - {word_count} words")
        print(f"{'=' * 80}")
        print(f"Original: {original_text[:100]}{'...' if len(original_text) > 100 else ''}")
        print()
        
        # Step 1: Encode (English → Sanskrit)
        print("🔄 Encoding: English → Sanskrit")
        start_time = time.time()
        encoded_result = tokenizer.tokenize_with_confidence(original_text)
        encode_time = time.time() - start_time
        
        encoded_text = encoded_result['tokens']
        reduction = calculate_reduction(original_text, encoded_text)
        
        print(f"✅ Encoded: {encoded_text[:100]}{'...' if len(encoded_text) > 100 else ''}")
        print(f"📊 Token Reduction: {reduction:.1f}%")
        print(f"⏱️  Encoding Time: {encode_time:.2f}s")
        print(f"📈 Confidence: {encoded_result['confidence'] * 100:.2f}%")
        print()
        
        # Step 2: Decode (Sanskrit → English)
        print("🔄 Decoding: Sanskrit → English")
        start_time = time.time()
        decoded_result = decoder.decode_with_details(encoded_text)
        decode_time = time.time() - start_time
        
        decoded_text = decoded_result.get('english', '')
        context_similarity = simple_context_similarity(original_text, decoded_text)
        
        print(f"✅ Decoded: {decoded_text[:100]}{'...' if len(decoded_text) > 100 else ''}")
        print(f"📊 Context Similarity: {context_similarity * 100:.1f}%")
        print(f"⏱️  Decoding Time: {decode_time:.2f}s")
        print()
        
        # Step 3: Evaluation
        print("📋 Evaluation:")
        reduction_status = "✅" if reduction >= 20 else "⚠️" if reduction >= 10 else "❌"
        context_status = "✅" if context_similarity >= 0.5 else "⚠️" if context_similarity >= 0.3 else "❌"
        
        print(f"  {reduction_status} Token Reduction: {reduction:.1f}% (target: 20%+)")
        print(f"  {context_status} Context Preservation: {context_similarity * 100:.1f}% (target: 50%+)")
        print()
        
        # Store results
        results.append({
            'test_num': i,
            'word_count': word_count,
            'reduction': reduction,
            'context_similarity': context_similarity,
            'encode_time': encode_time,
            'decode_time': decode_time,
            'confidence': encoded_result['confidence'] * 100
        })
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    avg_reduction = sum(r['reduction'] for r in results) / len(results)
    avg_context = sum(r['context_similarity'] for r in results) / len(results)
    avg_encode_time = sum(r['encode_time'] for r in results) / len(results)
    avg_decode_time = sum(r['decode_time'] for r in results) / len(results)
    
    print(f"Average Token Reduction: {avg_reduction:.1f}%")
    print(f"Average Context Similarity: {avg_context * 100:.1f}%")
    print(f"Average Encoding Time: {avg_encode_time:.2f}s")
    print(f"Average Decoding Time: {avg_decode_time:.2f}s")
    print()
    
    print("Detailed Results:")
    print(f"{'Test':<6} {'Words':<8} {'Reduction':<12} {'Context':<12} {'Encode(s)':<12} {'Decode(s)':<12}")
    print("-" * 80)
    for r in results:
        print(f"{r['test_num']:<6} {r['word_count']:<8} {r['reduction']:>10.1f}% {r['context_similarity']*100:>10.1f}% {r['encode_time']:>10.2f} {r['decode_time']:>10.2f}")
    print()
    
    # Overall assessment
    print("Overall Assessment:")
    if avg_reduction >= 20 and avg_context >= 0.5:
        print("✅ PASS: Meets targets for both token reduction and context preservation")
    elif avg_reduction >= 20:
        print("⚠️  PARTIAL: Good token reduction but context preservation needs improvement")
    elif avg_context >= 0.5:
        print("⚠️  PARTIAL: Good context preservation but token reduction needs improvement")
    else:
        print("❌ FAIL: Both metrics need improvement")
    
    print()
    return results

if __name__ == "__main__":
    results = test_comprehensive()

