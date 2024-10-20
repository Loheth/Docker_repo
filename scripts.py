import os
import re
import socket
from collections import Counter

def count_words(file_path):
    with open(file_path, 'r') as file:
        text = file.read()  # Keep the original case
        # Split text by spaces and filter out empty strings
        words = [word for word in text.split() if word]
    return len(words), words

def handle_contractions(words):
    # This function expands contractions using regex
    expanded_words = []
    contraction_pattern = re.compile(r"(\w+)'(ll|m|t|ve|s|d|re)")  # Capture common contractions

    for word in words:
        if contraction_pattern.search(word):
            # Expand contractions by replacing them with their full forms
            expanded_word = contraction_pattern.sub(r"\1 \2", word)
            expanded_words.extend(expanded_word.split())
        else:
            expanded_words.append(word)

    return expanded_words

def most_frequent_words(words, n=3):
    return Counter(words).most_common(n)

# Main logic
if __name__ == "__main__":
    files = ['/home/data/IF.txt', '/home/data/AlwaysRememberUsThisWay.txt']
    results = {}

    # Count words and calculate frequencies
    total_words = 0
    
    for file in files:
        count, words = count_words(file)
        total_words += count
        results[file] = {
            'word_count': count,
            'words': words,  # Store words to calculate top words later
        }

    # Handle contractions for AlwaysRememberUsThisWay.txt
    results[files[1]]['words'] = handle_contractions(results[files[1]]['words'])

    # Calculate top words for each file
    results[files[0]]['top_words'] = most_frequent_words(results[files[0]]['words'])
    results[files[1]]['top_words'] = most_frequent_words(results[files[1]]['words'])

    # Get the IP address
    ip_address = socket.gethostbyname(socket.gethostname())

    # Write results to result.txt
    output_path = '/home/data/output/result.txt'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as result_file:
        result_file.write(f"Total words in IF.txt: {results[files[0]]['word_count']}\n")
        result_file.write(f"Total words in AlwaysRememberUsThisWay.txt: {results[files[1]]['word_count']}\n")
        result_file.write(f"Grand total words: {total_words}\n")
        
        result_file.write("Top 3 words in IF.txt:\n")
        for word, count in results[files[0]]['top_words']:
            result_file.write(f"{word}: {count}\n")
        
        result_file.write("Top 3 words in AlwaysRememberUsThisWay.txt (after handling contractions):\n")
        for word, count in results[files[1]]['top_words']:
            result_file.write(f"{word}: {count}\n")
        
        result_file.write(f"IP Address: {ip_address}\n")

    # Print the result.txt content to console
    with open(output_path, 'r') as result_file:
        print(result_file.read())
