#!/usr/bin/env python3
"""
Adobe Hackathon Round 1A - PDF Outline Extraction
Structured PDF Outline Extraction with heading levels and page numbers
"""

import os
import sys
import json
import time
from pathlib import Path
from outline_extractor import OutlineExtractor

def main():
    """Main function for Round 1A: PDF Outline Extraction"""

    print("🚀 Adobe Hackathon Round 1A - PDF Outline Extraction Starting...")

    input_dir = Path("/app/input")
    output_dir = Path("/app/output")

    # Ensure directories exist
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # Find all PDF files
    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        print("⚠️ No PDF files found in /app/input directory")
        return

    print(f"📁 Found {len(pdf_files)} PDF files to process")

    # Initialize outline extractor
    outline_extractor = OutlineExtractor()

    # Process each PDF for outline extraction
    print("\n🏷️ Extracting PDF outlines...")

    for pdf_file in pdf_files:
        try:
            print(f"📄 Processing {pdf_file.name}...")
            start_time = time.time()

            # Extract outline
            result = outline_extractor.extract(pdf_file)

            # Save with exact challenge format
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

            processing_time = time.time() - start_time
            heading_count = len(result.get('outline', []))
            
            print(f"✅ Outline extracted: {heading_count} headings found in {processing_time:.2f}s")

        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {str(e)}")

    print("\n🎯 Round 1A Processing Complete!")

if __name__ == "__main__":
    main()
