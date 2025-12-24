import xml.etree.ElementTree as ET
import sys
import re

def get_center(bounds_str):
    # bounds="[882,2171][1050,2339]"
    matches = re.findall(r'\[(\d+),(\d+)\]', bounds_str)
    if len(matches) != 2:
        return None
    x1, y1 = map(int, matches[0])
    x2, y2 = map(int, matches[1])
    return (x1 + x2) // 2, (y1 + y2) // 2

def find_element(xml_file, search_term):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    for node in root.iter():
        content_desc = node.get('content-desc', '')
        text = node.get('text', '')
        if search_term.lower() in content_desc.lower() or search_term.lower() in text.lower():
            bounds = node.get('bounds')
            center = get_center(bounds)
            if center:
                print(f"{center[0]} {center[1]}")
                return
    print("NOT_FOUND")

if __name__ == "__main__":
    find_element(sys.argv[1], sys.argv[2])
