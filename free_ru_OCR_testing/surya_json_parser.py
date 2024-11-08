import os
import json
import Levenshtein as lev
import sys
import re
import collections

def clean_text(text):
      return re.sub(r'[^\w\s]', '', text.lower())

def get_word_set(text):
    words = clean_text(text).split()
    return set(words)

def calculate_jaccard_similarity(text1, text2):
    set1 = get_word_set(text1)
    set2 = get_word_set(text2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0.0

def process_file(file_path, ground_truth_text):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
        page_data = list(data.values())[0][0]['text_lines'] 
        
        text_fragments = [item['text'] for item in page_data]
    
    combined_text = " ".join(text_fragments).strip()
    lev_distance = lev.distance(ground_truth_text, combined_text)
    jaccard_similarity = calculate_jaccard_similarity(ground_truth_text, combined_text)
    return combined_text, lev_distance, jaccard_similarity

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_results.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    ground_truth_text = "ПАСПОРТ ГРАЖДАНИНА РОССИЙСКОЙ ФЕДЕРАЦИИ"

    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    try:
        combined_text, lev_distance, jaccard_similarity = process_file(file_path, ground_truth_text)
        print(f"Объединённый текст:\n{combined_text}")
        print(f"Расстояние Левенштейна: {lev_distance}")
        print(f"Сходство по Жаккару: {jaccard_similarity:.4f}")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
