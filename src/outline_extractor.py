"""
Round 1A: PDF Outline Extraction
Structured outline extraction with hierarchical headings and page numbers
"""

import fitz  # PyMuPDF
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import statistics

class OutlineExtractor:
    """PDF outline extractor for Round 1A challenges"""

    def __init__(self):
        # Enhanced heading patterns for better detection
        self.heading_patterns = [
            r'^\d+\.?\s+[A-Z]',  # Numbered headings like "1. Introduction", "1.1 Overview"
            r'^[A-Z][A-Z\s&:]+$',  # All caps headings like "INTRODUCTION", "RESULTS & DISCUSSION"
            r'^Chapter\s+\d+[:\-\s]*[A-Za-z\s]*$',  # Chapter headings
            r'^Section\s+\d+[:\-\s]*[A-Za-z\s]*$',  # Section headings
            r'^Appendix\s+[A-Z\d]+[:\-\s]*[A-Za-z\s]*$',  # Appendix headings
            r'^\d+\.\d+\.?\s+[A-Za-z]',  # Sub-numbered headings like "1.1. Methods"
            r'^\d+\.\d+\.\d+\.?\s+[A-Za-z]',  # Sub-sub-numbered headings like "1.1.1. Analysis"
            r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*$',  # Title case headings like "Introduction", "Data Analysis"
            r'^[A-Z][a-z]+\s+\d+[:\-\s]*[A-Za-z\s]*$',  # Pattern like "Part 1: Overview"
            r'^\([IVX]+\)\s+[A-Za-z]',  # Roman numeral headings like "(I) Introduction"
            r'^[A-Z]\.\s+[A-Za-z]',  # Letter headings like "A. Methods"
        ]
        
        # Common academic/document heading keywords for validation
        self.heading_keywords = [
            'introduction', 'abstract', 'summary', 'conclusion', 'discussion', 'results',
            'methods', 'methodology', 'analysis', 'background', 'literature', 'review',
            'objectives', 'goals', 'findings', 'recommendations', 'references', 'bibliography',
            'appendix', 'chapter', 'section', 'part', 'overview', 'approach', 'framework'
        ]

    def extract(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract outline in the exact challenge format"""
        try:
            doc = fitz.open(pdf_path)

            # Extract title
            title = self._extract_title(doc)

            # Extract headings with hierarchy
            outline = self._extract_headings(doc)

            doc.close()

            # Return in exact challenge format
            return {
                "title": title,
                "outline": outline
            }

        except Exception as e:
            return {
                "title": f"Error processing {pdf_path.name}",
                "outline": []
            }

    def _extract_title(self, doc) -> str:
        """Extract the document title"""
        # Try metadata first
        metadata = doc.metadata
        if metadata and metadata.get('title'):
            title = metadata['title'].strip()
            if title and len(title) < 200:
                return title

        # Look for title on first page
        if len(doc) > 0:
            first_page = doc[0]
            
            # Get text with formatting
            text_dict = first_page.get_text("dict")
            
            # Find largest font size text (likely title)
            font_sizes = []
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_sizes.append(span["size"])
            
            if font_sizes:
                max_font = max(font_sizes)
                
                # Find text with maximum font size
                for block in text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                if span["size"] == max_font:
                                    text = span["text"].strip()
                                    # Validate as title (reasonable length, not just numbers/symbols)
                                    if 5 < len(text) < 200 and re.search(r'[A-Za-z]', text):
                                        return text

        return "Untitled Document"

    def _extract_headings(self, doc) -> List[Dict[str, Any]]:
        """Extract headings with improved detection and hierarchy"""
        all_text_info = []

        # Collect all text with formatting information
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_dict = page.get_text("dict")
            
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        line_text = ""
                        line_font_size = 0
                        line_font_flags = 0
                        
                        for span in line["spans"]:
                            line_text += span["text"]
                            line_font_size = max(line_font_size, span["size"])
                            line_font_flags |= span["flags"]
                        
                        line_text = line_text.strip()
                        if line_text:
                            all_text_info.append({
                                "text": line_text,
                                "font_size": line_font_size,
                                "font_flags": line_font_flags,
                                "page": page_num + 1
                            })

        if not all_text_info:
            return []

        # Calculate font statistics
        font_sizes = [info["font_size"] for info in all_text_info]
        avg_font_size = statistics.mean(font_sizes)

        # Extract potential headings with improved logic
        headings = []
        
        for info in all_text_info:
            text = info["text"]
            font_size = info["font_size"]
            font_flags = info["font_flags"]
            page = info["page"]
            
            # Skip very long text (likely body text) and very short text
            if len(text) > 100 or len(text) < 3:
                continue
                
            is_heading = False
            
            # Check various heading criteria
            font_ratio = font_size / avg_font_size
            
            # Font size based detection
            if font_ratio > 1.2:
                is_heading = True
            
            # Bold text detection
            if font_flags & 2**4:  # Bold flag
                if font_ratio > 1.05:  # Even slightly larger bold text
                    is_heading = True
            
            # Pattern-based detection
            for pattern in self.heading_patterns:
                if re.match(pattern, text, re.IGNORECASE):
                    is_heading = True
                    break
            
            # All caps detection (but not too long)
            if text.isupper() and 3 < len(text) < 50:
                is_heading = True
            
            # Keyword-based validation
            text_lower = text.lower()
            if any(keyword in text_lower for keyword in self.heading_keywords):
                is_heading = True
            
            if is_heading:
                heading_level = self._determine_heading_level(text, font_size, font_flags, avg_font_size)
                
                # Clean the text
                cleaned_text = self._clean_heading_text(text)
                if cleaned_text:
                    headings.append({
                        "level": heading_level,
                        "text": cleaned_text,
                        "page": page
                    })

        # Remove duplicates and sort by page
        unique_headings = []
        seen_texts = set()
        
        for heading in sorted(headings, key=lambda x: x["page"]):
            text_key = heading["text"].lower().strip()
            if text_key not in seen_texts and len(heading["text"]) > 2:
                seen_texts.add(text_key)
                unique_headings.append(heading)

        return unique_headings

    def _determine_heading_level(self, text: str, font_size: float, font_flags: int, avg_font_size: float) -> str:
        """Determine heading level with improved logic"""
        
        # Check for numbered patterns first (most reliable)
        if re.match(r'^\d+\.?\s+[A-Za-z]', text):
            return "H1"
        elif re.match(r'^\d+\.\d+\.?\s+[A-Za-z]', text):
            return "H2" 
        elif re.match(r'^\d+\.\d+\.\d+\.?\s+[A-Za-z]', text):
            return "H3"
        
        # Check for chapter/section patterns
        if re.match(r'^Chapter\s+\d+', text, re.IGNORECASE):
            return "H1"
        elif re.match(r'^Section\s+\d+', text, re.IGNORECASE):
            return "H2"
        
        # Font size based determination with improved thresholds
        font_ratio = font_size / avg_font_size
        
        if font_ratio > 1.6:
            return "H1"
        elif font_ratio > 1.3:
            return "H2"
        elif font_ratio > 1.1:
            return "H3"
        
        # Font flags consideration (bold, italic)
        if font_flags & 2**4:  # Bold flag
            if font_ratio > 1.15:
                return "H2"
            else:
                return "H3"
                
        # Fallback based on text characteristics
        text_lower = text.lower()
        
        # Major section indicators
        major_indicators = ['introduction', 'conclusion', 'abstract', 'summary', 'references']
        if any(indicator in text_lower for indicator in major_indicators):
            return "H1"
        
        # Minor section indicators  
        minor_indicators = ['methods', 'results', 'discussion', 'analysis', 'background']
        if any(indicator in text_lower for indicator in minor_indicators):
            return "H2"
            
        return "H3"

    def _clean_heading_text(self, text: str) -> str:
        """Clean and normalize heading text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove page numbers at the end
        text = re.sub(r'\s+\d+\s*$', '', text)
        
        # Remove common artifacts
        text = re.sub(r'^[\.\-\s]+', '', text)  # Leading dots/dashes
        text = re.sub(r'[\.\-\s]+$', '', text)  # Trailing dots/dashes
        
        return text if len(text) > 2 else None
