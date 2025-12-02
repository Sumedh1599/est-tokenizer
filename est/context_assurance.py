#!/usr/bin/env python3
"""
Context Assurance - Context maintenance checks
"""

from typing import List, Dict, Optional, Tuple
import re

class ContextAssurance:
    def __init__(self):
        """Initialize context assurance"""
        self.context_loss_threshold = 0.40  # 40% context loss
        self.min_context_overlap = 0.30  # 30% minimum overlap
    
    def extract_context_words(self, text: str) -> set:
        """Extract context words from text"""
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        return set(w for w in words if w not in stop_words)
    
    def calculate_context_overlap(self, text1: str, text2: str) -> float:
        """Calculate context overlap between two texts"""
        words1 = self.extract_context_words(text1)
        words2 = self.extract_context_words(text2)
        
        if not words1 or not words2:
            return 0.0
        
        overlap = len(words1 & words2)
        union = len(words1 | words2)
        
        return overlap / union if union > 0 else 0.0
    
    def context_maintained(self, current_text: str, previous_text: str) -> bool:
        """Check if context is maintained between iterations"""
        overlap = self.calculate_context_overlap(current_text, previous_text)
        return overlap >= self.min_context_overlap
    
    def context_degradation(self, current_score: float, previous_score: Optional[float],
                           current_text: str, previous_text: Optional[str]) -> Tuple[bool, float]:
        """
        Detect context degradation
        Returns: (is_degraded, degradation_percentage)
        """
        if previous_score is None or previous_text is None:
            return False, 0.0
        
        # Score degradation
        score_degradation = (previous_score - current_score) / previous_score if previous_score > 0 else 0.0
        
        # Context overlap
        context_overlap = self.calculate_context_overlap(current_text, previous_text)
        context_loss = 1.0 - context_overlap
        
        # Combined degradation
        total_degradation = (score_degradation + context_loss) / 2.0
        
        is_degraded = total_degradation > self.context_loss_threshold
        
        return is_degraded, total_degradation
    
    def verify_context_consistency(self, chunks: List[Dict]) -> bool:
        """
        Verify context consistency across multiple chunks
        Returns: True if context is consistent
        """
        if len(chunks) < 2:
            return True
        
        # Check pairwise consistency
        for i in range(len(chunks) - 1):
            chunk1 = chunks[i]
            chunk2 = chunks[i + 1]
            
            text1 = chunk1.get('text', '')
            text2 = chunk2.get('text', '')
            
            overlap = self.calculate_context_overlap(text1, text2)
            if overlap < self.min_context_overlap:
                return False
        
        return True
    
    def get_context_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Extract top context keywords from text"""
        words = self.extract_context_words(text)
        # Simple frequency-based (can be enhanced)
        return list(words)[:top_n]
    
    def ensure_context_preservation(self, original_text: str, transformed_text: str) -> bool:
        """Ensure context is preserved in transformation"""
        overlap = self.calculate_context_overlap(original_text, transformed_text)
        return overlap >= self.min_context_overlap
    
    def merge_contexts(self, contexts: List[str]) -> set:
        """Merge multiple contexts"""
        merged = set()
        for context in contexts:
            words = self.extract_context_words(context)
            merged.update(words)
        return merged

def main():
    """Test context assurance"""
    assurance = ContextAssurance()
    
    text1 = "divide cake into portions"
    text2 = "share cake portions"
    text3 = "eat cake"
    
    print("Context Assurance - Test")
    print("=" * 80)
    
    overlap12 = assurance.calculate_context_overlap(text1, text2)
    overlap13 = assurance.calculate_context_overlap(text1, text3)
    
    print(f"\nText 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Overlap: {overlap12:.2%}")
    print(f"Context maintained: {assurance.context_maintained(text1, text2)}")
    
    print(f"\nText 1: {text1}")
    print(f"Text 3: {text3}")
    print(f"Overlap: {overlap13:.2%}")
    print(f"Context maintained: {assurance.context_maintained(text1, text3)}")
    
    keywords = assurance.get_context_keywords(text1)
    print(f"\nContext keywords: {keywords}")

if __name__ == "__main__":
    main()

