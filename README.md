# **EST (English → Sanskrit Tokenizer)**

**EST** is a revolutionary semantic tokenization engine that converts English text to Sanskrit words based on contextual meaning matching, leveraging the rich semantic structure of Sanskrit language.

![EST Architecture](assets/architecture.png)

## 🚀 **Features**

- **Semantic Tokenization**: Converts English to Sanskrit based on meaning, not direct translation
- **97%+ Accuracy**: For known vocabulary with proper contextual matching
- **50-70% Token Reduction**: Compresses English text using Sanskrit's semantic density
- **Context-Aware Processing**: Maintains semantic context throughout tokenization
- **Multi-Iteration Refinement**: 5-layer recursive processing for optimal matching
- **Graceful Degradation**: Handles unknown/modern terms gracefully
- **Rich Sanskrit Dataset**: 33,425 Sanskrit words with 7 semantic metadata columns

## 📦 **Installation**

```bash
pip install est-tokenizer
```

Or clone from source:

```bash
git clone https://github.com/sumedh1599/est-tokenizer.git
cd est-tokenizer
pip install -r requirements.txt
```

## 🔧 **Quick Start**

```python
from est import SanskritTokenizer

# Initialize tokenizer
tokenizer = SanskritTokenizer()

# Basic tokenization
english_text = "divide property inheritance fairly"
sanskrit_tokens = tokenizer.tokenize(english_text)
print(f"Input: {english_text}")
print(f"Tokens: {sanskrit_tokens}")

# With confidence scores
result = tokenizer.tokenize_with_confidence(english_text)
print(f"Confidence: {result['confidence']:.2f}%")
print(f"Processing Time: {result['processing_time_ms']}ms")
```

## 🏗️ **Architecture Overview**

EST uses a multi-layered recursive architecture:

```
English Text → Pre-Processor → Semantic Expander → Context Detector
      ↓
5-Iteration Recursive Engine → Scoring System → Decision Engine
      ↓
Sanskrit Tokens + Confidence Scores
```

### **Key Components:**

1. **Semantic Expander**: Expands English words to 17+ semantic concepts
2. **Context Detector**: Identifies domain (legal, mathematical, technical, etc.)
3. **Scoring System**: 40/25/20/15 weighted scoring algorithm
4. **Recursive Engine**: 5-iteration progressive refinement
5. **Decision Engine**: Accept/Continue/Reject logic with context assurance

## 📊 **Performance**

| Metric | Value | Status |
|--------|-------|--------|
| Accuracy (known vocab) | 97%+ | ✅ Excellent |
| Token Reduction | 50-70% | ✅ Optimal |
| Processing Speed | ~350ms/token | ⚡ Fast |
| Context Preservation | 100% | ✅ Perfect |
| Modern Term Handling | Graceful fallback | ✅ Robust |

## 📁 **Dataset**

EST uses a rich Sanskrit dataset with 33,425 words and 7 semantic columns:

- **sanskrit**: Sanskrit word
- **english**: English definition
- **semantic_frame**: Semantic role labels
- **Contextual_Triggers**: Context words
- **Conceptual_Anchors**: Abstract concepts
- **Ambiguity_Resolvers**: Disambiguation clues
- **Usage_Frequency_Index**: Context frequency weights

## 🎯 **Use Cases**

### **1. Text Compression**

```python
text = "Large language models process sequential data efficiently"
compressed = tokenizer.compress(text)
print(f"Reduction: {compressed['reduction_rate']:.1f}%")
```

### **2. Semantic Search**

```python
# Find Sanskrit equivalents for English concepts
concepts = tokenizer.find_sanskrit_equivalents("divide share distribute")
```

### **3. Context Analysis**

```python
context = tokenizer.analyze_context("property inheritance laws")
print(f"Primary Context: {context['primary']}")
print(f"Confidence: {context['confidence']:.1f}%")
```

### **4. Batch Processing**

```python
texts = ["divide property", "share resources", "calculate fractions"]
results = tokenizer.batch_tokenize(texts)
```

## 🔍 **Advanced Usage**

### **Custom Confidence Threshold**

```python
# Set custom acceptance threshold
tokenizer = SanskritTokenizer(min_confidence=0.85)
```

### **Expected Token Guidance**

