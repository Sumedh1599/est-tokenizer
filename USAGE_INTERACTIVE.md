# 🧪 Interactive Test Script Usage

## **Quick Start**

Run the interactive test script:

```bash
cd est-tokenizer
python3 test_interactive.py
```

Or if installed as package:

```bash
python3 -m est.test_interactive
```

## **How It Works**

1. **Enter English Text**: Type any English sentence
2. **See Sanskrit Output**: The tokenizer converts it to Sanskrit
3. **View Details**: See confidence scores, processing time, and breakdown
4. **Decode Option**: Choose to decode Sanskrit back to English
5. **Compare Results**: See original → encoded → decoded comparison

## **Example Session**

```
================================================================================
  🕉️  EST TOKENIZER - INTERACTIVE TEST
================================================================================

Enter English text to tokenize: divide property

================================================================================
  ENCODING: English → Sanskrit
================================================================================

📝 Input: divide property

🔄 Processing...

✅ Sanskrit Output: saMpraBinna
📊 Confidence: 100.00%
⏱️  Processing Time: 8696.45ms
🔄 Iteration Used: 1
📋 Decision: Decision.ACCEPT

📈 Score Breakdown:
   • Semantic Frame: 0.75
   • Contextual Triggers: 0.79
   • Conceptual Anchors: 0.60
   • Frequency Index: 1.00

================================================================================
Decode back to English? (yes/y or no/n): yes

================================================================================
  DECODING: Sanskrit → English
================================================================================

📝 Sanskrit Input: saMpraBinna

🔄 Decoding...

✅ English Output: Split open
📊 Decode Confidence: 100.0%
📊 Words Decoded: 1/1

📋 Word-by-Word Translation:
   ✅ saMpraBinna → Split open

================================================================================
📊 COMPARISON:
   Original:  divide property
   Encoded:   saMpraBinna
   Decoded:   Split open
```

## **Commands**

- **Enter text**: Type any English sentence
- **Decode**: Type `yes`, `y`, or press Enter to decode
- **Skip decode**: Type `no` or `n`
- **Exit**: Type `quit`, `exit`, or `q`

## **Features**

✅ Real-time tokenization
✅ Confidence scoring
✅ Detailed breakdown
✅ Optional decoding
✅ Word-by-word translation
✅ Comparison view
✅ Error handling

## **Tips**

- First run may be slower (dataset loading)
- Subsequent operations are faster
- Unknown words are marked in decode output
- High confidence (80%+) indicates good matches

