import fitz
import logging
import unicodedata

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFParser:
    def __init__(self):
        self.supported_formats = ['.pdf']

    def parse_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            if doc.needs_pass:
                logger.warning(f"PDF {pdf_path} is protected by a password")
                return {"pages": [], "metadata": {}}
            metadata = doc.metadata
            pages = []
            for pg_no in range(len(doc)):
                page = doc[pg_no]
                page_data = self.extract_page_data(page, pg_no + 1)
                pages.append(page_data)
            doc.close()

            return {
                "pages" : pages,
                "metadata" : metadata
            }
        except Exception as e:
            logger.error(f"Error parsing PDF {pdf_path}: {str(e)}")
            return {"pages": [], "metadata": {}}
        
    def extract_page_data(self, page, pg_no):
        try:
            text_dict = page.get_text("dict")
            text_blocks = []
            page_height = page.rect.height
            page_width = page.rect.width
            
            if not page_height or not page_width:
                logger.error(f"Invalid page dimensions for page {pg_no}")
                return None

            for block in text_dict["blocks"]:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()

                        if not text:
                            continue
                        text = unicodedata.normalize("NFKC", text)
                        font_size = span["size"]
                        font_flags = span["flags"]
                        font_family = span["font"]

                        bbox = span["bbox"] #get bounding box coordinates of text span
                        x = bbox[0] / page.rect.width
                        y = 1 - (bbox[1] / page_height) #normalize the coordinates

                        is_bold = bool(font_flags & 16) #font flag for bold text is 16
                        is_italic = bool(font_flags & 2) #font flag for italic text is 2

                        text_block = {
                            "text": text,
                            "font_size": font_size,
                            "font_family": font_family,
                            "is_bold": is_bold,
                            "is_italic": is_italic,
                            "x": x,
                            "y": y,
                            "page": pg_no,
                            "bbox": bbox
                        }
                        text_blocks.append(text_block)
            return {
                "page_num": pg_no,
                "text_blocks": text_blocks,
                "page_width": page.rect.width,
                "page_height": page.rect.height
            }
        
        except Exception as e:
            logger.error(f"Error processing page {pg_no}: {str(e)}")
            return None

