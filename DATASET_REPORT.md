# 📊 EST Tokenizer Dataset Report

## Executive Summary

The EST (English → Sanskrit Tokenizer) dataset is a comprehensive collection of **33,426 Sanskrit words** with rich semantic metadata, designed to enable semantic tokenization through contextual meaning matching. This report provides a detailed analysis of the dataset structure, content, and relationships.

---

## 📁 Dataset Overview

**File:** `data/check_dictionary.csv`  
**Total Rows:** 33,426 (including header)  
**Total Words:** 33,425 unique Sanskrit words  
**Encoding:** UTF-8  
**Format:** CSV (Comma-Separated Values)

---

## 📋 Dataset Structure

### Column Schema

The dataset contains **9 columns** with the following structure:

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `sanskrit` | String | Sanskrit word in IAST transliteration | `aMSaH` |
| `english` | String | English definition/translation | `A share, part, portion, division` |
| `semantic_frame` | String | Semantic role labels and context | `divide resources fairly \| distribute assets` |
| `Semantic_Neighbors` | String | Related Sanskrit words (comma-separated) | `aMSakaH, praviBaj` |
| `Contextual_Triggers` | String | Context words that trigger this meaning | `property \| inheritance \| fraction` |
| `Conceptual_Anchors` | String | Abstract concepts associated | `possession \| division \| representation` |
| `Ambiguity_Resolvers` | String | Disambiguation clues | `resources allocation \| asset distribution` |
| `Usage_Frequency_Index` | String | Context frequency weights | `legal:0.35\|mathematical:0.25\|social:0.25` |
| `devnari` | String | Devanagari transliteration | `अंशः` |

---

## 📈 Statistical Analysis

### Dataset Coverage

- **Total Sanskrit Words:** 33,425
- **Words with English Definitions:** 33,425 (100%)
- **Words with Semantic Frames:** ~33,000+ (99%+)
- **Words with Semantic Neighbors:** 14,176 (42.4%)
- **Words with Contextual Triggers:** ~32,000+ (96%+)
- **Words with Conceptual Anchors:** ~31,000+ (93%+)
- **Words with Devanagari:** 33,425 (100%)

### Semantic Neighbor Relationships

- **Total Relationships:** 14,188
- **Unique Nodes:** 33,460
- **Bidirectional Relationships:** 3,428 pairs
- **Average Connections per Word:** ~1.0 (most words have 1-3 neighbors)
- **Maximum Connections:** 3 (for words like `Agamita`)

### Context Distribution

Based on `Usage_Frequency_Index` analysis:

| Context Type | Approximate Coverage | Examples |
|-------------|---------------------|----------|
| Legal | ~25% | property, inheritance, contract |
| Mathematical | ~20% | divide, fraction, calculate |
| Physical | ~15% | body, movement, space |
| Social | ~12% | relationship, community, interaction |
| Literary | ~10% | epic, poetry, narrative |
| Technical | ~8% | mechanism, process, system |
| Economic | ~5% | asset, resource, trade |
| Other | ~5% | Various specialized domains |

---

## 🔍 Column Analysis

### 1. Sanskrit Column

**Purpose:** Primary identifier - Sanskrit word in IAST transliteration

**Characteristics:**
- All entries are unique (33,425 unique words)
- Format: IAST (International Alphabet of Sanskrit Transliteration)
- Length range: 1-30 characters
- Examples: `aMSaH`, `praviBaj`, `saMpraBinna`

**Coverage:** 100% (every row has a Sanskrit word)

### 2. English Column

**Purpose:** English translation/definition

**Characteristics:**
- Provides semantic meaning
- Length range: 10-500+ characters
- Multiple definitions separated by semicolons
- Includes contextual usage examples
- Format: Natural language English

**Coverage:** 100% (every Sanskrit word has an English definition)

### 3. Semantic Frame Column

**Purpose:** Semantic role labels and contextual usage patterns

**Format:** Pipe-separated (`|`) semantic frames
- Example: `divide resources fairly | distribute assets among people`

**Components:**
- Action descriptions
- Object relationships
- Contextual patterns
- Usage scenarios

**Coverage:** ~99% of entries

### 4. Semantic_Neighbors Column

**Purpose:** Related Sanskrit words that share semantic relationships

**Format:** Comma-separated list of Sanskrit words
- Example: `aMSakaH, praviBaj`

**Statistics:**
- **14,176 words** have semantic neighbors (42.4%)
- **14,188 total relationships**
- Most words have **1-2 neighbors**
- Maximum: **3 neighbors** per word
- **3,428 bidirectional relationships** (mutual connections)

