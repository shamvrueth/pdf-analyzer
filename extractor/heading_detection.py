import numpy as np
import re
import logging
from .feature_extraction import FeatureExtract

logger = logging.getLogger(__name__)

class HeadingDetect:
    def __init__(self):
        self.feature_extractor = FeatureExtract()
        self.threshold = 0.6
        self.heading_patterns = [
            (r'^\d+\.\s+', 0.4),           # 1. Introduction
            (r'^\d+\.\d+\s+', 0.4),        # 1.1 Overview  
            (r'^\d+\.\d+\.\d+\s+', 0.3),   # 1.1.1 Details
            (r'^[A-Z]\.\s+', 0.4),         # A. Appendix
            (r'^[IVX]+\.\s+', 0.4),        # I. Roman numerals
            (r'^Chapter\s+\d+', 0.2),      # Chapter 1
            (r'^Section\s+\d+', 0.2),      # Section 1
            (r'^Part\s+[IVX\d]+', 0.2),    # Part I
        ]
        self.compiled_patterns = [(re.compile(pattern, re.IGNORECASE), score) for pattern, score in self.heading_patterns]

    
    def detect_heading(self, document_data):
        stats = self.feature_extractor.calc_document_stats(document_data)
        blocks = []
        detected_headings = []
        
        
        for page in document_data["pages"]:
            blocks.extend(page["text_blocks"])

        if not blocks:
            return []
        
        for block in blocks:
            score = self.calc_score(block, stats)
            if score > self.threshold:
                block_with_score = block.copy()
                block_with_score["score"] = score
                detected_headings.append(block_with_score)
        
        detected_headings = self.merge_headings(detected_headings)
        logger.info(f"Detected {len(detected_headings)} headings using rule-based approach")
        return detected_headings

    def calc_score(self, text_block, doc_stats):
        text = text_block["text"].strip()
        score = 0
        if not text:
            return 0
        
        score += self.font_size_score(text_block, doc_stats)
        score += self.pattern_matching_score(text)
        score += self.font_weight_score(text_block, doc_stats)
        score += self.position_score(text_block)
        score *= self.length_penalty(text)
        
        return min(score, 1.0)
        
    def font_size_score(self, text_block, doc_stats):
        size = text_block["font_size"]
        avg_size = doc_stats.get("avg_font_size", size)
        max_size = doc_stats.get("max_font_size", size)

        if avg_size == 0:
            return 0
        ratio = size / avg_size
        score = 0
        if ratio >= 1.5:
            score = 0.6  
        elif ratio >= 1.3:
            score = 0.4
        elif ratio >= 1.15:
            score = 0.25
        elif ratio >= 1.05:
            score = 0.15
        else:
            score = 0
        if size > (max_size * 0.9):  # If font size is within 90% of max
            score = min(0.8, score + 0.2)
        return score
    
    def pattern_matching_score(self, text):
        for pattern, score in self.compiled_patterns:
            if pattern.match(text):
                return score
        return 0.0
    
    def font_weight_score(self, text_block, doc_stats):
        score = 0.0
        if text_block.get("is_bold", False):
            score += 0.1
        
        if text_block.get("is_italic", False):
            score += 0.05

        if text_block.get("is_bold", False) and text_block.get("font_size", 0) > doc_stats.get("avg_font_size", 0):
            score += 0.25
        
        return score
    
    def position_score(self, text_block):
        score = 0.0
        
        x_pos = text_block.get("x", 0)
        y_pos = text_block.get("y", 0)

        if x_pos < 0.15:
            score += 0.1

        if y_pos > 0.8:
            score += 0.15

        if y_pos > 0.2:
            score += 0.05

        return score

    def length_penalty(self, text):
        word_count = len(text.split())
        char_count = len(text)

        if 2 <= word_count <= 8 and 5 <= char_count <= 80:
            return 1.0

        elif 1 <= word_count <= 15 and 3 <= char_count <= 120:
            return 0.8

        elif word_count == 1 and 3 <= char_count <= 20:
            return 0.7
        
        elif word_count > 20 or char_count > 200:
            return 0.1

        elif word_count < 1 or char_count < 2:
            return 0.0
        
        return 0.5
    
    def process_headings(self, headings, doc_stats):
        if not headings:
            return headings
        
        s = set()
        unique = []

        for heading in headings:
            key = (heading["text"], heading["page"])
            if key not in s:
                s.add(key)
                unique.append(heading)
        filtered = []
        for i, heading in enumerate(unique):
            is_duplicate = False
            for j, other in enumerate(unique):
                if i != j and heading["page"] == other["page"]:
                    if self.texts_are_similar(heading["text"], other["text"]):
                        if heading["confidence"] <= other["confidence"]:
                            is_duplicate = True
                            break
            
            if not is_duplicate:
                filtered.append(heading)
        
        min_threshold = 0.4
        quality_filtered = [h for h in filtered if h["confidence"] >= min_threshold]
        
        return quality_filtered

    def texts_are_similar(self, text1, text2, threshold):
        if abs(len(text1) - len(text2)) > min(len(text1), len(text2)) * 0.3:
            return False
        
        common_chars = sum(1 for c1, c2 in zip(text1.lower(), text2.lower()) if c1 == c2)
        max_len = max(len(text1), len(text2))
        
        if max_len == 0:
            return True
        
        similarity = common_chars / max_len
        return similarity >= threshold

    def merge_headings(self, headings):
        if not headings:
            return []
        merged_list = []
        current_group = [headings[0]]

        for i in range(1, len(headings)):
            current_heading = headings[i]
            first_in_group = current_group[0]

            if (current_heading['page'] == first_in_group['page']) and abs(current_heading['y'] - first_in_group['y']) < 0.05:
                current_group.append(current_heading)
            else:
                merged_list.append(self.merge_group(current_group))
                current_group = [current_heading]

        merged_list.append(self.merge_group(current_group))

        return merged_list
    
    def merge_group(self, group):
        """Helper function to combine a list of dictionaries into one."""
        if len(group) == 1:
            return group[0]

        group.sort(key=lambda h: h['x'])

        merged = group[0].copy()

        merged['text'] = ' '.join(h['text'] for h in group)

        min_x0 = min(h['bbox'][0] for h in group)
        min_y0 = min(h['bbox'][1] for h in group)
        max_x1 = max(h['bbox'][2] for h in group)
        max_y1 = max(h['bbox'][3] for h in group)
        merged['bbox'] = [min_x0, min_y0, max_x1, max_y1]

        merged['score'] = max(h['score'] for h in group)

        return merged