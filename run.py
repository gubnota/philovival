#!/usr/bin/env python3
import sys
import json
import re
import os

# ---------------- Stage 1 ----------------
# Searches for all author names that contain Cyrillic characters.
def stage1():
    # Try to load authors from 'authors.json' if the file exists,
    # otherwise use sample data.
    authors_file = "philovival/en/authors/01.json"
    if os.path.exists(authors_file):
        with open(authors_file, "r", encoding="utf-8") as f:
            try:
                authors = json.load(f)
                authors = authors['contents']
            except json.JSONDecodeError:
                print("Error: authors.json is not valid JSON.")
                return
    else:
        # Sample data with a mix of Latin and Cyrillic names
        authors = [
            {"id": 1321, "name": "Niklas Luhmann"},
            {"id": 1322, "name": "Никола Тесла"},
            {"id": 1323, "name": "Александр Пушкин"},
            {"id": 1324, "name": "John Doe"}
        ]
    
    # Function to check if a name contains any Cyrillic characters.
    def contains_cyrillic(name):
        return bool(re.search('[\u0400-\u04FF]', name))
    
    # Search for and print authors that have Cyrillic characters.
    cyrillic_authors = [author for author in authors if contains_cyrillic(author['name'])]
    if cyrillic_authors:
        print("Cyrillic author names found:")
        for author in cyrillic_authors:
            print(author['name'])
    else:
        print("No Cyrillic author names were found.")

# ---------------- Stage 2 ----------------
# Replaces the content of ru.names.md with the filtered content of en.names.md.
def stage2():
    ru_names_path = "ru.names.md"
    en_names_path = "en.names.md"
    
    # Read the en.names.md file.
    if not os.path.exists(en_names_path):
        print(f"Error: {en_names_path} does not exist.")
        return
    
    with open(en_names_path, "r", encoding="utf-8") as en_file:
        en_lines = en_file.readlines()
    
    # Filter out empty strings and non-printable lines.
    filtered_en_lines = [line.strip() for line in en_lines if line.strip() and line.isprintable()]
    
    # Write the filtered content into ru.names.md.
    with open(ru_names_path, "w", encoding="utf-8") as ru_file:
        ru_file.write("\n".join(filtered_en_lines))
    
    print(f"Replaced {ru_names_path} with filtered content from {en_names_path}.")

# ---------------- Stage 3 ----------------
# Searches for all quotes by a certain author (by name or id) within a quotes JSON file.
# This JSON file is expected to contain "contents" for quotes and "authors" for author info.
def stage3():
    if len(sys.argv) < 3:
        print("Usage: ./run.py stage3 <json_file> [--author=<name> | --id=<id>]")
        return
    
    json_path = sys.argv[2]
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON file.")
            return

    # Expecting the JSON to include keys: "contents" for quotes and "authors" for author details.
    quotes = data.get("contents", [])
    authors = data.get("authors", [])
    
    search_by = None
    search_val = None
    # Process additional arguments for author search.
    for arg in sys.argv[3:]:
        if arg.startswith("--author="):
            search_by = "name"
            search_val = arg.split("=", 1)[1]
        elif arg.startswith("--id="):
            search_by = "id"
            try:
                search_val = int(arg.split("=", 1)[1])
            except ValueError:
                print("Invalid author id provided.")
                return

    if search_by == "name":
        author = next((a for a in authors if a['name'] == search_val), None)
        if not author:
            print(f"Author with name '{search_val}' not found.")
            return
        author_id = author["id"]
    elif search_by == "id":
        author_id = search_val
    else:
        print("Please provide either --author=<name> or --id=<id> to search for quotes.")
        return

    # Filter and print quotes matching the author id.
    matching_quotes = [q for q in quotes if q.get("author_id") == author_id]
    if not matching_quotes:
        print(f"No quotes found for author id {author_id}.")
        return
    print(f"Quotes by author id {author_id}:")
    for quote in matching_quotes:
        print(quote.get("text"))