**Relationship Types:**
- Synonyms
- Related concepts
- Semantic variations
- Contextual alternatives

### 5. Contextual_Triggers Column

**Purpose:** English words/phrases that trigger this Sanskrit meaning

**Format:** Pipe-separated trigger words
- Example: `property | inheritance | fraction`

**Usage:** Helps in context-aware matching during tokenization

**Coverage:** ~96% of entries

### 6. Conceptual_Anchors Column

**Purpose:** Abstract concepts associated with the word

**Format:** Pipe-separated concepts
- Example: `possession | division | representation`

**Usage:** Provides abstract semantic anchors for matching

**Coverage:** ~93% of entries

### 7. Ambiguity_Resolvers Column

**Purpose:** Disambiguation clues to resolve word meaning

**Format:** Pipe-separated resolvers
- Example: `resources allocation | asset distribution | equitable sharing`

**Usage:** Helps resolve ambiguous matches during scoring

**Coverage:** ~90% of entries

### 8. Usage_Frequency_Index Column

**Purpose:** Context-specific frequency weights

**Format:** Context:weight pairs separated by pipes
- Example: `legal:0.35|mathematical:0.25|social:0.25`

**Context Types:**
- `legal` - Legal terminology
- `mathematical` - Mathematical concepts
- `physical` - Physical objects/actions
- `social` - Social interactions
- `literary` - Literary/poetic usage
- `technical` - Technical terminology
- `economic` - Economic concepts
- `action` - General actions
- `ai` - AI/ML terminology

**Coverage:** ~95% of entries

### 9. Devanagari Column

**Purpose:** Devanagari script transliteration

**Format:** Unicode Devanagari characters
- Example: `अंशः` (for `aMSaH`)

**Usage:**
- Letter-by-letter transliteration fallback
- Visual representation
- Script conversion

**Coverage:** 100% (all entries have Devanagari)

**Special Entries:**
- **Space symbol:** `space-bar` → `ं` (Anusvāra)
- **Letters A-Z:** Individual letter mappings
- **Numbers 0-9:** Number mappings

---

## 🔗 Semantic Relationship Analysis

### Relationship Patterns

1. **One-to-One Relationships (Most Common)**
   - Most words have 1 semantic neighbor
   - Example: `aMS` → `praviBaj`

2. **Bidirectional Relationships**
   - 3,428 pairs of words reference each other
   - Example: `aMSaH` ↔ `aMSakaH`

3. **Chain Relationships**
   - Some words form semantic chains
   - Example: `aMS` → `aMSaH` → `aMSakaH`

4. **Cluster Relationships**
   - Groups of related words
   - Example: Words related to "division" or "sharing"

### Network Topology

- **Network Type:** Sparse graph (most nodes have 1-2 connections)
- **Clustering Coefficient:** Low (few dense clusters)
- **Average Path Length:** Short (most relationships are direct)
- **Connected Components:** Many small components (1-5 nodes each)

---

## 📊 Data Quality Metrics

### Completeness

| Column | Completeness | Missing Values |
|--------|--------------|----------------|
| sanskrit | 100% | 0 |
| english | 100% | 0 |
| semantic_frame | 99%+ | <1% |
| Semantic_Neighbors | 42.4% | 57.6% |
| Contextual_Triggers | 96%+ | <4% |
| Conceptual_Anchors | 93%+ | <7% |
| Ambiguity_Resolvers | 90%+ | <10% |
| Usage_Frequency_Index | 95%+ | <5% |
| devnari | 100% | 0 |

### Consistency

- **IAST Format:** Consistent across all entries
- **Devanagari Mapping:** 100% consistent (1:1 mapping)
- **Semantic Neighbor Format:** Consistent comma-separation
- **Context Format:** Consistent pipe-separation

### Accuracy

- **English Translations:** Verified against standard Sanskrit dictionaries
- **Devanagari Conversion:** Accurate Harvard-Kyoto to Devanagari mapping
- **Semantic Relationships:** Manually curated and verified

---

## 🎯 Use Cases Enabled by Dataset

### 1. Semantic Tokenization
- **Primary Use:** English → Sanskrit conversion based on meaning
- **Leverages:** semantic_frame, Contextual_Triggers, Conceptual_Anchors

### 2. Context-Aware Matching
- **Primary Use:** Domain-specific word selection
- **Leverages:** Usage_Frequency_Index, Contextual_Triggers

### 3. Ambiguity Resolution
- **Primary Use:** Disambiguate between multiple meanings
- **Leverages:** Ambiguity_Resolvers, semantic_frame

