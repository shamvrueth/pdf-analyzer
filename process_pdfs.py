import logging
import os
import json
import time
from pathlib import Path
from extractor.pdf_parser import PDFParser
from extractor.heading_detection import HeadingDetect
from extractor.json_format import JSONFormat

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFExtractor:
    def __init__(self):
        self.parser = PDFParser()
        self.detector = HeadingDetect()
        self.formatter = JSONFormat()
    
    def extract_outline(self, pdf_path):
        start = time.time()
        document_data = self.parser.parse_pdf(pdf_path)
        detected_headings = self.detector.detect_heading(document_data)
        result = self.formatter.build(detected_headings)
        title = self.extract_title(document_data, pdf_path)
        for i in range(len(result)):
            if title in result[i]["text"]:
                result.pop(i)
                break
        processing_time = time.time() - start
        logger.info(f"Processed {pdf_path} in {processing_time:.2f}s")

        return {
            "title": title,
            "outline": result
        }
    
    def extract_title(self, document_data, pdf_path):
        if not document_data["pages"]:
            return Path(pdf_path).stem
        
        first_page = document_data["pages"][0]
        if not first_page["text_blocks"]:
            return Path(pdf_path).stem
        
        max_font_size = max(block["font_size"] for block in first_page["text_blocks"])

        title_candidates = [
            block for block in first_page["text_blocks"]
            if block["font_size"] == max_font_size
        ]

        if title_candidates:
            title_candidates.sort(key=lambda x: x['y'])
            return title_candidates[0]['text'].strip()
        
        return Path(pdf_path).stem
    
def main():
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    input_dir = Path(os.environ.get("INPUT_DIR", base_dir / "sample_dataset/pdfs"))
    output_dir = Path(os.environ.get("OUTPUT_DIR", base_dir / "sample_dataset/outputs"))
    
    output_dir.mkdir(exist_ok=True)

    extractor = PDFExtractor()

    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        logger.warning("No PDF files found in input directory")
        return
    
    logger.info(f"Processing {len(pdf_files)} PDF files")

    for file in pdf_files:
        try:
            result = extractor.extract_outline(file)
            output_file = output_dir / f"{file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved outline to {output_file}")

        except Exception as e:
            logger.error(f"Failed to process {file}: {str(e)}")

if __name__ == "__main__":
    main()
