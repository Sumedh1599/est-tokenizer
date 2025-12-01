#!/usr/bin/env python3
"""
EST Decoder - Converts Sanskrit tokens back to English
Provides reverse translation from Sanskrit to English using the dataset
"""

import csv
from typing import List, Dict, Optional
from pathlib import Path

class SanskritDecoder:
    """
    Decoder class for converting Sanskrit tokens back to English.
    
    Example:
        >>> decoder = SanskritDecoder()
        >>> english = decoder.decode("saMpraBinna")
        >>> print(english)
        'divide property'
    """
    
    def __init__(self, csv_path: Optional[str] = None):
        """
        Initialize the Sanskrit decoder.
        
        Args:
            csv_path: Path to Sanskrit dictionary CSV. If None, uses default location.
        """
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
        self.word_data = {}
        self._load_dataset()
    
    def _load_dataset(self):
        """Load Sanskrit word data from CSV"""
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
    
    def decode_word(self, sanskrit_word: str) -> Optional[str]:
        """
        Decode a single Sanskrit word to its English definition.
        
        Args:
            sanskrit_word: Sanskrit word to decode
        
        Returns:
            English definition or None if not found
        """
        word_data = self.word_data.get(sanskrit_word)
        if word_data:
            return word_data.get('english', '')
        return None
    
    def decode(self, sanskrit_text: str, include_unknown: bool = True) -> str:
        """
        Decode Sanskrit text back to English.
        
        Args:
            sanskrit_text: Sanskrit text (space-separated words)
            include_unknown: If True, include unknown words in output; if False, skip them
        
        Returns:
            English translation (space-separated)
        """
        words = sanskrit_text.split()
        english_words = []
        unknown_words = []
        
        for word in words:
            # Remove any punctuation for lookup
            clean_word = word.strip('.,!?;:()[]{}')
            
            english = self.decode_word(clean_word)
            if english:
                # Take first definition if multiple (split by semicolon or comma)
                primary_def = english.split(';')[0].split(',')[0].strip()
                english_words.append(primary_def)
            else:
                if include_unknown:
                    english_words.append(f"[{word}]")  # Mark as unknown
                unknown_words.append(word)
        
        result = ' '.join(english_words)
        
        return result
    
    def decode_with_details(self, sanskrit_text: str) -> Dict:
        """
        Decode Sanskrit text with detailed information.
        
        Args:
            sanskrit_text: Sanskrit text to decode
        
        Returns:
            Dict with:
                - english: English translation
                - words: List of word-by-word translations
                - unknown_words: List of words not found in dataset
                - confidence: Percentage of words successfully decoded
        """
        words = sanskrit_text.split()
        decoded_words = []
        word_details = []
        unknown_words = []
        
        for word in words:
            clean_word = word.strip('.,!?;:()[]{}')
            word_data = self.word_data.get(clean_word)
            
            if word_data:
                english = word_data.get('english', '')
                primary_def = english.split(';')[0].split(',')[0].strip()
                decoded_words.append(primary_def)
                word_details.append({
                    'sanskrit': clean_word,
                    'english': primary_def,
                    'full_definition': english,
                    'found': True
                })
            else:
                decoded_words.append(f"[{word}]")
                unknown_words.append(word)
                word_details.append({
                    'sanskrit': clean_word,
                    'english': None,
                    'found': False
                })
        
        total_words = len(words)
        decoded_count = total_words - len(unknown_words)
        confidence = (decoded_count / total_words * 100) if total_words > 0 else 0.0
        
        return {
            'english': ' '.join(decoded_words),
            'words': word_details,
            'unknown_words': unknown_words,
            'confidence': confidence,
            'decoded_count': decoded_count,
            'total_count': total_words
        }
    
    def decode_batch(self, sanskrit_texts: List[str]) -> List[Dict]:
        """
        Decode multiple Sanskrit texts in batch.
        
        Args:
            sanskrit_texts: List of Sanskrit texts
        
        Returns:
            List of decode results (same format as decode_with_details)
        """
        results = []
        for text in sanskrit_texts:
            result = self.decode_with_details(text)
            result['original'] = text
            results.append(result)
        
        return results
    
    def get_word_info(self, sanskrit_word: str) -> Optional[Dict]:
        """
        Get full information about a Sanskrit word.
        
        Args:
            sanskrit_word: Sanskrit word
        
        Returns:
            Dict with all word data or None if not found
        """
        word_data = self.word_data.get(sanskrit_word)
        if word_data:
            return {
                'sanskrit': sanskrit_word,
                **word_data
            }
        return None

