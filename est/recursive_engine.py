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
        self.transformer = TransformationFlows()
        self.context_assurance = ContextAssurance()
        
        # Expected tokens for testing (optional)
        self.expected_tokens = None
        self.expected_context = None
    
    def load_dataset(self):
        """Load Sanskrit word data from CSV"""
        print("Loading dataset...")
        
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
                        'usage_frequency_index': row.get('Usage_Frequency_Index', '').strip(),
                        'semantic_neighbors': row.get('Semantic_Neighbors', '').strip()
                    }
        
        print(f"Loaded {len(self.word_data)} Sanskrit words")
    
    def iteration1_full_sentence(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 1: Full sentence scoring"""
        matches = self.scoring_system.find_best_matches(
            text, top_n=1, 
            expected_tokens=self.expected_tokens, 
            expected_context=self.expected_context
        )
        
        if matches:
            sanskrit, score, breakdown = matches[0]
            decision, reason = self.decision_engine.make_decision(score, previous_score, 1, "full_sentence")
            
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
            'breakdown': {},
            'decision': Decision.REJECT,
            'reason': 'No matches found'
        }
    
    def iteration2_phrase_breakdown(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 2: Phrase breakdown"""
        preprocessed = self.pre_processor.process(text)
        phrases = preprocessed['phrases']
        
        if not phrases:
            # Fallback to simple word groups
            words = preprocessed['filtered']
            if len(words) >= 2:
                phrases = [(' '.join(words[:len(words)//2]), 'first_half'),
                          (' '.join(words[len(words)//2:]), 'second_half')]
        
        best_phrase_result = None
        best_score = 0.0
        
        for phrase, phrase_type in phrases[:5]:  # Limit to 5 phrases
            matches = self.scoring_system.find_best_matches(
                phrase, top_n=1,
                expected_tokens=self.expected_tokens,
                expected_context=self.expected_context
            )
            if matches:
                sanskrit, score, breakdown = matches[0]
                if score > best_score:
                    best_score = score
                    best_phrase_result = {
                        'iteration': 2,
                        'chunk': phrase,
                        'sanskrit': sanskrit,
                        'score': score,
                        'breakdown': breakdown,
                        'phrase_type': phrase_type
                    }
        
        if best_phrase_result:
            decision, reason = self.decision_engine.make_decision(
                best_score, previous_score, 2, "phrase"
            )
            best_phrase_result['decision'] = decision
            best_phrase_result['reason'] = reason
            return best_phrase_result
        
        return {
            'iteration': 2,
            'chunk': text,
            'sanskrit': None,
            'score': 0.0,
            'decision': Decision.REJECT,
            'reason': 'No phrase matches found'
        }
    
    def iteration3_verb_object_pairs(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 3: Verb-object pairs with transformation"""
        preprocessed = self.pre_processor.process(text)
        verb_object_pairs = preprocessed['verb_object_pairs']
        
        if not verb_object_pairs:
            # Try to extract pairs from filtered words
            words = preprocessed['filtered']
            if len(words) >= 2:
                verb_object_pairs = [(words[0], words[-1])]
        
        best_pair_result = None
        best_score = 0.0
        
        for verb, obj in verb_object_pairs[:3]:  # Limit to 3 pairs
            # Transform the pair
            transformations = self.transformer.transform_verb_object_pair(verb, obj)
            
            for transformed in transformations:
                matches = self.scoring_system.find_best_matches(
                    transformed, top_n=1,
                    expected_tokens=self.expected_tokens,
                    expected_context=self.expected_context
                )
                if matches:
                    sanskrit, score, breakdown = matches[0]
                    if score > best_score:
                        best_score = score
                        best_pair_result = {
                            'iteration': 3,
                            'chunk': f"{verb} {obj}",
                            'transformed': transformed,
                            'sanskrit': sanskrit,
                            'score': score,
                            'breakdown': breakdown
                        }
        
        if best_pair_result:
            decision, reason = self.decision_engine.make_decision(
                best_score, previous_score, 3, "verb_object"
            )
            best_pair_result['decision'] = decision
            best_pair_result['reason'] = reason
            return best_pair_result
        
        return {
            'iteration': 3,
            'chunk': text,
            'sanskrit': None,
            'score': 0.0,
            'decision': Decision.REJECT,
            'reason': 'No verb-object pair matches found'
        }
    
    def iteration4_individual_words(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 4: Individual words with synonyms"""
        preprocessed = self.pre_processor.process(text)
        words = preprocessed['filtered']
        
        best_word_result = None
        best_score = 0.0
        
        for word in words[:5]:  # Limit to 5 words
            # Try original word
            matches = self.scoring_system.find_best_matches(
                word, top_n=1,
                expected_tokens=self.expected_tokens,
                expected_context=self.expected_context
            )
            
            # Try synonyms
            synonym_phrases = self.transformer.apply_synonyms(word)
            for synonym_phrase in synonym_phrases[:2]:
                synonym_matches = self.scoring_system.find_best_matches(
                    synonym_phrase, top_n=1,
                    expected_tokens=self.expected_tokens,
                    expected_context=self.expected_context
                )
                if synonym_matches:
                    matches.extend(synonym_matches)
            
            if matches:
                # Get best match
                matches.sort(key=lambda x: x[1], reverse=True)
                sanskrit, score, breakdown = matches[0]
                
                if score > best_score:
                    best_score = score
                    best_word_result = {
                        'iteration': 4,
                        'chunk': word,
                        'sanskrit': sanskrit,
                        'score': score,
                        'breakdown': breakdown
                    }
        
        if best_word_result:
            decision, reason = self.decision_engine.make_decision(
                best_score, previous_score, 4, "individual_word"
            )
            best_word_result['decision'] = decision
            best_word_result['reason'] = reason
            return best_word_result
        
        return {
            'iteration': 4,
            'chunk': text,
            'sanskrit': None,
            'score': 0.0,
            'decision': Decision.REJECT,
            'reason': 'No individual word matches found'
        }
    
    def iteration5_final_resolution(self, text: str, previous_score: Optional[float] = None) -> Dict:
        """Iteration 5: Final resolution with Ambiguity_Resolvers and Semantic_Neighbors"""
        # Try all words in dataset with ambiguity resolvers
        best_result = None
        best_score = 0.0
        
        preprocessed = self.pre_processor.process(text)
        text_words = set(preprocessed['filtered'])
        
        for sanskrit, word_data in self.word_data.items():
            # Check ambiguity resolvers
            resolvers = word_data.get('ambiguity_resolvers', '').strip()
            if resolvers:
                resolver_words = set()
                for resolver in resolvers.split('|'):
                    resolver = resolver.strip().lower()
                    if resolver:
                        resolver_words.add(resolver)
                
                # Calculate overlap
                overlap = len(text_words & resolver_words)
                if overlap > 0:
                    # Calculate score
                    score, breakdown = self.scoring_system.calculate_score(text, sanskrit)
                    # Boost score based on resolver overlap
                    score = min(score + (overlap * 0.1), 1.0)
                    
                    if score > best_score:
                        best_score = score
                        best_result = {
                            'iteration': 5,
                            'chunk': text,
                            'sanskrit': sanskrit,
                            'score': score,
                            'breakdown': breakdown,
                            'resolver_match': True
                        }
        
        # If no resolver match, try semantic neighbors of previous matches
        if not best_result or best_score < 0.50:
            # Get all matches and check their neighbors
            all_matches = self.scoring_system.find_best_matches(
                text, top_n=10,
                expected_tokens=self.expected_tokens,
                expected_context=self.expected_context
            )
            for sanskrit, score, breakdown in all_matches:
                word_data = self.word_data.get(sanskrit)
                if word_data:
                    neighbors = word_data.get('semantic_neighbors', '').strip()
                    if neighbors:
                        # Try neighbors
                        for neighbor in neighbors.split('|')[:3]:  # Limit to 3 neighbors
                            neighbor = neighbor.strip()
                            if neighbor in self.word_data:
                                neighbor_score, neighbor_breakdown = self.scoring_system.calculate_score(text, neighbor)
                                if neighbor_score > best_score:
                                    best_score = neighbor_score
                                    best_result = {
                                        'iteration': 5,
                                        'chunk': text,
                                        'sanskrit': neighbor,
                                        'score': neighbor_score,
                                        'breakdown': neighbor_breakdown,
                                        'via_neighbor': sanskrit
                                    }
        
        # Force best available match if still no result
        if not best_result:
            all_matches = self.scoring_system.find_best_matches(
                text, top_n=1,
                expected_tokens=self.expected_tokens,
                expected_context=self.expected_context
            )
            if all_matches:
                sanskrit, score, breakdown = all_matches[0]
                best_result = {
                    'iteration': 5,
                    'chunk': text,
                    'sanskrit': sanskrit,
                    'score': score,
                    'breakdown': breakdown,
                    'forced': True
                }
        
        if best_result:
            decision, reason = self.decision_engine.make_decision(
                best_result['score'], previous_score, 5, "final_resolution"
            )
            best_result['decision'] = decision
            best_result['reason'] = reason
            return best_result
        
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
        Process full text through recursive engine word-by-word
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
        
        # Stop words to keep as-is (not tokenized)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'do', 'does', 'did',
                     'we', 'need', 'how', 'into', 'have', 'has', 'had', 'will', 'would', 'could', 'should'}
        
        # Process word-by-word maintaining order
        output_parts = []
        word_results = []
        total_confidence = 0.0
        matched_count = 0
        i = 0
        
        while i < len(original_words):
            word = original_words[i]
            word_clean = word.lower().strip('.,!?;:()[]{}')
            
            # Keep stop words as-is
            if word_clean in stop_words:
                output_parts.append(word)
                i += 1
                continue
            
            # Try 2-word phrase first (if not at end and next word is not stop word)
            phrase_matched = False
            if i < len(original_words) - 1:
                next_word = original_words[i + 1]
                next_word_clean = next_word.lower().strip('.,!?;:()[]{}')
                
                if next_word_clean not in stop_words:
                    phrase = f"{word_clean} {next_word_clean}"
                    phrase_result = self.process_chunk(phrase)
                    
                    if phrase_result.get('sanskrit') and phrase_result.get('score', 0.0) >= 0.60:
                        # Good phrase match
                        output_parts.append(phrase_result.get('sanskrit'))
                        word_results.append(phrase_result)
                        total_confidence += phrase_result.get('score', 0.0)
                        matched_count += 2
                        i += 2  # Skip both words
                        phrase_matched = True
            
            if not phrase_matched:
                # Try single word match
                word_result = self.process_chunk(word_clean)
                
                if word_result.get('sanskrit') and word_result.get('score', 0.0) >= 0.60:
                    # Good match found
                    output_parts.append(word_result.get('sanskrit'))
                    word_results.append(word_result)
                    total_confidence += word_result.get('score', 0.0)
                    matched_count += 1
                else:
                    # No good match - keep original English word
                    output_parts.append(word)
                
                i += 1
        
        # Build final output
        sanskrit_output = ' '.join(output_parts)
        
        # Calculate average confidence
        avg_confidence = total_confidence / matched_count if matched_count > 0 else 0.0
        
        # Create summary result
        summary_result = {
            'iteration': 'word-by-word',
            'chunk': text,
            'sanskrit': sanskrit_output,
            'score': avg_confidence,
            'breakdown': {},
            'decision': Decision.ACCEPT if matched_count > 0 else Decision.REJECT,
            'reason': f'Processed {matched_count} words/phrases, {len(original_words) - matched_count} kept in English'
        }
        
        return {
            'original_text': text,
            'preprocessed': preprocessed,
            'final_result': summary_result,
            'sanskrit_output': sanskrit_output,
            'confidence': avg_confidence,
            'word_results': word_results,
            'matched_count': matched_count,
            'total_words': len(original_words)
        }

def main():
    """Test recursive engine"""
    print("=" * 80)
    print("Recursive Engine - Testing")
    print("=" * 80)
    
    engine = RecursiveEngine()
    
    test_text = "How to divide a cake into portions"
    print(f"\nInput: '{test_text}'")
    
    result = engine.process_text(test_text)
    
    print(f"\nOutput: '{result['sanskrit_output']}'")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"\nFinal Result:")
    final = result['final_result']
    print(f"  Sanskrit: {final.get('sanskrit', 'N/A')}")
    print(f"  Score: {final.get('score', 0.0):.2%}")
    print(f"  Decision: {final.get('decision', 'N/A')}")
    print(f"  Iteration: {final.get('iteration', 'N/A')}")

if __name__ == "__main__":
    main()