```python
# Guide token selection with expected Sanskrit words
result = tokenizer.tokenize(
    "share resources", 
    expected_tokens=["aMS", "bhāgaH"],
    expected_context="economic"
)
```

### **Detailed Analysis**

```python
# Get full processing details
analysis = tokenizer.analyze("divide cake into portions")
print(analysis.keys())
# ['tokens', 'confidence', 'context', 'iterations_used', 
#  'scoring_breakdown', 'semantic_expansion']
```

## 📈 **Benchmarks**

```python
from est import benchmark

# Run comprehensive benchmarks
results = benchmark.run_suite()
benchmark.generate_report(results)
```

Sample benchmark results:
- Short phrases (1-10 words): 100% confidence, 66% token reduction
- Medium sentences (10-50 words): 97% confidence, 58% token reduction
- Technical texts: 29-60% confidence (expected for modern terms)

## 🛠️ **Development**

### **Project Structure**

```
est-tokenizer/
├── est/                          # Main package
│   ├── __init__.py
│   ├── tokenizer.py              # Main tokenizer class
│   ├── recursive_engine.py       # 5-iteration engine
│   ├── semantic_expander.py      # Semantic concept expansion
│   ├── scoring_system.py         # Weighted scoring
│   ├── context_detector.py       # Context detection
│   ├── dataset.py               # Sanskrit dataset loader
│   └── utils/                   # Utilities
├── data/
│   └── check_dictionary.csv     # 33,425 Sanskrit words
├── tests/                       # Test suite
├── examples/                    # Usage examples
├── benchmarks/                  # Performance benchmarks
└── assets/
    └── architecture.png         # Architecture diagram
```

### **Running Tests**

```bash
python -m pytest tests/ -v
python tests/test_comprehensive.py
```

### **Adding New Vocabulary**

Add new Sanskrit words to `data/check_dictionary.csv` with all 7 semantic columns.

## 📚 **API Reference**

### **SanskritTokenizer Class**

```python
class SanskritTokenizer:
    def __init__(self, min_confidence=0.80):
        """
        Initialize tokenizer with optional minimum confidence threshold.
        
        Args:
            min_confidence: Minimum confidence score (0-1) to accept a token
        """
    
    def tokenize(self, text, expected_tokens=None, expected_context=None):
        """
        Convert English text to Sanskrit tokens.
        
        Args:
            text: English input text
            expected_tokens: List of expected Sanskrit tokens (optional)
            expected_context: Expected context domain (optional)
        
        Returns:
            String of Sanskrit tokens (unmatched words remain in English)
        """
    
    def tokenize_with_confidence(self, text, **kwargs):
        """
        Tokenize with confidence scores and processing details.
        
        Returns:
            Dict with tokens, confidence, processing_time_ms, etc.
        """
    
    def compress(self, text):
        """
        Compress English text using Sanskrit tokenization.
        
        Returns:
            Dict with compressed text and reduction metrics
        """
    
    def analyze(self, text):
        """
        Detailed analysis of tokenization process.
        
        Returns:
            Dict with full processing details
        """
```

## 🔬 **Research Basis**

EST is based on linguistic research showing:

1. **Sanskrit's Semantic Density**: Single Sanskrit words encode multiple English concepts
2. **Dhātu System**: 2000 verbal roots generate millions of words
3. **Contextual Precision**: Sanskrit's case system reduces ambiguity
4. **Morphological Richness**: Inflections encode relationships without extra tokens

## 🤝 **Contributing**

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details.

## 👨‍💻 **Author**

**Sumedh Patil**
- GitHub: [sumedh1599](https://github.com/sumedh1599)
- Portfolio: [https://sumedh1599.github.io/Sumedh_Portfolio.github.io/](https://sumedh1599.github.io/Sumedh_Portfolio.github.io/)

## 🎉 **Citation**

If you use EST in your research or project:

```bibtex
@software{est_tokenizer2024,
  title = {EST: English → Sanskrit Tokenizer},
  author = {Sumedh Patil},
  year = {2025},
  url = {https://github.com/sumedh1599/est-tokenizer}
}
```

## ⭐ **Support**

If you find EST useful, please:
- Star the repository ⭐
- Share with your network
- Report issues and suggest features
- Contribute to development

---

**Built with ❤️ for Sanskrit language preservation and NLP innovation**

