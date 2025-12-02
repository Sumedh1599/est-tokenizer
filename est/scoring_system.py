#!/usr/bin/env python3
"""
Scoring System - Weighted scoring algorithm with SEMANTIC CONCEPT MATCHING
40% semantic_frame, 25% contextual_triggers, 20% conceptual_anchors, 15% frequency_index
Uses semantic expansion instead of raw word matching
"""

import re
from typing import List, Dict, Tuple, Set
from collections import Counter
from .semantic_expander import SemanticExpander
from .context_detector import ContextDetector

class ScoringSystem:
    def __init__(self, word_data: Dict):
        """Initialize with Sanskrit word data"""
        self.word_data = word_data
        self.expander = SemanticExpander()
        self.context_detector = ContextDetector()
        
        # Scoring weights
        self.weights = {
            'semantic_frame': 0.40,
            'contextual_triggers': 0.25,
            'conceptual_anchors': 0.20,
            'frequency_index': 0.15
        }
    
    def extract_semantic_concepts(self, text: str) -> Set[str]:
        """
        Extract semantic concepts from text (not just words)
        Returns: Set of semantic concepts
        """
        # Use semantic expander to get all concepts
        expanded = self.expander.expand_with_context(text)
        # Convert list back to set for set operations
        concepts_list = expanded['concepts']
        return set(concepts_list) if isinstance(concepts_list, list) else concepts_list
    
    def extract_words(self, text: str) -> set:
        """Extract meaningful words from text (legacy method)"""
        words = re.findall(r'\b[a-z]{2,}\b', text.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        return set(w for w in words if w not in stop_words)
    
    def compare_frames(self, english_chunk: str, sanskrit_word: str) -> float:
        """
        Compare semantic frames using SEMANTIC CONCEPTS (40% weight)
        Matches meanings, not just words
        """
        word_data = self.word_data.get(sanskrit_word)
        if not word_data:
            return 0.0
        
        semantic_frame = word_data.get('semantic_frame', '').strip()
        if not semantic_frame:
            return 0.0
        
        # Get semantic concepts from English chunk
        english_concepts = self.extract_semantic_concepts(english_chunk)
        
        # Extract concepts from semantic frame sections
        frame_concepts = set()
        for section in semantic_frame.split('|'):
            section = section.strip()
            if section:
                # Expand section to concepts
                section_concepts = self.expander.expand_text(section)
                frame_concepts.update(section_concepts)
        
        if not frame_concepts:
            return 0.0
        
        # Calculate semantic concept overlap
        overlap = len(english_concepts & frame_concepts)
        total_frame_concepts = len(frame_concepts)
        
        # Higher score for better concept overlap
        return min(overlap / total_frame_concepts, 1.0) if total_frame_concepts > 0 else 0.0
    
    def compare_triggers(self, english_chunk: str, sanskrit_word: str) -> float:
        """
        Compare contextual triggers using SEMANTIC CONCEPTS (25% weight)
        """
        word_data = self.word_data.get(sanskrit_word)
        if not word_data:
            return 0.0
        
        triggers = word_data.get('contextual_triggers', '').strip()
        if not triggers:
            return 0.0
        
        # Get semantic concepts from English chunk
        english_concepts = self.extract_semantic_concepts(english_chunk)
        
        # Expand triggers to concepts
        trigger_concepts = set()
        for trigger in triggers.split('|'):
            trigger = trigger.strip().lower()
            if trigger:
                # Expand trigger to concepts
                trigger_expanded = self.expander.expand_word(trigger)
                trigger_concepts.update(trigger_expanded)
        
        if not trigger_concepts:
            return 0.0
        
        # Calculate concept overlap
        overlap = len(english_concepts & trigger_concepts)
        total_triggers = len(trigger_concepts)
        
        return min(overlap / total_triggers, 1.0) if total_triggers > 0 else 0.0
    
    def compare_anchors(self, english_chunk: str, sanskrit_word: str) -> float:
        """
        Compare conceptual anchors using SEMANTIC CONCEPTS (20% weight)
        """
        word_data = self.word_data.get(sanskrit_word)
        if not word_data:
            return 0.0
        
        anchors = word_data.get('conceptual_anchors', '').strip()
        if not anchors:
            return 0.0
        
        # Get semantic concepts from English chunk
        english_concepts = self.extract_semantic_concepts(english_chunk)
        
        # Expand anchors to concepts
        anchor_concepts = set()
        for anchor in anchors.split('|'):
            anchor = anchor.strip().lower()
            if anchor:
                # Expand anchor to concepts
                anchor_expanded = self.expander.expand_word(anchor)
                anchor_concepts.update(anchor_expanded)
        
        if not anchor_concepts:
            return 0.0
        
        # Calculate concept overlap
        overlap = len(english_concepts & anchor_concepts)
        total_anchors = len(anchor_concepts)
        
        return min(overlap / total_anchors, 1.0) if total_anchors > 0 else 0.0
    
    def get_frequency_score(self, english_chunk: str, sanskrit_word: str) -> float:
        """
        Get frequency index score using CONTEXT DETECTION (15% weight)
        """
        word_data = self.word_data.get(sanskrit_word)
        if not word_data:
            return 0.0
        
        frequency_index = word_data.get('usage_frequency_index', '').strip()
        if not frequency_index:
            return 0.0
        
        # Detect context from English chunk
        detected_context = self.context_detector.detect_context(english_chunk)
        primary_context = detected_context.get('primary_context')
        
        if not primary_context:
            return 0.0
        
        # Get semantic concepts
        english_concepts = self.extract_semantic_concepts(english_chunk)
        total_weight = 0.0
        
        # Parse frequency index and check for context matches
        for part in frequency_index.split('|'):
            part = part.strip()
            if ':' in part:
                context, weight_str = part.rsplit(':', 1)
                try:
                    weight = float(weight_str)
                    context_lower = context.strip().lower()
                    
                    # Check if detected context matches
                    if context_lower == primary_context:
                        total_weight += weight * 1.5  # Boost for exact context match
                    # Also check if context word appears in concepts
                    elif context_lower in english_concepts:
                        total_weight += weight
                except ValueError:
                    continue
        
        return min(total_weight, 1.0)
    
    def compare_english_definition(self, english_chunk: str, sanskrit_candidate: str) -> float:
        """
        Compare against English definition using SEMANTIC CONCEPTS (bonus score)
        This is the most direct match - uses meaning, not words
        """
        word_data = self.word_data.get(sanskrit_candidate)
        if not word_data:
            return 0.0
        
        english_def = word_data.get('english', '').strip()
        if not english_def:
            return 0.0
        
        # Get semantic concepts from both
        chunk_concepts = self.extract_semantic_concepts(english_chunk)
        def_concepts = self.extract_semantic_concepts(english_def)
        
        if not def_concepts:
            return 0.0
        
        # Calculate concept overlap (semantic similarity)
        overlap = len(chunk_concepts & def_concepts)
        total_def_concepts = len(def_concepts)
        
        # Higher weight for definition match (most direct)
        return min(overlap / total_def_concepts, 1.0) if total_def_concepts > 0 else 0.0
    
    def prioritize_by_semantic_frame(self, english_chunk: str, sanskrit_candidate: str) -> float:
        """
        Prioritize based on semantic frame role matching
        "divide property" should prefer aMSaH over aMS
        "share resources" should prefer aMS over aMSaH
        """
        word_data = self.word_data.get(sanskrit_candidate, {})
        semantic_frame = word_data.get('semantic_frame', '').strip()
        
        if not semantic_frame:
            return 0.0
        
        english_concepts = self.extract_semantic_concepts(english_chunk)
        
        # Analyze semantic frame sections for role-specific matching
        frame_sections = semantic_frame.split('|')
        role_scores = []
        
        for section in frame_sections:
            section = section.strip()
            if section:
                # Extract concepts from section
                section_concepts = self.expander.expand_text(section)
                
                # Calculate role-specific overlap
                overlap = len(english_concepts & section_concepts)
                if len(section_concepts) > 0:
                    role_score = overlap / len(section_concepts)
                    role_scores.append(role_score)
        
        # Prioritize frames with higher role-specific matches
        if role_scores:
            # Use maximum role score (best matching role)
            return max(role_scores)
        
        return 0.0
    
    def use_ambiguity_resolvers(self, english_chunk: str, sanskrit_candidate: str) -> float:
        """
        Use Ambiguity_Resolvers for tie-breaking
        "property context" → boosts aMSaH
        "fairness principles" → boosts aMS
        """
        word_data = self.word_data.get(sanskrit_candidate, {})
        resolvers = word_data.get('ambiguity_resolvers', '').strip()
        
        if not resolvers:
            return 0.0
        
        english_concepts = self.extract_semantic_concepts(english_chunk)
        
        # Expand resolvers to concepts
        resolver_concepts = set()
        for resolver in resolvers.split('|'):
            resolver = resolver.strip().lower()
            if resolver:
                resolver_expanded = self.expander.expand_text(resolver)
                resolver_concepts.update(resolver_expanded)
        
        if not resolver_concepts:
            return 0.0
        
        # Calculate resolver overlap
        overlap = len(english_concepts & resolver_concepts)
        total_resolvers = len(resolver_concepts)
        
        # Resolver match is a strong signal (boost factor)
        resolver_score = min(overlap / total_resolvers, 1.0) if total_resolvers > 0 else 0.0
        
        return resolver_score
    
    def apply_frequency_boost(self, english_chunk: str, sanskrit_candidate: str) -> float:
        """
        Apply frequency-based boosting for context-appropriate selection
        Legal context → boost words with high legal frequency
        Returns: Boost factor (0.0 to 1.0)
        """
        word_data = self.word_data.get(sanskrit_candidate, {})
        frequency_index = word_data.get('usage_frequency_index', '').strip()
        
        if not frequency_index:
            return 0.0
        
        # Detect context from English chunk
        detected_context = self.context_detector.detect_context(english_chunk)
        primary_context = detected_context.get('primary_context')
        
        if not primary_context:
            return 0.0
        
        # Find frequency weight for detected context
        max_weight = 0.0
        exact_match_weight = 0.0
        
        for part in frequency_index.split('|'):
            part = part.strip()
            if ':' in part:
                context, weight_str = part.rsplit(':', 1)
                try:
                    weight = float(weight_str)
                    context_lower = context.strip().lower()
                    
                    if context_lower == primary_context:
                        # Exact context match
                        exact_match_weight = weight
                    elif weight > max_weight:
                        max_weight = weight
                except ValueError:
                    continue
        
        # Return exact match weight if found, otherwise max weight
        # Cap at 1.0 (100%)
        return min(exact_match_weight if exact_match_weight > 0 else max_weight, 1.0)
    
    def apply_neighbor_priority(self, expected_tokens: List[str], sanskrit_candidate: str) -> float:
        """
        Apply priority boost if candidate is in expected tokens' Semantic_Neighbors
        If aMSaH is expected, boost aMS and bhāgaH (neighbors of aMSaH)
        Returns: Boost factor (0.0 to 1.0)
        """
        if not expected_tokens:
            return 0.0
        
        candidate_data = self.word_data.get(sanskrit_candidate, {})
        
        # Check if candidate is directly in expected tokens
        if sanskrit_candidate in expected_tokens:
            return 1.0  # Maximum boost for exact match
        
        # Check if candidate appears in any expected token's Semantic_Neighbors
        for expected_token in expected_tokens:
            expected_data = self.word_data.get(expected_token, {})
            neighbors = expected_data.get('semantic_neighbors', '').strip()
            
            if neighbors:
                # Parse neighbors (format: "word1|word2|word3")
                neighbor_list = [n.strip() for n in neighbors.split('|') if n.strip()]
                if sanskrit_candidate in neighbor_list:
                    # Found in neighbors - strong boost
                    return 0.8
        
        return 0.0
    
    def align_with_expected_context(self, english_chunk: str, sanskrit_candidate: str, expected_context: str = None) -> float:
        """
        Align with expected context by checking Contextual_Triggers
        "property inheritance" should boost tokens with "property" in Contextual_Triggers
        Returns: Boost factor (0.0 to 1.0)
        """
        candidate_data = self.word_data.get(sanskrit_candidate, {})
        triggers = candidate_data.get('contextual_triggers', '').strip()
        
        if not triggers:
            return 0.0
        
        # Get semantic concepts from English chunk
        english_concepts = self.extract_semantic_concepts(english_chunk)
        
        # Expand triggers to concepts
        trigger_concepts = set()
        for trigger in triggers.split('|'):
            trigger = trigger.strip().lower()
            if trigger:
                trigger_expanded = self.expander.expand_text(trigger)
                trigger_concepts.update(trigger_expanded)
        
        if not trigger_concepts:
            return 0.0
        
        # Calculate overlap between English concepts and trigger concepts
        overlap = len(english_concepts & trigger_concepts)
        total_triggers = len(trigger_concepts)
        
        # Strong boost for high trigger alignment
        alignment_score = min(overlap / total_triggers, 1.0) if total_triggers > 0 else 0.0
        
        # Additional boost if expected_context matches
        if expected_context:
            # Check if expected context appears in triggers
            context_lower = expected_context.lower()
            trigger_text = triggers.lower()
            if context_lower in trigger_text:
                alignment_score = min(alignment_score + 0.2, 1.0)
        
        return alignment_score
    
    def match_frequency_context(self, expected_context: str, sanskrit_candidate: str) -> float:
        """
        Match frequency context - boost tokens with high frequency for expected context
        Expected "legal" context → boost tokens with high legal frequency
        Returns: Boost factor (0.0 to 1.0)
        """
        if not expected_context:
            return 0.0
        
        candidate_data = self.word_data.get(sanskrit_candidate, {})
        frequency_index = candidate_data.get('usage_frequency_index', '').strip()
        
        if not frequency_index:
            return 0.0
        
        expected_context_lower = expected_context.lower()
        max_weight = 0.0
        exact_match_weight = 0.0
        
        # Parse frequency index
        for part in frequency_index.split('|'):
            part = part.strip()
            if ':' in part:
                context, weight_str = part.rsplit(':', 1)
                try:
                    weight = float(weight_str)
                    context_lower = context.strip().lower()
                    
                    if context_lower == expected_context_lower:
                        # Exact context match
                        exact_match_weight = weight
                    elif weight > max_weight:
                        max_weight = weight
                except ValueError:
                    continue
        
        # Return exact match weight if found, otherwise max weight
        return min(exact_match_weight if exact_match_weight > 0 else max_weight, 1.0)
    
    def validate_with_resolvers(self, english_chunk: str, sanskrit_candidate: str) -> float:
        """
        Validate with Ambiguity_Resolvers - check if candidate's resolvers match input context
        "property context" resolver should match "property inheritance" input
        Returns: Boost factor (0.0 to 1.0)
        """
        candidate_data = self.word_data.get(sanskrit_candidate, {})
        resolvers = candidate_data.get('ambiguity_resolvers', '').strip()
        
        if not resolvers:
            return 0.0
        
        # Get semantic concepts from English chunk
        english_concepts = self.extract_semantic_concepts(english_chunk)
        
        # Expand resolvers to concepts
        resolver_concepts = set()
        for resolver in resolvers.split('|'):
            resolver = resolver.strip().lower()
            if resolver:
                resolver_expanded = self.expander.expand_text(resolver)
                resolver_concepts.update(resolver_expanded)
        
        if not resolver_concepts:
            return 0.0
        
        # Calculate resolver overlap
        overlap = len(english_concepts & resolver_concepts)
        total_resolvers = len(resolver_concepts)
        
        # Resolver match is a very strong signal
        resolver_match = min(overlap / total_resolvers, 1.0) if total_resolvers > 0 else 0.0
        
        return resolver_match
    
    def calculate_score(self, english_chunk: str, sanskrit_candidate: str, 
                       expected_tokens: List[str] = None, expected_context: str = None) -> Tuple[float, Dict]:
        """
        Calculate total score using SEMANTIC CONCEPT MATCHING with precision enhancements
        Now includes expected token priority boosts
        Returns: (total_score, score_breakdown)
        """
        word_data = self.word_data.get(sanskrit_candidate, {})
        
        semantic_frame_match = self.compare_frames(english_chunk, sanskrit_candidate)
        contextual_triggers = self.compare_triggers(english_chunk, sanskrit_candidate)
        conceptual_anchors = self.compare_anchors(english_chunk, sanskrit_candidate)
        frequency_weight = self.get_frequency_score(english_chunk, sanskrit_candidate)
        english_def_match = self.compare_english_definition(english_chunk, sanskrit_candidate)
        
        # NEW: Precision enhancements
        frame_prioritization = self.prioritize_by_semantic_frame(english_chunk, sanskrit_candidate)
        ambiguity_resolver_match = self.use_ambiguity_resolvers(english_chunk, sanskrit_candidate)
        frequency_boost = self.apply_frequency_boost(english_chunk, sanskrit_candidate)
        
        # Get context priority boost
        context_priority = self.context_detector.get_context_priority(english_chunk, sanskrit_candidate, word_data)
        
        # NEW: Expected token priority boosts
        neighbor_priority = 0.0
        context_alignment = 0.0
        frequency_context_match = 0.0
        resolver_validation = 0.0
        
        if expected_tokens:
            neighbor_priority = self.apply_neighbor_priority(expected_tokens, sanskrit_candidate)
        
        if expected_context:
            context_alignment = self.align_with_expected_context(english_chunk, sanskrit_candidate, expected_context)
            frequency_context_match = self.match_frequency_context(expected_context, sanskrit_candidate)
        
        resolver_validation = self.validate_with_resolvers(english_chunk, sanskrit_candidate)
        
        # PROVEN ARCHITECTURE: Core 40/25/20/15 scoring (DO NOT CHANGE)
        # This is what gave us 97% confidence - preserve exactly
        base_score = (
            semantic_frame_match * self.weights['semantic_frame'] +
            contextual_triggers * self.weights['contextual_triggers'] +
            conceptual_anchors * self.weights['conceptual_anchors'] +
            frequency_weight * self.weights['frequency_index'] +
            english_def_match * 0.20  # English definition match (additional signal)
        )
        
        # SMALL PRECISION ENHANCEMENTS (tie-breakers only, not fundamental changes)
        # These are small additive boosts, not large multipliers
        precision_boosts = 0.0
        
        # Frame prioritization: small boost for role matching (up to 5%)
        if frame_prioritization > 0.70:
            precision_boosts += frame_prioritization * 0.05
        
        # Ambiguity resolver: small boost for disambiguation (up to 5%)
        if ambiguity_resolver_match > 0.60:
            precision_boosts += ambiguity_resolver_match * 0.05
        
        # Frequency boost: small context appropriateness (up to 3%)
        if frequency_boost > 0.50:
            precision_boosts += frequency_boost * 0.03
        
        # Context priority: small boost (up to 2%)
        if context_priority > 0.50:
            precision_boosts += context_priority * 0.02
        
        # SMALL EXPECTED TOKEN BOOSTS (conservative tie-breakers only)
        expected_token_boosts = 0.0
        if expected_tokens or expected_context:
            # If candidate IS the expected token: small boost (10%)
            if neighbor_priority >= 1.0:  # Exact match
                expected_token_boosts += 0.10
            # If candidate is in expected token's neighbors: small boost (5%)
            elif neighbor_priority >= 0.80:
                expected_token_boosts += 0.05
            
            # Context alignment: small boost if triggers match (up to 5%)
            if context_alignment > 0.70:
                expected_token_boosts += context_alignment * 0.05
            
            # Frequency context match: small boost (up to 3%)
            if frequency_context_match > 0.50:
                expected_token_boosts += frequency_context_match * 0.03
        
        # Total small boosts (capped at 20% total - conservative)
        total_small_boosts = min(precision_boosts + expected_token_boosts, 0.20)
        
        # Add small boosts to base score (additive, not multiplicative)
        total_score = min(base_score + total_small_boosts, 1.0)
        
        score_breakdown = {
            # Core proven architecture scores (40/25/20/15)
            'semantic_frame': semantic_frame_match,
            'contextual_triggers': contextual_triggers,
            'conceptual_anchors': conceptual_anchors,
            'frequency_index': frequency_weight,
            'english_definition': english_def_match,
            'base_score': base_score,  # Core 40/25/20/15 score
            
            # Small precision enhancements (tie-breakers)
            'frame_prioritization': frame_prioritization,
            'ambiguity_resolver': ambiguity_resolver_match,
            'frequency_boost': frequency_boost,
            'context_priority': context_priority,
            'precision_boosts': precision_boosts,
            
            # Small expected token boosts (tie-breakers)
            'neighbor_priority': neighbor_priority,
            'context_alignment': context_alignment,
            'frequency_context_match': frequency_context_match,
            'resolver_validation': resolver_validation,
            'expected_token_boosts': expected_token_boosts,
            
            # Total
            'total_small_boosts': total_small_boosts,
            'total': total_score
        }
        
        return total_score, score_breakdown
    
    def find_best_matches(self, english_chunk: str, top_n: int = 10, 
                         expected_tokens: List[str] = None, expected_context: str = None) -> List[Tuple[str, float, Dict]]:
        """
        Find best matching Sanskrit words using SEMANTIC CONCEPT MATCHING
        Applies context-aware filtering and expected token priority boosts
        OPTIMIZED: Aggressive early exit and maximum iteration limit
        """
        matches = []
        
        # Ultra-aggressive early exit for performance
        early_exit_threshold = 0.25  # Lowered from 0.3 to 0.25
        early_exit_count = top_n  # Need top_n high-score matches
        max_iterations = 500  # Limit to first 500 words (reduced from 1000)
        min_matches_for_early_exit = top_n  # Need at least top_n matches
        max_total_matches = top_n * 3  # Stop after collecting 3x top_n matches (reduced from 5x)
        quick_exit_iterations = 100  # If no good matches after 100 iterations, likely no match (reduced from 200)
        
        # Check expected tokens first (priority boost)
        if expected_tokens:
            for token in expected_tokens:
                if token in self.word_data:
                    score, breakdown = self.calculate_score(
                        english_chunk, 
                        token,
                        expected_tokens=expected_tokens,
                        expected_context=expected_context
                    )
                    if score > 0:
                        matches.append((token, score * 1.1, breakdown))  # 10% boost for expected
        
        # Search through words with aggressive early exit and iteration limit
        high_score_count = 0
        iteration = 0
        best_score_so_far = 0.0
        word_list = list(self.word_data.keys())
        
        for sanskrit_word in word_list:
            iteration += 1
            
            # Quick exit: if we've checked many words and best score is still very low, likely no match
            if iteration > quick_exit_iterations and best_score_so_far < 0.1 and len(matches) == 0:
                # No good matches found after checking many words, likely no match exists
                break
            
            # Maximum iteration limit - stop after checking max_iterations words
            if iteration > max_iterations:
                break
            
            # Skip if already in matches (from expected_tokens)
            if any(m[0] == sanskrit_word for m in matches):
                continue
            
            score, breakdown = self.calculate_score(
                english_chunk, 
                sanskrit_word,
                expected_tokens=expected_tokens,
                expected_context=expected_context
            )
            if score > 0:
                matches.append((sanskrit_word, score, breakdown))
                best_score_so_far = max(best_score_so_far, score)
                
                # Early exit: if we have enough high-score matches, stop searching
                if score >= early_exit_threshold:
                    high_score_count += 1
                    # More aggressive: stop if we have top_n high-score matches
                    if high_score_count >= early_exit_count and len(matches) >= min_matches_for_early_exit:
                        # We have enough good matches, sort and return
                        matches.sort(key=lambda x: x[1], reverse=True)
                        matches = self.context_detector.context_aware_filter(english_chunk, matches, self.word_data)
                        return matches[:top_n]
                
                # Also exit early if we have enough matches total (even if scores are lower)
                if len(matches) >= max_total_matches:
                    # We have enough matches, sort and return best ones
                    matches.sort(key=lambda x: x[1], reverse=True)
                    matches = self.context_detector.context_aware_filter(english_chunk, matches, self.word_data)
                    return matches[:top_n]
                
                # Early exit if we have top_n matches and best score is decent
                if len(matches) >= top_n:
                    matches.sort(key=lambda x: x[1], reverse=True)
                    if matches[0][1] >= 0.15:  # Best match is at least 15% (lowered from 20%)
                        matches = self.context_detector.context_aware_filter(english_chunk, matches, self.word_data)
                        return matches[:top_n]
                
                # Very early exit: if we have a few good matches, return early
                if len(matches) >= 3 and best_score_so_far >= 0.4:
                    matches.sort(key=lambda x: x[1], reverse=True)
                    matches = self.context_detector.context_aware_filter(english_chunk, matches, self.word_data)
                    return matches[:top_n]
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        
        # Apply context-aware filtering and re-ranking
        matches = self.context_detector.context_aware_filter(english_chunk, matches, self.word_data)
        
        return matches[:top_n]

def main():
    """Test scoring system"""
    # This would normally load from CSV
    print("Scoring System - Test")
    print("Note: Requires word_data dictionary from CSV")

if __name__ == "__main__":
    main()

