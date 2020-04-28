import sys
import os
import subprocess
from difflib import SequenceMatcher

from .freetype import Face

def load_font_list():
    fonts = {}
    font_files = []
    if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
        path = os.path.join(os.environ['WINDIR'], 'Fonts')
        for r, d, f in os.walk(path):
            for file in f:
                font_files.append(os.path.join(r, file))

    elif sys.platform.startswith('darwin'):
        for path in ['/System/Library/Fonts/', '/Library/Fonts/', '~/Library/Fonts/']:
            for r, d, f in os.walk(path):
                for file in f:
                    font_files.append(os.path.join(r, file))
    else:
        for x in subprocess.getstatusoutput('fc-list')[1].split("\n"):
            font_files.append(str(x.split(": ")[0]))

    for file in font_files:
        try:
            F = Face(file)
            font_name = F.family_name.decode("utf-8") + " " + F.style_name.decode("utf-8")
            fonts[font_name] = file
            del F
        except Exception as e:
            pass
    return fonts

def findHighestMatch(font_name, search_dict):
    max_ratio = 0.0
    last_max_font = ""
    for f in search_dict:
        ratio = SequenceMatcher(None, f, font_name).ratio()
        if ratio > max_ratio :
            max_ratio = ratio
            last_max_font = f
    #print(font_name, ' > ', last_max_font, " matched at ", str(max_ratio))
    return max_ratio, last_max_font

def load_font_from_list(font_name, font_list):
    if font_name in font_list:
        status_text = str("Loaded " + font_name)
        font_file = font_list[font_name]
    else:
        font_desc = font_name.split(" ")
        candidate_fonts = font_list.copy()
        next_candidate_fonts = font_list.copy()
        for desc in font_desc:
            for f in candidate_fonts:
                if desc not in f:
                    del next_candidate_fonts[f]
            candidate_fonts = next_candidate_fonts.copy()

        if len(candidate_fonts) > 1:
            for f in candidate_fonts:
                if "Regular" not in f:
                    del next_candidate_fonts[f]

        if len(next_candidate_fonts) is not 0:
            ratio, font_match = findHighestMatch(font_name, next_candidate_fonts)
            if len(next_candidate_fonts) is 1 : ratio = 0.99
            font_file = next_candidate_fonts[font_match]
        elif len(candidate_fonts) is not 0:
            ratio, font_match = findHighestMatch(font_name, candidate_fonts)
            if len(candidate_fonts) is 1 : ratio = 0.99
            font_file = candidate_fonts[font_match]
        else:
           ratio, font_match = findHighestMatch(font_name, font_list)
           font_file = font_list[font_match]  
        status_text = str("Loaded " + font_match + " (approx match: " + str(round(ratio*100)) + " %)")
    return status_text, font_file

