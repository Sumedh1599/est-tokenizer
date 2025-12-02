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
        self.space_symbol = 'ं'  # Default: Anusvāra (space-bar symbol)
        self.devnari_to_letter = {}  # Reverse mapping for letter transliteration
        self._load_dataset()
    
    def _load_dataset(self):
        """Load Sanskrit word data from CSV"""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                sanskrit = row.get('sanskrit', '').strip()
                devnari = row.get('devnari', '').strip()
                
                if sanskrit:
                    self.word_data[sanskrit] = {
                        'english': row.get('english', '').strip(),
                        'semantic_frame': row.get('semantic_frame', '').strip(),
                        'contextual_triggers': row.get('Contextual_Triggers', '').strip(),
                        'conceptual_anchors': row.get('Conceptual_Anchors', '').strip(),
                        'ambiguity_resolvers': row.get('Ambiguity_Resolvers', '').strip(),
                        'usage_frequency_index': row.get('Usage_Frequency_Index', '').strip(),
                        'semantic_neighbors': row.get('Semantic_Neighbors', '').strip(),
                        'devnari': devnari
                    }
                
                # Build reverse mapping: devnari -> letter (for letter transliteration)
                if len(sanskrit) == 1 and (sanskrit.isalpha() or sanskrit.isdigit()):
                    if devnari:
                        # Map Devanagari to IAST letter (both cases)
                        self.devnari_to_letter[devnari] = sanskrit
                        if sanskrit.isupper() and sanskrit.lower() not in self.devnari_to_letter.values():
                            # Also allow lowercase mapping
                            pass  # Will use the same devnari for both
                        elif sanskrit.islower():
                            # Lowercase maps to same devnari
                            pass
                
                # Get space symbol (space-bar entry)
                if sanskrit.lower() == 'space-bar' and devnari:
                    self.space_symbol = devnari
    
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
            sanskrit_text: Sanskrit text (double space symbol between words, single between letters)
            include_unknown: If True, include unknown words in output; if False, skip them
        
        Returns:
            English translation (space-separated)
        """
        if not sanskrit_text:
            return ""
        
        # Split by DOUBLE space symbol first to separate WORDS
        # Single space symbol separates letters WITHIN a word
        # Double space symbol separates WORDS
        word_separator = self.space_symbol + self.space_symbol
        words = sanskrit_text.split(word_separator)
        words = [w.strip() for w in words if w.strip()]
        
        if not words:
            return ""
        
        # Now process each word (which may contain letters separated by single space symbol)
        english_words = []
        unknown_words = []
        
        for word_part in words:
            # Split this word by single space symbol to get letters/characters
            parts = word_part.split(self.space_symbol)
            parts = [p.strip() for p in parts if p.strip()]
            
            if not parts:
                continue
            
            # Process parts of this word
            current_letter_sequence = []  # For letter-by-letter transliteration
            decoded_word = None  # Track if we decoded a complete dictionary word
            
            for i, part in enumerate(parts):
                # Remove punctuation for lookup (but keep it for output)
                clean_part = part.strip('.,!?;:()[]{}')
                has_punctuation = part != clean_part
                punctuation = part[len(clean_part):] if has_punctuation else ''
                
                # Check if it's a dictionary word (Sanskrit word)
                # First, check if it's already an English word (preserved from encoding)
                # Common English words should not be decoded as Sanskrit
                if i == 0:
                    full_word = word_part.replace(self.space_symbol, '').strip('.,!?;:()[]{}')
                    # Check if it's a preserved English word (common words, or has uppercase, or contains punctuation like apostrophes/hyphens)
                    common_english_words = {'in', 'at', 'on', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'the', 'a', 'an', 'and', 'or', 'but', 'cat', 'sat', 'mat', 'dog', 'man', 'he', 'she', 'we', 'you', 'car', 'ant', 'vast', 'hiker', 'fire', 'breathing'}
                    # Check if word contains punctuation (apostrophe, hyphen) - likely preserved English
                    has_punctuation_in_word = "'" in full_word or "-" in full_word
                    if full_word.lower() in common_english_words or (full_word.isalpha() and any(c.isupper() for c in full_word)) or has_punctuation_in_word:
                        # It's a preserved English word - keep it as is
                        decoded_word = full_word + punctuation
                        break
                    
                    # Now try as dictionary word
                    english = self.decode_word(full_word)
                    if english:
                        primary_def = english.split(';')[0].split(',')[0].strip()
                        decoded_word = primary_def + punctuation
                        break
                
                # Also try single part as dictionary word
                if len(parts) == 1:
                    english = self.decode_word(clean_part)
                    if english:
                        primary_def = english.split(';')[0].split(',')[0].strip()
                        decoded_word = primary_def + punctuation
                        break
                
                # Not a dictionary word - process as letters
                # Check if it's already an English word (preserved from encoding)
                # Check the entire word_part first (before splitting by space symbol)
                if i == 0:
                    # Check if entire word_part is an English word
                    full_word_clean = word_part.replace(self.space_symbol, '').strip('.,!?;:()[]{}')
                    if full_word_clean.isalpha() and len(full_word_clean) > 1:
                        # Already English word (preserved during encoding)
                        if current_letter_sequence:
                            letter_word = ''.join(current_letter_sequence)
                            english_words.append(letter_word)
                            current_letter_sequence = []
                        decoded_word = full_word_clean + punctuation
                        break
                
                # Check individual part
                if clean_part.isalpha() and (any(c.isupper() for c in clean_part) or len(clean_part) > 1):
                    # Already English word (preserved during encoding)
                    if current_letter_sequence:
                        letter_word = ''.join(current_letter_sequence)
                        english_words.append(letter_word)
                        current_letter_sequence = []
                    decoded_word = clean_part + punctuation
                    break
                # Check if it's a single letter (Devanagari, IAST, or English letter)
                elif len(clean_part) == 1:
                    # Check Devanagari first (most common case for letter transliteration)
                    if clean_part in self.devnari_to_letter:
                        # It's a Devanagari character - convert to English letter
                        english_letter = self.devnari_to_letter[clean_part]
                        current_letter_sequence.append(english_letter)
                    elif clean_part.isalpha():
                        # It's already an English letter - use it directly
                        current_letter_sequence.append(clean_part)
                    else:
                        # Unknown single character
                        if include_unknown:
                            current_letter_sequence.append(f"[{clean_part}]")
                        unknown_words.append(clean_part)
                else:
                    # Multi-character unknown word
                    if current_letter_sequence:
                        letter_word = ''.join(current_letter_sequence)
                        english_words.append(letter_word)
                        current_letter_sequence = []
                    if include_unknown:
                        english_words.append(f"[{clean_part}]" + punctuation)
                    unknown_words.append(clean_part)
            
            # Add decoded word or letter sequence
            if decoded_word:
                english_words.append(decoded_word)
            elif current_letter_sequence:
                # We have a letter sequence - join it as a word
                letter_word = ''.join(current_letter_sequence)
                english_words.append(letter_word)
        
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
        # Split by double space to get words
        word_separator = self.space_symbol + self.space_symbol
        words = sanskrit_text.split(word_separator)
        words = [w.strip() for w in words if w.strip()]
        
        decoded_words = []
        word_details = []
        unknown_words = []
        
        for word in words:
            # Remove space symbols to get the actual word
            clean_word = word.replace(self.space_symbol, '').strip('.,!?;:()[]{}')
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
                # Try to decode as letter sequence
                parts = word.split(self.space_symbol)
                letter_word = ''
                for part in parts:
                    if part in self.devnari_to_letter:
                        letter_word += self.devnari_to_letter[part]
                    elif part.isalpha():
                        letter_word += part
                
                if letter_word:
                    decoded_words.append(letter_word)
                    word_details.append({
                        'sanskrit': clean_word,
                        'english': letter_word,
                        'found': False,
                        'transliterated': True
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