# ---------------- Stage 4 ----------------
# Deletes or moves quotes by a certain author from 'contents' to a 'hidden' array in a JSON file.
def stage4():
    if len(sys.argv) < 4:
        print("Usage: ./run.py stage4 <json_file> --id=<id> --action=<delete|move_to_hidden>")
        return

    json_path = sys.argv[2]
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        return

    author_id = None
    action = None
    for arg in sys.argv[3:]:
        if arg.startswith("--id="):
            try:
                author_id = int(arg.split("=", 1)[1])
            except ValueError:
                print("Invalid author id provided.")
                return
        elif arg.startswith("--action="):
            action = arg.split("=", 1)[1]

    if author_id is None or action is None:
        print("Please provide both --id and --action arguments.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON file.")
            return
    
    if "contents" not in data:
        print("The JSON file does not have a 'contents' key.")
        return
    # Ensure that the hidden array exists.
    if "hidden" not in data:
        data["hidden"] = []
    
    if action == "delete":
        data["contents"] = [q for q in data["contents"] if q.get("author_id") != author_id]
        print(f"Deleted all quotes by author ID {author_id}.")
    elif action == "move_to_hidden":
        to_hide = [q for q in data["contents"] if q.get("author_id") == author_id]
        data["hidden"].extend(to_hide)
        data["contents"] = [q for q in data["contents"] if q.get("author_id") != author_id]
        print(f"Moved all quotes by author ID {author_id} to hidden.")
    else:
        print("Invalid action. Use 'delete' or 'move_to_hidden'.")
        return

    # Save the modified JSON back to the same file.
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Print updated JSON content.
    # print(json.dumps(data, indent=2, ensure_ascii=False))

# ---------------- Stage 5 ----------------
def stage5():
    if len(sys.argv) < 4:
        print("Usage: ./run.py stage5 <json_file> --action=<delete|move_to_hidden>")
        return

    json_path = sys.argv[2]
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        return

    action = None
    for arg in sys.argv[3:]:
        if arg.startswith("--action="):
            action = arg.split("=", 1)[1]

    if action is None:
        print("Please provide --action argument.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON file.")
            return
    
    if "contents" not in data:
        print("The JSON file does not have a 'contents' key.")
        return

    # Ensure hidden array exists
    if "hidden" not in data:
        data["hidden"] = []

    seen = set()
    duplicates = []
    new_contents = []

    # Detect duplicates
    for quote in data["contents"]:
        text = quote.get("text", "").strip().lower()
        if text in seen:
            duplicates.append(quote)
        else:
            seen.add(text)
            new_contents.append(quote)

    # Process duplicates based on action
    if action == "delete":
        data["contents"] = new_contents
        print(f"Deleted {len(duplicates)} duplicate quotes.")
    elif action == "move_to_hidden":
        data["hidden"].extend(duplicates)
        data["contents"] = new_contents
        print(f"Moved {len(duplicates)} duplicates to hidden.")
    else:
        print("Invalid action. Use 'delete' or 'move_to_hidden'.")
        return

    # Save changes
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------------- Stage 6 ----------------
def stage6():
    if len(sys.argv) < 4:
        print("Usage: ./run.py stage6 <authors_json> <quotes_json>")
        return

    authors_path = sys.argv[2]
    quotes_path = sys.argv[3]

    # Load authors data
    if not os.path.exists(authors_path):
        print(f"Error: {authors_path} does not exist.")
        return
    try:
        with open(authors_path, "r", encoding="utf-8") as f:
            authors_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {authors_path} is not a valid JSON file.")
        return
    authors = authors_data.get("contents", [])

    # Load quotes data
    if not os.path.exists(quotes_path):
        print(f"Error: {quotes_path} does not exist.")
        return
    try:
        with open(quotes_path, "r", encoding="utf-8") as f:
            quotes_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {quotes_path} is not a valid JSON file.")
        return
    quotes = quotes_data.get("contents", [])

    # Collect all author_ids referenced in quotes
    used_author_ids = set()
    for quote in quotes:
        author_id = quote.get("author_id")
        if author_id is not None:
            used_author_ids.add(author_id)

    # Filter authors to keep only those present in used_author_ids
    filtered_authors = [author for author in authors if author.get("id") in used_author_ids]
    removed_count = len(authors) - len(filtered_authors)
    
    # Update authors data and save
    authors_data["contents"] = filtered_authors
    with open(authors_path, "w", encoding="utf-8") as f:
        json.dump(authors_data, f, indent=2, ensure_ascii=False)
    
    print(f"Removed {removed_count} authors from {authors_path} whose quotes are not present in {quotes_path}.")

# ---------------- Main ----------------
def main():
    if len(sys.argv) < 2:
        print("Usage: ./run.py stage1|stage2|stage3|stage4|stage5|stage6 [additional arguments...]")
        sys.exit(1)
    
    stage = sys.argv[1].lower()
    if stage == "stage1":
        stage1()
    elif stage == "stage2":
        stage2()
    elif stage == "stage3":
        stage3()
    elif stage == "stage4":
        stage4()
    elif stage == "stage5":
        stage5()
    elif stage == "stage6":
        stage6()
    else:
        print("Unknown stage. Please choose stage1, stage2, stage3, stage4, stage5, stage6.")
        sys.exit(1)

if __name__ == "__main__":
    main()

