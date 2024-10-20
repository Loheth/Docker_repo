import os  # Import os module for file path manipulations
import re  # Import re module for regular expression operations
import socket  # Import socket module to retrieve the IP address of the machine
from collections import Counter  # Import Counter to count the frequency of words

# Function to count the total words in a file and return the word list
def count_words(file_path):
    with open(file_path, 'r') as file:  # Open the specified file in read mode
        text = file.read()  # Read the content of the file while preserving the original case
        # Split the text into words and filter out any empty strings
        words = [word for word in text.split() if word]
    return len(words), words  # Return the total word count and the list of words

# Function to handle and expand contractions in the list of words
def handle_contractions(words):
    expanded_words = []  # Initialize a list to hold expanded words
    # Define a regex pattern to match common contractions
    contraction_pattern = re.compile(r"(\w+)'(ll|m|t|ve|s|d|re)")

    for word in words:  # Iterate over each word in the list
        if contraction_pattern.search(word):  # Check if the word matches the contraction pattern
            # Expand the contraction by replacing it with its full form
            expanded_word = contraction_pattern.sub(r"\1 \2", word)
            expanded_words.extend(expanded_word.split())  # Add the expanded words to the list
        else:
            expanded_words.append(word)  # If not a contraction, add the word as is

    return expanded_words  # Return the list of expanded words

# Function to get the most frequent words from a list
def most_frequent_words(words, n=3):
    return Counter(words).most_common(n)  # Return the n most common words and their counts

# Main logic to execute the word counting and processing
if __name__ == "__main__":
    # List of files to process
    files = ['/home/data/IF.txt', '/home/data/AlwaysRememberUsThisWay.txt']
    results = {}  # Dictionary to store results for each file

    total_words = 0  # Initialize total words counter
    
    # Loop through each file to count words and gather results
    for file in files:
        count, words = count_words(file)  # Count words in the current file
        total_words += count  # Update the total word count
        results[file] = {
            'word_count': count,  # Store the word count for the file
            'words': words,  # Store the list of words to calculate top words later
        }

    # Process the second file to handle contractions
    results[files[1]]['words'] = handle_contractions(results[files[1]]['words'])

    # Calculate the top words for each file and store the results
    results[files[0]]['top_words'] = most_frequent_words(results[files[0]]['words'])
    results[files[1]]['top_words'] = most_frequent_words(results[files[1]]['words'])

    # Get the IP address of the current machine
    ip_address = socket.gethostbyname(socket.gethostname())

    # Define the path for the output results file
    output_path = '/home/data/output/result.txt'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Create the output directory if it doesn't exist

    # Write the results to the specified output file
    with open(output_path, 'w') as result_file:
        result_file.write(f"Total words in IF.txt: {results[files[0]]['word_count']}\n")
        result_file.write(f"Total words in AlwaysRememberUsThisWay.txt: {results[files[1]]['word_count']}\n")
        result_file.write(f"Grand total words: {total_words}\n")
        
        result_file.write("Top 3 words in IF.txt:\n")
        for word, count in results[files[0]]['top_words']:  # Write the top words for the first file
            result_file.write(f"{word}: {count}\n")
        
        result_file.write("Top 3 words in AlwaysRememberUsThisWay.txt (after handling contractions):\n")
        for word, count in results[files[1]]['top_words']:  # Write the top words for the second file
            result_file.write(f"{word}: {count}\n")
        
        result_file.write(f"IP Address: {ip_address}\n")  # Write the IP address of the machine

    # Print the contents of the result file to the console
    with open(output_path, 'r') as result_file:
        print(result_file.read())  # Display the results
