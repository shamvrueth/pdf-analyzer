import logging

logger = logging.getLogger(__name__)

class JSONFormat:
    def __init__(self):
        self.max_levels = 3

    def build(self, detected_headings):
        if not detected_headings:
            return []
        sorted_headings = sorted(detected_headings, key=lambda x: (x["page"], -x["y"]))

        leveled_headings = self.assign_levels(sorted_headings)
        outline = []
        for heading in leveled_headings:
            outline_item = {
                "level": heading["level"],
                "text": heading["text"],
                "page": heading["page"] - 1
            }
            outline.append(outline_item)
        
        return outline
    
    def assign_levels(self, headings):
        if not headings:
            return []
        
        font_sizes = [h["font_size"] for h in headings]
        unique_sizes = sorted(set(font_sizes), reverse=True)

        if len(unique_sizes) == 1:
            level_map = {unique_sizes[0]: "H1"}
        elif len(unique_sizes) == 2:
            level_map = {unique_sizes[0]: "H1", unique_sizes[1]: "H2"}
        else:
            total_sizes = len(unique_sizes)
            h1_group_size = min(5, max(2, total_sizes // 3))
            h2_group_size = max(1, (total_sizes - h1_group_size) // 2)
            
            level_map = {}
            for i in range(h1_group_size):
                level_map[unique_sizes[i]] = "H1"
            
            for i in range(h1_group_size, h1_group_size + h2_group_size):
                level_map[unique_sizes[i]] = "H2"
            for i in range(h1_group_size + h2_group_size, total_sizes):
                level_map[unique_sizes[i]] = "H3"
        
        leveled_headings = []
        for h in headings:
            font_size = h["font_size"]
            level = level_map.get(font_size, "H3")
            head = h.copy()
            head["level"] = level
            leveled_headings.append(head)
        
        return leveled_headings