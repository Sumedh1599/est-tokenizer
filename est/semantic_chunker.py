#!/usr/bin/env python3
"""
Semantic Chunker - Groups words by semantic relationships (subject-verb-object)
Breaks and rearranges sentences to preserve context through semantic roles
"""

import re
from typing import List, Dict, Tuple, Optional

class SemanticChunker:
    def __init__(self):
        """Initialize semantic chunker"""
        # Common verbs
        self.verbs = {
            'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'having',
            'do', 'does', 'did', 'doing',
            'make', 'makes', 'made', 'making',
            'get', 'gets', 'got', 'getting',
            'go', 'goes', 'went', 'going',
            'come', 'comes', 'came', 'coming',
            'see', 'sees', 'saw', 'seeing',
            'know', 'knows', 'knew', 'knowing',
            'think', 'thinks', 'thought', 'thinking',
            'take', 'takes', 'took', 'taking',
            'give', 'gives', 'gave', 'giving',
            'say', 'says', 'said', 'saying',
            'find', 'finds', 'found', 'finding',
            'use', 'uses', 'used', 'using',
            'work', 'works', 'worked', 'working',
            'call', 'calls', 'called', 'calling',
            'try', 'tries', 'tried', 'trying',
            'ask', 'asks', 'asked', 'asking',
            'need', 'needs', 'needed', 'needing',
            'want', 'wants', 'wanted', 'wanting',
            'look', 'looks', 'looked', 'looking',
            'process', 'processes', 'processed', 'processing',
            'identify', 'identifies', 'identified', 'identifying',
            'distribute', 'distributes', 'distributed', 'distributing',
            'govern', 'governs', 'governed', 'governing',
            'transform', 'transforms', 'transformed', 'transforming',
            'interact', 'interacts', 'interacted', 'interacting',
            'learn', 'learns', 'learned', 'learning',
            'improve', 'improves', 'improved', 'improving',
            'understand', 'understands', 'understood', 'understanding',
            'generate', 'generates', 'generated', 'generating',
            'develop', 'develops', 'developed', 'developing',
            'solve', 'solves', 'solved', 'solving',
            'calculate', 'calculates', 'calculated', 'calculating',
            'apply', 'applies', 'applied', 'applying',
            'establish', 'establishes', 'established', 'establishing',
            'interpret', 'interprets', 'interpreted', 'interpreting',
            'represent', 'represents', 'represented', 'representing',
            'consider', 'considers', 'considered', 'considering',
            'ensure', 'ensures', 'ensured', 'ensuring',
            'determine', 'determines', 'determined', 'determining',
            'facilitate', 'facilitates', 'facilitated', 'facilitating',
            'implement', 'implements', 'implemented', 'implementing',
            'provide', 'provides', 'provided', 'providing',
            'depend', 'depends', 'depended', 'depending',
            'allow', 'allows', 'allowed', 'allowing',
            'formulate', 'formulates', 'formulated', 'formulating',
            'design', 'designs', 'designed', 'designing',
            'enable', 'enables', 'enabled', 'enabling',
            'require', 'requires', 'required', 'requiring',
            'support', 'supports', 'supported', 'supporting',
            'address', 'addresses', 'addressed', 'addressing',
            'explore', 'explores', 'explored', 'exploring',
            'integrate', 'integrates', 'integrated', 'integrating',
            'increase', 'increases', 'increased', 'increasing',
            'expect', 'expects', 'expected', 'expecting',
            'expand', 'expands', 'expanded', 'expanding'
        }
        
        # Subject indicators (words that often indicate subjects)
        self.subject_indicators = {
            'the', 'a', 'an', 'this', 'that', 'these', 'those',
            'some', 'many', 'most', 'all', 'each', 'every'
        }
        
        # Object indicators
        self.object_indicators = {
            'to', 'for', 'with', 'by', 'from', 'into', 'onto', 'upon'
        }
    
    def is_verb(self, word: str) -> bool:
        """Check if word is a verb"""
        word_lower = word.lower().strip('.,!?;:()[]{}')
        return word_lower in self.verbs
    
    def extract_svo_chunks(self, text: str) -> List[Dict]:
        """
        Extract Subject-Verb-Object chunks from text
        Returns list of chunks with their semantic roles
        """
        words = text.split()
        chunks = []
        i = 0
        
        while i < len(words):
            # Look for verb
            verb_idx = None
            verb = None
            
            # Find next verb
            for j in range(i, min(i + 10, len(words))):
                if self.is_verb(words[j]):
                    verb_idx = j
                    verb = words[j]
                    break
            
            if verb_idx is None:
                # No verb found, treat remaining as object/noun phrase
                if i < len(words):
                    chunk = {
                        'type': 'noun_phrase',
                        'words': words[i:],
                        'start_idx': i,
                        'end_idx': len(words)
                    }
                    chunks.append(chunk)
                break
            
            # Extract subject (words before verb)
            subject_words = words[i:verb_idx] if verb_idx > i else []
            subject = ' '.join(subject_words) if subject_words else None
            
            # Extract verb
            verb_start = verb_idx
            verb_end = verb_idx + 1
            
            # Extract object (words after verb, up to next verb or end)
            object_start = verb_end
            object_end = verb_end
            for j in range(verb_end, min(verb_end + 8, len(words))):
                if self.is_verb(words[j]):
                    break
                object_end = j + 1
            
            object_words = words[object_start:object_end] if object_end > object_start else []
            obj = ' '.join(object_words) if object_words else None
            
            # Create SVO chunk
            chunk = {
                'type': 'svo',
                'subject': subject,
                'verb': verb,
                'object': obj,
                'words': words[i:object_end] if object_end > i else words[i:verb_end],
                'start_idx': i,
                'end_idx': object_end if object_end > verb_end else verb_end
            }
            chunks.append(chunk)
            
            i = object_end if object_end > verb_end else verb_end
        
        return chunks
    
    def group_semantic_units(self, text: str) -> List[Dict]:
        """
        Group words into semantic units based on relationships
        Breaks and rearranges to preserve context
        """
        # First, extract SVO chunks
        svo_chunks = self.extract_svo_chunks(text)
        
        semantic_units = []
        
        for chunk in svo_chunks:
            if chunk['type'] == 'svo':
                # Create semantic units for subject, verb, object
                if chunk['subject']:
                    semantic_units.append({
                        'type': 'subject',
                        'text': chunk['subject'],
                        'words': chunk['subject'].split(),
                        'original_indices': list(range(chunk['start_idx'], chunk['start_idx'] + len(chunk['subject'].split())))
                    })
                
                if chunk['verb']:
                    semantic_units.append({
                        'type': 'verb',
                        'text': chunk['verb'],
                        'words': [chunk['verb']],
                        'original_indices': [chunk['start_idx'] + (len(chunk['subject'].split()) if chunk['subject'] else 0)]
                    })
                
                if chunk['object']:
                    semantic_units.append({
                        'type': 'object',
                        'text': chunk['object'],
                        'words': chunk['object'].split(),
                        'original_indices': list(range(chunk['start_idx'] + (len(chunk['subject'].split()) if chunk['subject'] else 0) + 1, chunk['end_idx']))
                    })
            else:
                # Noun phrase
                semantic_units.append({
                    'type': 'noun_phrase',
                    'text': ' '.join(chunk['words']),
                    'words': chunk['words'],
                    'original_indices': list(range(chunk['start_idx'], chunk['end_idx']))
                })
        
        return semantic_units
    
    def create_semantic_phrases(self, text: str) -> List[str]:
        """
        Create semantic phrases by grouping related concepts
        Returns list of phrases that preserve subject-verb-object relationships
        """
        units = self.group_semantic_units(text)
        phrases = []
        
        i = 0
        while i < len(units):
            # Try to group subject-verb-object together
            if i < len(units) - 2:
                subject_unit = units[i] if units[i]['type'] == 'subject' else None
                verb_unit = units[i + 1] if i + 1 < len(units) and units[i + 1]['type'] == 'verb' else None
                object_unit = units[i + 2] if i + 2 < len(units) and units[i + 2]['type'] == 'object' else None
                
                if subject_unit and verb_unit and object_unit:
                    # Create SVO phrase
                    svo_phrase = f"{subject_unit['text']} {verb_unit['text']} {object_unit['text']}"
                    phrases.append(svo_phrase)
                    i += 3
                    continue
            
            # Try subject-verb
            if i < len(units) - 1:
                subject_unit = units[i] if units[i]['type'] == 'subject' else None
                verb_unit = units[i + 1] if units[i + 1]['type'] == 'verb' else None
                
                if subject_unit and verb_unit:
                    sv_phrase = f"{subject_unit['text']} {verb_unit['text']}"
                    phrases.append(sv_phrase)
                    i += 2
                    continue
            
            # Try verb-object
            if i < len(units) - 1:
                verb_unit = units[i] if units[i]['type'] == 'verb' else None
                object_unit = units[i + 1] if units[i + 1]['type'] == 'object' else None
                
                if verb_unit and object_unit:
                    vo_phrase = f"{verb_unit['text']} {object_unit['text']}"
                    phrases.append(vo_phrase)
                    i += 2
                    continue
            
            # Single unit
            phrases.append(units[i]['text'])
            i += 1
        
        return phrases

def main():
    """Test semantic chunker"""
    chunker = SemanticChunker()
    
    test_texts = [
        "Machine learning algorithms process large amounts of data",
        "Property inheritance laws govern how assets are distributed",
        "The quick brown fox jumps over the lazy dog"
    ]
    
    for text in test_texts:
        print(f"Text: {text}")
        print()
        
        chunks = chunker.extract_svo_chunks(text)
        print("SVO Chunks:")
        for chunk in chunks:
            if chunk['type'] == 'svo':
                print(f"  Subject: {chunk.get('subject', 'None')}")
                print(f"  Verb: {chunk.get('verb', 'None')}")
                print(f"  Object: {chunk.get('object', 'None')}")
            else:
                print(f"  Noun phrase: {chunk.get('words', [])}")
        print()
        
        phrases = chunker.create_semantic_phrases(text)
        print(f"Semantic Phrases: {phrases}")
        print()
        print("-" * 80)
        print()

if __name__ == "__main__":
    main()

