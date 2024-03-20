import csv

def print_comments(title, sentences):
    print(f"Post Title: '{title}'")
    print(f"Number of Comments: {len(sentences)}")
    print("Comments:")
    for itr, comment in enumerate(sentences, 1):
        print(f"{itr}. {comment}")
    print("\n" + "-" * 70 + "\n")

def read_csv_file_row_by_row(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sentences = row['comments'].split("', '")

            sentences[0] = sentences[0].replace("['", "")
            sentences[-1] = sentences[-1].replace("']", "")

            print_comments(row['title'],sentences)

# Usage
read_csv_file_row_by_row('../Datasets/gaming_post.csv')