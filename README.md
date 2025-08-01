# Adobe Hackathon Round 1A - PDF Outline Extraction

## Challenge Theme: Connecting the Dots Through Docs

### Mission
Extract structured outlines from PDF documents to identify hierarchical headings (Title, H1, H2, H3) with their corresponding page numbers, creating the foundation for intelligent document experiences.

## Features
- **Fast Processing**: Handles 50-page PDFs in under 10 seconds
- **Intelligent Heading Detection**: Multi-layered approach using font analysis, text patterns, and semantic validation
- **Hierarchical Structure**: Accurately determines H1/H2/H3 levels based on relative font sizes
- **Domain Agnostic**: Works across research papers, financial reports, technical documentation
- **Robust**: Handles various document formats and styling approaches

## Architecture & Approach

### Core Methodology
1. **PDF Parsing**: PyMuPDF for robust document parsing and font extraction
2. **Statistical Analysis**: Calculate document-wide font statistics for relative sizing
3. **Multi-Pattern Detection**: 11+ heading patterns covering:
   - Numbered sections (1., 1.1, 1.1.1)
   - All caps headings (INTRODUCTION)
   - Chapter/Section markers
   - Roman numerals (I, II, III)
   - Letter indexing (A., B., C.)
4. **Semantic Validation**: Keyword matching against academic/business terminology
5. **Hierarchy Assignment**: Font size thresholds for H1/H2/H3 classification

### Key Innovations
- **Adaptive Font Thresholds**: Uses document-specific font size distributions
- **Bold Text Detection**: Font flags analysis for emphasis detection
- **Pattern Redundancy**: Multiple pattern matching for comprehensive coverage
- **Edge Case Handling**: Fallback mechanisms for non-standard documents

## Input/Output Specification

### Input
- PDF files in `/app/input` directory
- Supports up to 50 pages per document
- No network access required (offline processing)

### Output Format (Challenge Compliant)
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## Docker Execution

### Build (AMD64 Compatible)
```bash
docker build --platform linux/amd64 -t round1a:latest .
```

### Run (Challenge Format)
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  round1a:latest
```

### Expected Behavior
- Processes all PDFs in `/app/input`
- Generates `filename.json` for each `filename.pdf`
- Completes within 10 seconds per 50-page document

## Performance Guarantees
- ✅ **Speed**: ≤10 seconds for 50-page PDFs
- ✅ **Size**: <200MB total (no ML models)
- ✅ **Architecture**: AMD64/x86_64 compatible
- ✅ **Offline**: No internet connectivity required
- ✅ **Resource**: CPU-only (8 CPUs, 16GB RAM)

## Scoring Alignment
- **Heading Detection Accuracy**: High precision/recall through multi-pattern approach
- **Performance**: Optimized for speed and size constraints
- **Multilingual Support**: Unicode-aware text processing for international documents

## Dependencies
- **PyMuPDF (fitz)**: PDF parsing and font analysis
- **Python Standard Library**: JSON, regex, statistics
- **No ML Dependencies**: Rule-based approach for reliability and speed

## Why This Approach Works
Unlike ML-based solutions, our rule-based system:
- Provides consistent results across document types
- Requires no training data or large models
- Processes documents at blazing speed
- Handles edge cases through pattern redundancy
- Scales to any domain without retraining
