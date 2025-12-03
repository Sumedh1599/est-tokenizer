---
title: 'EST: English-to-Sanskrit Tokenizer - A Sanskrit-Based Semantic Tokenization System for NLP'
tags:
  - Python
  - NLP
  - tokenization
  - Sanskrit
  - computational linguistics
  - semantic-compression
authors:
  - name: Sumedh Patil
    orcid: 0009-0003-1901-4250
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 04 December 2024
bibliography: paper.bib
---

# Summary

EST (English-to-Sanskrit Tokenizer) is a novel semantic tokenization engine that converts English text to Sanskrit words based on contextual meaning matching, leveraging the rich morphological structure of Sanskrit language. Unlike statistical sub-word tokenizers (BPE, WordPiece, SentencePiece) that segment text by frequency, EST performs semantic-aware mapping into linguistically valid Sanskrit tokens. This approach yields a 55% average token reduction (with peaks of 82% in legal/mathematical domains) while preserving 95% contextual information in the encode-decode cycle.

# Statement of Need

Tokenization is the foundational step in modern Natural Language Processing pipelines. Current tokenization methods face two key limitations: (1) they operate on frequency-based statistics rather than linguistic meaning, producing arbitrary fragments, and (2) they lack cross-lingual consistency. There is a clear need for semantically-grounded tokenization that produces interpretable, compressible representations while maintaining reversibility. EST addresses this gap by treating Sanskrit's algorithmic morphology—codified in Paninian grammar—as a computational resource. Sanskrit's agglutinative nature enables single lexical items to encode multi-word English concepts while remaining grammatically valid.

# Key Features

The EST tokenizer provides:
- **Semantic-first tokenization** that outputs grammatical Sanskrit tokens
- **55% average token reduction** with 95% context-retrieval accuracy
- **33,425-entry curated lexicon** with Paninian morphological constraints and semantic metadata
- **Dual-path architecture** ensuring 100% coverage through dictionary matching and reversible transliteration
- **Zero token loss** with perfect reversibility in encode-decode cycles
- **Domain-aware processing** with specialized performance in legal, mathematical, and technical texts

# Methodology

EST implements a linguistically constrained dual-path pipeline:

1. **Semantic Phrase Matching**: Greedy matching of 2-6 word English phrases against the Sanskrit lexicon using a weighted scoring function (40% semantic frame, 25% context, 20% conceptual anchors, 15% frequency).

2. **Single-Word Lookup**: Fallback matching for individual words with aggressive similarity thresholds (0.05-0.15).

3. **Reversible Transliteration**: Final fallback converting English graphemes to phonetically nearest Devanagari characters, preserving round-trip integrity through anusvara boundary markers.

The system includes a manually curated Sanskrit lexicon of 33,425 words, each annotated with eight semantic metadata columns and a semantic-neighbor network of 14,188 bidirectional pairs for concept disambiguation.

# Benchmark Results

Evaluation on a balanced 100-sentence corpus across five domains shows consistent superiority over baseline tokenizers:

- **Token Reduction**: 55% average reduction (GPT-2: -18%, SentencePiece: -31%, Mandarin: -47%)
- **Context Retrieval**: 95% accuracy after decode cycle
- **Space Savings**: 40% compression achieved
- **Coverage**: 100% through dual-path approach

**Notable Case Study**: The legal phrase "divide property inheritance fairly among heirs" compresses to the single Sanskrit token "*aṃśakaḥ*" (agent noun "partitioner"), achieving 82% token reduction without semantic loss.

# Availability

- **Source Code**: https://github.com/Sumedh1599/est-tokenizer
- **License**: MIT License
- **Archive**: Zenodo DOI: 10.5281/zenodo.17807018
- **Python Package**: `pip install est-tokenizer`
