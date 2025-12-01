#!/usr/bin/env python3
"""
EST - Main Tokenizer Class
Provides high-level API for English → Sanskrit tokenization
"""

import os
import time
from typing import List, Dict, Optional, Union
from pathlib import Path

from .recursive_engine import RecursiveEngine
from .semantic_expander import SemanticExpander
from .context_detector import ContextDetector

class SanskritTokenizer:
    """
    Main tokenizer class for converting English to Sanskrit tokens.
    
    Example:
        >>> tokenizer = SanskritTokenizer()
        >>> result = tokenizer.tokenize("divide property")
        >>> print(result)
        'saMpraBinna'
    """
    
    def __init__(self, min_confidence: float = 0.80, csv_path: Optional[str] = None):
        """
        Initialize the Sanskrit tokenizer.
        
        Args:
            min_confidence: Minimum confidence score (0-1) to accept a token. Default: 0.80
            csv_path: Path to Sanskrit dictionary CSV. If None, uses default location.
        """
        self.min_confidence = min_confidence
        
        # Determine CSV path
        if csv_path is None:
            # Try to find data file relative to package
            package_dir = Path(__file__).parent.parent
            default_path = package_dir / 'data' / 'check_dictionary.csv'
            if default_path.exists():
                csv_path = str(default_path)
            else:
                # Fallback to current directory
                csv_path = 'check_dictionary.csv'
        
        self.csv_path = csv_path
        self._engine = None
        self._expander = None
        self._detector = None
    
    @property
    def engine(self) -> RecursiveEngine:
        """Lazy load recursive engine."""
        if self._engine is None:
            self._engine = RecursiveEngine(csv_path=self.csv_path)
        return self._engine
    
    @property
    def expander(self) -> SemanticExpander:
        """Lazy load semantic expander."""
        if self._expander is None:
            self._expander = SemanticExpander()
        return self._expander
    
    @property
    def detector(self) -> ContextDetector:
        """Lazy load context detector."""
        if self._detector is None:
            self._detector = ContextDetector()
        return self._detector
    
    def tokenize(self, text: str, expected_tokens: Optional[List[str]] = None, 
                 expected_context: Optional[str] = None) -> str:
        """
        Convert English text to Sanskrit tokens.
        
        Args:
            text: English input text
            expected_tokens: List of expected Sanskrit tokens (optional, for guidance)
            expected_context: Expected context domain (optional, for guidance)
        
        Returns:
            String of Sanskrit tokens (unmatched words remain in English)
        """
        result = self.engine.process_text(text, expected_tokens, expected_context)
        return result.get('sanskrit_output', '')
    
    def tokenize_with_confidence(self, text: str, expected_tokens: Optional[List[str]] = None,
                                 expected_context: Optional[str] = None) -> Dict:
        """
        Tokenize with confidence scores and processing details.
        
        Args:
            text: English input text
            expected_tokens: List of expected Sanskrit tokens (optional)
            expected_context: Expected context domain (optional)
        
        Returns:
            Dict with:
                - tokens: Sanskrit output string
                - confidence: Confidence score (0-1)
                - processing_time_ms: Processing time in milliseconds
                - iteration: Iteration number used
                - decision: Decision made (ACCEPT/CONTINUE/REJECT)
        """
        start_time = time.time()
        
        result = self.engine.process_text(text, expected_tokens, expected_context)
        final_result = result.get('final_result', {})
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return {
            'tokens': result.get('sanskrit_output', ''),
            'confidence': result.get('confidence', 0.0),
            'processing_time_ms': processing_time,
            'iteration': final_result.get('iteration', 0),
            'decision': str(final_result.get('decision', 'UNKNOWN')),
            'reason': final_result.get('reason', ''),
            'breakdown': final_result.get('breakdown', {})
        }
    
    def compress(self, text: str) -> Dict:
        """
        Compress English text using Sanskrit tokenization.
        
        Args:
            text: English input text
        
        Returns:
            Dict with:
                - compressed: Sanskrit tokenized text
                - original_tokens: Number of original English tokens
                - sanskrit_tokens: Number of Sanskrit tokens
                - reduction_rate: Token reduction percentage
                - reduction_percentage: Formatted reduction percentage
        """
        result = self.tokenize_with_confidence(text)
        tokens = result['tokens']
        
        # Count tokens (simple word count)
        original_tokens = len(text.split())
        sanskrit_tokens = len(tokens.split()) if tokens else 0
        
        reduction_rate = (original_tokens - sanskrit_tokens) / original_tokens if original_tokens > 0 else 0.0
        
        return {
            'compressed': tokens,
            'original_tokens': original_tokens,
            'sanskrit_tokens': sanskrit_tokens,
            'reduction_rate': reduction_rate,
            'reduction_percentage': f"{reduction_rate * 100:.1f}%"
        }
    
    def find_sanskrit_equivalents(self, text: str, top_n: int = 5) -> List[Dict]:
        """
        Find Sanskrit equivalents for English concepts.
        
        Args:
            text: English input text
            top_n: Number of top matches to return
        
        Returns:
            List of dicts with sanskrit, score, and breakdown
        """
        matches = self.engine.scoring_system.find_best_matches(text, top_n=top_n)
        
        results = []
        for sanskrit, score, breakdown in matches:
            results.append({
                'sanskrit': sanskrit,
                'score': score,
                'confidence': f"{score * 100:.2f}%",
                'breakdown': breakdown
            })
        
        return results
    
    def analyze_context(self, text: str) -> Dict:
        """
        Analyze context of English text.
        
        Args:
            text: English input text
        
        Returns:
            Dict with primary context, scores, and keywords
        """
        context_info = self.detector.detect_context(text)
        
        return {
            'primary': context_info.get('primary_context', 'general'),
            'confidence': max(context_info.get('context_scores', {}).values(), default=0.0),
            'scores': context_info.get('context_scores', {}),
            'keywords': context_info.get('context_keywords', {})
        }
    
    def batch_tokenize(self, texts: List[str]) -> List[Dict]:
        """
        Tokenize multiple texts in batch.
        
        Args:
            texts: List of English texts
        
        Returns:
            List of tokenization results (same format as tokenize_with_confidence)
        """
        results = []
        for text in texts:
            result = self.tokenize_with_confidence(text)
            result['original_text'] = text
            results.append(result)
        
        return results
    
    def analyze(self, text: str) -> Dict:
        """
        Detailed analysis of tokenization process.
        
        Args:
            text: English input text
        
        Returns:
            Dict with full processing details including:
                - tokens: Sanskrit output
                - confidence: Confidence score
                - context: Context analysis
                - iterations_used: Iteration number
                - scoring_breakdown: Detailed scoring
                - semantic_expansion: Expanded concepts
        """
        # Get tokenization result
        result = self.tokenize_with_confidence(text)
        
        # Get context analysis
        context = self.analyze_context(text)
        
        # Get semantic expansion
        expanded = self.expander.expand_with_context(text)
        
        # Get final result details
        final_result = self.engine.process_text(text).get('final_result', {})
        
        return {
            'tokens': result['tokens'],
            'confidence': result['confidence'],
            'context': context,
            'iterations_used': result['iteration'],
            'scoring_breakdown': result.get('breakdown', {}),
            'semantic_expansion': {
                'concepts': expanded.get('concepts', [])[:20],  # First 20 concepts
                'total_concepts': len(expanded.get('concepts', [])),
                'primary_context': expanded.get('primary_context', 'N/A')
            },
            'decision': result['decision'],
            'reason': result['reason']
        }

