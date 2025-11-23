import re
import pymupdf 
import json
import ftfy 
from collections import defaultdict

def filter_bold_dates(bold_texts):
    """
    Takes a list of bold text strings and returns only those
    that match a valid date pattern.
    """
    month_names = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
    # Optional day after a month
    day_part = r"(?:\s?\d{1,2}(?:st|nd|rd|th)?)?"
    # Optional whitespace before year
    year_part = r"\s*\d{4}"
    # Multiple months separated by space, comma, or newline
    multi_month = rf"(?:[\s,]*(?:and\s+)?{month_names}{day_part})*"
    # Full date pattern
    date_pattern = rf"{month_names}{day_part}{multi_month}{year_part}"
    full_pattern = re.compile(
        rf"({date_pattern})"       # capture the date
        rf"(.*?)"                  # capture text after date
        rf"(?=(?:{date_pattern})|\Z)",  # until next date or end
        re.DOTALL | re.IGNORECASE
    )
    date_regex = re.compile(date_pattern, re.IGNORECASE)
    filtered_dates = [text for text in bold_texts if date_regex.search(text)]

    return filtered_dates

def get_all_bold_lines(doc: pymupdf.Document) -> list[str]: 
    bold_lines = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                line_text = ""
                for line in b["lines"]:
                    for span in line["spans"]:
                        if "Bold" in span["font"] or span["text"] == " ":
                            line_text += span["text"]
                if line_text.strip():
                    bold_lines.append(line_text.strip())
    return bold_lines


def get_all_text(doc: pymupdf.Document) -> str:
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def get_text_in_sections(first_date, second_date, text: str):
    first_date_index, second_date_index = text.find(first_date), text.find(second_date)
    return text[first_date_index+len(first_date):second_date_index]

def clean_text(text: str) -> str:
    return ftfy.fix_text(text).replace("\n", "").replace("\t", "").strip()

diary = pymupdf.open('diary.pdf')

dirty_bold_lines = get_all_bold_lines(diary)
bold_lines = filter_bold_dates(dirty_bold_lines)
print(bold_lines)
text = get_all_text(diary)
pdf_data_dict = {'entries': defaultdict(list)}

while len(bold_lines) >= 2:
    section_text = get_text_in_sections(bold_lines[0], bold_lines[1], text)
    date = clean_text(bold_lines[0])
    pdf_data_dict["entries"][date[-4:]].append({'date': date, 'text': clean_text(section_text)})

    bold_lines.pop(0)

date = clean_text(bold_lines[0])
pdf_data_dict["entries"][date[-4:]].append({'date': clean_text(bold_lines[0]), 'text': clean_text(text[text.find(bold_lines[0]):-1])})
with open('pdf_data.json', 'w') as f:
    json.dump(pdf_data_dict, f)