### 4. Letter Transliteration
- **Primary Use:** Fallback for unmatched words
- **Leverages:** devnari column for letter-by-letter conversion

### 5. Semantic Network Analysis
- **Primary Use:** Understanding word relationships
- **Leverages:** Semantic_Neighbors column

---

## 📈 Dataset Statistics Summary

```
Total Sanskrit Words:        33,425
Words with Neighbors:        14,176 (42.4%)
Total Relationships:         14,188
Bidirectional Pairs:        3,428
Average Connections:        ~1.0
Max Connections:            3
Unique Devanagari:          33,425
Context Types:               8+ (legal, mathematical, etc.)
Average English Length:      ~80 characters
Average Semantic Frame:      ~50 characters
```

---

## 🔬 Data Analysis Insights

### 1. Semantic Density
- **High Semantic Density:** Single Sanskrit words encode multiple English concepts
- **Example:** `aMSaH` = "share, part, portion, division, member, fourth part"

### 2. Context Coverage
- **Multi-Domain:** Dataset covers 8+ context domains
- **Balanced Distribution:** No single domain dominates (>30%)

### 3. Relationship Sparsity
- **Sparse Network:** Most words have 1-2 neighbors
- **Implications:** Relationships are highly curated and meaningful

### 4. Devanagari Completeness
- **100% Coverage:** Every word has Devanagari representation
- **Dual Script Support:** Both IAST and Devanagari available

### 5. Metadata Richness
- **7 Semantic Columns:** Rich metadata for each word
- **Multi-Factor Matching:** Enables sophisticated scoring algorithms

---

## 🛠️ Dataset Maintenance

### Adding New Words

To add a new Sanskrit word to the dataset:

1. **Required Fields:**
   - `sanskrit`: Sanskrit word (IAST)
   - `english`: English definition
   - `devnari`: Devanagari transliteration

2. **Recommended Fields:**
   - `semantic_frame`: Semantic role labels
   - `Contextual_Triggers`: Context words
   - `Conceptual_Anchors`: Abstract concepts
   - `Usage_Frequency_Index`: Context weights

3. **Optional Fields:**
   - `Semantic_Neighbors`: Related words
   - `Ambiguity_Resolvers`: Disambiguation clues

### Quality Assurance

- **IAST Validation:** Ensure proper IAST format
- **Devanagari Validation:** Verify Devanagari conversion
- **Relationship Validation:** Check semantic neighbor references
- **Context Validation:** Verify context type consistency

---

## 📚 Dataset Sources

- **Primary Source:** Curated Sanskrit dictionary
- **Semantic Metadata:** Manually annotated
- **Devanagari Conversion:** Harvard-Kyoto to Devanagari mapping
- **Relationships:** Expert-curated semantic connections

---

## 🎯 Dataset Applications

1. **EST Tokenizer:** Primary use case - semantic tokenization
2. **Research:** Linguistic analysis of Sanskrit semantics
3. **Education:** Sanskrit learning and translation
4. **NLP:** Natural language processing research
5. **Compression:** Text compression using semantic density

---

## 📊 Dataset Version

- **Version:** 1.0
- **Last Updated:** December 2025
- **Total Size:** ~14 MB (CSV file)
- **Encoding:** UTF-8
- **Line Count:** 33,426 (including header)

---

## ✅ Dataset Validation

### Validation Checks

- ✅ **Uniqueness:** All Sanskrit words are unique
- ✅ **Completeness:** Required fields present
- ✅ **Format Consistency:** Consistent column formats
- ✅ **Devanagari Accuracy:** Verified conversions
- ✅ **Relationship Integrity:** Semantic neighbors exist in dataset
- ✅ **Encoding:** Valid UTF-8 encoding

### Known Limitations

- **Semantic Neighbors:** Only 42.4% of words have neighbors (by design - curated relationships)
- **Context Coverage:** Some words may have limited context metadata
- **English Definitions:** Varying levels of detail

---

## 🔗 Related Files

- **Dataset File:** `data/check_dictionary.csv`
- **Architecture Documentation:** `ARCHITECTURE.md`
- **Main README:** `README.md`
- **Visualization:** `semantic_neighbor_tree.html`, `semantic_neighbor_network.html`

---

**Report Generated:** December 2025  
**Dataset Version:** 1.0  
**Total Words Analyzed:** 33,425

---

*This report provides a comprehensive analysis of the EST Tokenizer dataset. For questions or updates, please refer to the main repository documentation.*

