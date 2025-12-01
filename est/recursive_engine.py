#!/usr/bin/env python3
"""
Recursive Engine - Main recursive loop with 5 iterations
"""

import csv
from typing import List, Dict, Tuple, Optional
from .pre_processor import PreProcessor
from .scoring_system import ScoringSystem
from .decision_engine import DecisionEngine, Decision
from .transformation_flows import TransformationFlows
from .context_assurance import ContextAssurance
from .semantic_chunker import SemanticChunker

class RecursiveEngine:
    def __init__(self, csv_path=None):
        """Initialize recursive engine"""
        if csv_path is None:
            # Try to find data file relative to package
            from pathlib import Path
            package_dir = Path(__file__).parent.parent
            default_path = package_dir / 'data' / 'check_dictionary.csv'
            if default_path.exists():
                csv_path = str(default_path)
            else:
                csv_path = 'check_dictionary.csv'
        self.csv_path = csv_path
        self.word_data = {}
        self.load_dataset()
        
        # Initialize components
        self.pre_processor = PreProcessor()
        self.scoring_system = ScoringSystem(self.word_data)
        self.decision_engine = DecisionEngine()
        self.transformation_flows = TransformationFlows()
        self.context_assurance = ContextAssurance()
        self.semantic_chunker = SemanticChunker()
        
        # For expected tokens/context guidance
        self.expected_tokens = None
        self.expected_context = None
    
    def load_dataset(self):
        """Load Sanskrit dataset from CSV"""
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sanskrit = row.get('sanskrit', '').strip()
                    if sanskrit:
                        self.word_data[sanskrit] = {
                            'english': row.get('english', '').strip(),
                            'semantic_frame': row.get('semantic_frame', '').strip(),
                            'contextual_triggers': row.get('Contextual_Triggers', '').strip(),
                            'conceptual_anchors': row.get('Conceptual_Anchors', '').strip(),
                            'ambiguity_resolvers': row.get('Ambiguity_Resolvers', '').strip(),
                            'usage_frequency_index': row.get('Usage_Frequency_Index', '').strip()
                        }
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.word_data = {}
    
    def iteration1_full_sentence(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 1: Try to match full sentence"""
        matches = self.scoring_system.find_best_matches(
            text, 
            top_n=1,
            expected_tokens=self.expected_tokens,
            expected_context=self.expected_context
        )
        
        if matches:
            sanskrit, score, breakdown = matches[0]
            decision, reason = self.decision_engine.make_decision(score, previous_score, iteration=1)
            return {
                'iteration': 1,
                'chunk': text,
                'sanskrit': sanskrit,
                'score': score,
                'breakdown': breakdown,
                'decision': decision,
                'reason': reason
            }
        
        return {
            'iteration': 1,
            'chunk': text,
            'sanskrit': None,
            'score': 0.0,
            'decision': Decision.CONTINUE,
            'reason': 'No full sentence match found'
        }
    
    def iteration2_phrase_breakdown(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 2: Break into phrases and match"""
        # Simple phrase extraction: split by common delimiters
        phrases = [p.strip() for p in text.split(',') if p.strip()]
        if not phrases:
            phrases = [text]
        
        best_phrases = []
        total_score = 0.0
        
        for phrase in phrases:
            matches = self.scoring_system.find_best_matches(
                phrase,
                top_n=1,
                expected_tokens=self.expected_tokens,
                expected_context=self.expected_context
            )
            if matches:
                sanskrit, score, breakdown = matches[0]
                if score >= 0.60:
                    best_phrases.append(sanskrit)
                    total_score += score
        
        if best_phrases:
            avg_score = total_score / len(best_phrases)
            sanskrit_output = ' '.join(best_phrases)
            decision, reason = self.decision_engine.make_decision(avg_score, previous_score, iteration=2)
            return {
                'iteration': 2,
                'chunk': text,
                'sanskrit': sanskrit_output,
                'score': avg_score,
                'breakdown': {},
                'decision': decision,
                'reason': reason
            }
        
        return {
            'iteration': 2,
            'chunk': text,
            'sanskrit': None,
            'score': 0.0,
            'decision': Decision.CONTINUE,
            'reason': 'No phrase matches found'
        }
    
    def iteration3_verb_object_pairs(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 3: Extract verb-object pairs"""
        words = text.split()
        if len(words) < 2:
            return {
                'iteration': 3,
                'chunk': text,
                'sanskrit': None,
                'score': 0.0,
                'decision': Decision.CONTINUE,
                'reason': 'Not enough words for verb-object pairs'
            }
        
        # Try 2-word combinations
        pairs = []
        for i in range(len(words) - 1):
            pair = f"{words[i]} {words[i+1]}"
            matches = self.scoring_system.find_best_matches(
                pair,
                top_n=1,
                expected_tokens=self.expected_tokens,
                expected_context=self.expected_context
            )
            if matches:
                sanskrit, score, breakdown = matches[0]
                if score >= 0.60:
                    pairs.append((pair, sanskrit, score))
        
        if pairs:
            best_pair = max(pairs, key=lambda x: x[2])
            decision, reason = self.decision_engine.make_decision(best_pair[2], previous_score, iteration=3)
            return {
                'iteration': 3,
                'chunk': text,
                'sanskrit': best_pair[1],
                'score': best_pair[2],
                'breakdown': {},
                'decision': decision,
                'reason': reason
            }
        
        return {
            'iteration': 3,
            'chunk': text,
            'sanskrit': None,
            'score': 0.0,
            'decision': Decision.CONTINUE,
            'reason': 'No verb-object pairs found'
        }
    
    def iteration4_individual_words(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 4: Match individual words"""
        words = text.split()
        matched_words = []
        total_score = 0.0
        
        for word in words:
            matches = self.scoring_system.find_best_matches(
                word,
                top_n=1,
                expected_tokens=self.expected_tokens,
                expected_context=self.expected_context
            )
            if matches:
                sanskrit, score, breakdown = matches[0]
                if score >= 0.60:
                    matched_words.append(sanskrit)
                    total_score += score
                else:
                    matched_words.append(word)  # Keep original if low score
            else:
                matched_words.append(word)  # Keep original if no match
        
        if matched_words:
            matched_count = len([w for w in matched_words if w in self.word_data])
            avg_score = total_score / matched_count if matched_count > 0 else 0.0
            sanskrit_output = ' '.join(matched_words)
            decision, reason = self.decision_engine.make_decision(avg_score, previous_score, iteration=4)
            return {
                'iteration': 4,
                'chunk': text,
                'sanskrit': sanskrit_output,
                'score': avg_score,
                'breakdown': {},
                'decision': decision,
                'reason': reason
            }
        
        return {
            'iteration': 4,
            'chunk': text,
            'sanskrit': None,
            'score': 0.0,
            'decision': Decision.CONTINUE,
            'reason': 'No individual word matches'
        }
    
    def iteration5_final_resolution(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 5: Final resolution with lower threshold"""
        matches = self.scoring_system.find_best_matches(
            text,
            top_n=5,
            expected_tokens=self.expected_tokens,
            expected_context=self.expected_context
        )
        
        if matches:
            # Use best match even with lower score
            best_result = matches[0]
            sanskrit, score, breakdown = best_result
            
            # Lower threshold for final resolution
            if score >= 0.30:
                decision, reason = self.decision_engine.make_decision(score, previous_score, iteration=5)
                return {
                    'iteration': 5,
                    'chunk': text,
                    'sanskrit': sanskrit,
                    'score': score,
                    'breakdown': breakdown,
                    'decision': decision,
                    'reason': reason
                }
        
        return {
            'iteration': 5,
            'chunk': text,
            'sanskrit': None,
            'score': 0.0,
            'decision': Decision.REJECT,
            'reason': 'No matches found in final resolution'
        }
    
    def process_chunk(self, text: str) -> Dict:
        """
        Process a chunk through all 5 iterations
        Returns: Final result with best match
        """
        results = []
        previous_score = None
        previous_text = text
        
        # Iteration 1: Full sentence
        result1 = self.iteration1_full_sentence(text, previous_score)
        results.append(result1)
        
        if result1['decision'] == Decision.ACCEPT:
            return result1
        
        previous_score = result1['score']
        
        # Iteration 2: Phrase breakdown
        result2 = None
        if result1['decision'] == Decision.CONTINUE:
            result2 = self.iteration2_phrase_breakdown(text, previous_score)
            results.append(result2)
            
            if result2['decision'] == Decision.ACCEPT:
                return result2
            
            if result2['score'] > previous_score:
                previous_score = result2['score']
        
        # Iteration 3: Verb-object pairs
        result3 = None
        if (result2 and result2.get('decision') == Decision.CONTINUE) or (not result2 and result1['decision'] == Decision.CONTINUE):
            result3 = self.iteration3_verb_object_pairs(text, previous_score)
            results.append(result3)
            
            if result3['decision'] == Decision.ACCEPT:
                return result3
            
            if result3['score'] > previous_score:
                previous_score = result3['score']
        
        # Iteration 4: Individual words
        result4 = None
        if (result3 and result3.get('decision') == Decision.CONTINUE) or (not result3 and result1['decision'] == Decision.CONTINUE):
            result4 = self.iteration4_individual_words(text, previous_score)
            results.append(result4)
            
            if result4['decision'] == Decision.ACCEPT:
                return result4
            
            if result4['score'] > previous_score:
                previous_score = result4['score']
        
        # Iteration 5: Final resolution (always run if we haven't accepted)
        result5 = self.iteration5_final_resolution(text, previous_score)
        results.append(result5)
        
        # Return best result
        best_result = max(results, key=lambda x: x.get('score', 0.0))
        best_result['all_iterations'] = results
        
        return best_result
    
    def process_text(self, text: str, expected_tokens: List[str] = None, expected_context: str = None) -> Dict:
        """
        Process full text with semantic chunking (SVO relationships) for context preservation
        Breaks and rearranges sentences to preserve subject-verb-object relationships
        Tries longest phrases first (4 → 3 → 2 → 1 words) to achieve 50-70% reduction
        Unmatched words are preserved in English
        Returns: Complete processing result
        """
        # Store expected tokens for use in scoring
        self.expected_tokens = expected_tokens
        self.expected_context = expected_context
        
        # Pre-process
        preprocessed = self.pre_processor.process(text)
        
        # Get original words maintaining order
        original_words = text.split()
        
        # Step 1: Semantic chunking - identify SVO relationships
        # Temporarily disable semantic chunking for simple sentences to ensure all words are processed
        # Only use semantic chunking for longer, more complex sentences
        if len(original_words) > 10:
            semantic_phrases = self.semantic_chunker.create_semantic_phrases(text)
        else:
            semantic_phrases = []  # Skip semantic chunking for short sentences
        
        # Stop words to keep as-is (not tokenized)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'do', 'does', 'did',
                     'we', 'need', 'how', 'into', 'have', 'has', 'had', 'will', 'would', 'could', 'should'}
        
        # Helper functions
        def is_stop_word(w):
            return w.lower().strip('.,!?;:()[]{}') in stop_words
        
        def clean_word(w):
            return w.lower().strip('.,!?;:()[]{}')
        
        # Track which words have been processed
        processed = [False] * len(original_words)
        output_parts = []
        word_results = []
        total_confidence = 0.0
        matched_count = 0
        
        # Step 2: Process semantic phrases (SVO relationships) first
        # This preserves context by matching subject-verb-object as units
        # Only process if we have meaningful semantic phrases (not just single words)
        if len(semantic_phrases) > 1 or (len(semantic_phrases) == 1 and len(semantic_phrases[0].split()) > 2):
            for phrase in semantic_phrases:
                # Skip single word phrases here - they'll be handled in greedy matching
                if len(phrase.split()) <= 1:
                    continue
                    
                # Try to match the entire semantic phrase
                phrase_result = self.process_chunk(phrase)
                
                # Lower threshold for semantic phrases (they preserve context)
                score_threshold = 0.30 if len(phrase.split()) >= 3 else 0.40
                
                if phrase_result.get('sanskrit') and phrase_result.get('score', 0.0) >= score_threshold:
                    # Good semantic phrase match - preserves SVO relationship
                    output_parts.append(phrase_result.get('sanskrit'))
                    word_results.append(phrase_result)
                    total_confidence += phrase_result.get('score', 0.0)
                    matched_count += len([w for w in phrase.split() if not is_stop_word(w)])
                    
                    # Mark words in phrase as processed
                    phrase_words = phrase.split()
                    for word in phrase_words:
                        # Find word in original text
                        for idx, orig_word in enumerate(original_words):
                            if not processed[idx] and clean_word(orig_word) == clean_word(word):
                                processed[idx] = True
                                break
        
        # Step 3: Greedy phrase matching for remaining words
        # Process words sequentially, trying to match phrases when possible
        i = 0
        while i < len(original_words):
            if processed[i]:
                i += 1
                continue
            
            word = original_words[i]
            word_clean = clean_word(word)
            
            # Keep stop words as-is
            if is_stop_word(word):
                output_parts.append(word)
                processed[i] = True
                i += 1
                continue
            
            # Try to find best phrase match starting at position i
            # Look ahead up to 6 words to find meaningful word sequences
            best_match = None
            best_score = 0.0
            best_meaningful_count = 0
            
            # Try phrases of different lengths (greedy: longest first)
            # Start from single word (i+1) to allow single word matches if no phrases work
            max_lookahead = min(6, len(original_words) - i)
            
            for end_pos in range(i + 1, i + max_lookahead + 1):
                # Extract phrase words from i to end_pos
                phrase_words = original_words[i:end_pos]
                
                # Skip if any word in phrase is already processed
                if any(processed[i + j] for j in range(end_pos - i)):
                    continue
                
                # Extract meaningful words (skip stop words for matching)
                meaningful_words = []
                meaningful_indices = []
                for j, w in enumerate(phrase_words):
                    if not is_stop_word(w):
                        meaningful_words.append(clean_word(w))
                        meaningful_indices.append(i + j)
                
                # Need at least 1 meaningful word
                if len(meaningful_words) < 1:
                    continue
                
                # For phrase matching, we need at least 2 meaningful words
                # Single words will be handled in the else block below
                if len(meaningful_words) < 2:
                    continue
                
                # Build phrase for matching (meaningful words only)
                phrase = ' '.join(meaningful_words)
                
                # Try to match this phrase
                phrase_result = self.process_chunk(phrase)
                
                # Score threshold: lower for longer phrases (encourages compression)
                # Also lower overall to allow more matches
                score_threshold = 0.30 if len(meaningful_words) >= 3 else 0.40
                
                if phrase_result.get('sanskrit') and phrase_result.get('score', 0.0) >= score_threshold:
                    current_score = phrase_result.get('score', 0.0)
                    # Prefer longer phrases with good scores
                    if current_score > best_score or (current_score == best_score and len(meaningful_words) > best_meaningful_count):
                        best_match = {
                            'sanskrit': phrase_result.get('sanskrit'),
                            'score': current_score,
                            'word_count': end_pos - i,  # Total words in phrase (including stop words)
                            'meaningful_count': len(meaningful_words),
                            'result': phrase_result,
                            'words': phrase_words,
                            'meaningful_indices': meaningful_indices
                        }
                        best_score = current_score
                        best_meaningful_count = len(meaningful_words)
            
            # Use best phrase match if found
            if best_match:
                # Add Sanskrit token (replaces all meaningful words in the phrase)
                output_parts.append(best_match['sanskrit'])
                word_results.append(best_match['result'])
                total_confidence += best_match['score']
                matched_count += best_match['meaningful_count']
                
                # Mark all words in phrase as processed
                # Meaningful words are replaced by Sanskrit, stop words are added separately
                for j in range(best_match['word_count']):
                    word_idx = i + j
                    word = original_words[word_idx]
                    
                    if is_stop_word(word):
                        # Add stop word to output (preserve in original position)
                        output_parts.append(word)
                    
                    # Mark as processed
                    processed[word_idx] = True
                
                # Move past all words in the phrase
                i += best_match['word_count']
            else:
                # No phrase match, try single word
                word_result = self.process_chunk(word_clean)
                
                # Lower threshold for single words - accept if score > 0.10 (10%)
                # This allows more words to be matched, improving tokenization
                # Even low-confidence matches are better than keeping English words
                min_score = 0.10
                
                if word_result.get('sanskrit') and word_result.get('score', 0.0) >= min_score:
                    # Acceptable single word match
                    output_parts.append(word_result.get('sanskrit'))
                    word_results.append(word_result)
                    total_confidence += word_result.get('score', 0.0)
                    matched_count += 1
                else:
                    # No good match - keep original English word
                    output_parts.append(word)
                
                processed[i] = True
                i += 1
        
        # Safety check: ensure all words are processed
        # Add any unprocessed words to output
        for idx in range(len(original_words)):
            if not processed[idx]:
                word = original_words[idx]
                # Try to match it as single word first (if not stop word)
                if not is_stop_word(word):
                    word_result = self.process_chunk(clean_word(word))
                    # Lower threshold for safety check - accept if score > 0.25
                    if word_result.get('sanskrit') and word_result.get('score', 0.0) >= 0.25:
                        output_parts.append(word_result.get('sanskrit'))
                        word_results.append(word_result)
                        total_confidence += word_result.get('score', 0.0)
                        matched_count += 1
                    else:
                        output_parts.append(word)
                else:
                    output_parts.append(word)
                processed[idx] = True
        
        # Build final output
        sanskrit_output = ' '.join(output_parts)
        
        # Calculate average confidence
        avg_confidence = total_confidence / matched_count if matched_count > 0 else 0.0
        
        # Calculate token reduction
        input_tokens = len(original_words)
        output_tokens = len(sanskrit_output.split())
        token_reduction = ((input_tokens - output_tokens) / input_tokens * 100) if input_tokens > 0 else 0.0
        
        # Create summary result
        summary_result = {
            'iteration': 'greedy-phrase-matching',
            'chunk': text,
            'sanskrit': sanskrit_output,
            'score': avg_confidence,
            'breakdown': {},
            'decision': Decision.ACCEPT if matched_count > 0 else Decision.REJECT,
            'reason': f'Processed {matched_count} words/phrases, {len(original_words) - matched_count} kept in English. Token reduction: {token_reduction:.1f}%'
        }
        
        return {
            'original_text': text,
            'preprocessed': preprocessed,
            'final_result': summary_result,
            'sanskrit_output': sanskrit_output,
            'confidence': avg_confidence,
            'word_results': word_results,
            'matched_count': matched_count,
            'total_words': len(original_words),
            'output_tokens': output_tokens,
            'token_reduction': token_reduction
        }
