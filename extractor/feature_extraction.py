import re
import numpy as np
from collections import Counter

class FeatureExtract:
    def __init__(self):
        self.heading_patterns = [
            r'^\d+\.\s',           # 1. 
            r'^\d+\.\d+\.\s',      # 1.1. 
            r'^\d+\.\d+\.\d+\.\s', # 1.1.1. 
            r'^[A-Z]\.\s',         # A. 
            r'^[IVX]+\.\s',        # I. II. III. 
            r'^Chapter\s+\d+',     # Chapter 1
            r'^Section\s+\d+',     # Section 1
        ]
        
        self.compiled_patterns = [re.compile(pattern) for pattern in self.heading_patterns]
    
    def calc_document_stats(self, doc_data):
        blocks = []
        font_sizes = []
        font_families = []

        for page in doc_data["pages"]:
            for block in page["text_blocks"]:
                blocks.append(block)
                font_sizes.append(block["font_size"])
                font_families.append(block["font_family"])
        if not font_sizes:
            return {}
        
        font_counter = Counter(font_families)
        
        return {
            "avg_font_size": np.mean(font_sizes),
            "max_font_size": np.max(font_sizes),
            "min_font_size": np.min(font_sizes),
            "common_font": font_counter.most_common(1)[0][0] if font_counter else "",
            "total_blocks": len(blocks)
        }


