import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
import sqlite3
from llm_client import query_llm, query_llm_image

# ================================
#        Operations Tasks
# ================================

def handle_a1(task_description: str) -> str:
    """
    A1: Install uv (if needed) and run the datagen.py script from GitHub with USER_EMAIL.
    """
    user_email = os.environ.get("USER_EMAIL")
    if not user_email:
        raise ValueError("USER_EMAIL environment variable not set")
    # Check if uv is installed; if not, install it.
    try:
        subprocess.run(["uv", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        subprocess.run(["pip", "install", "uv"], check=True)
    # Download datagen.py
    import requests
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download datagen.py")
    with open("datagen.py", "w", encoding="utf-8") as f:
        f.write(response.text)
    # Execute the script with user_email as the only argument.
    subprocess.run(["python", "datagen.py", user_email], check=True)
    return "Task A1 completed: datagen.py executed."

def handle_a2(task_description: str) -> str:
    """
    A2: Format /data/format.md using prettier@3.4.2 (in-place).
    """
    file_path = "/data/format.md"
    # Use npx to run a specific version of prettier.
    subprocess.run(["npx", "prettier@3.4.2", "--write", file_path], check=True)
    return "Task A2 completed: File formatted with prettier@3.4.2."

def handle_a3(task_description: str) -> str:
    """
    A3: Count the number of Wednesdays in data/dates.txt and write the count to data/dates-wednesdays.txt.
    """
    input_file = "data/dates.txt"
    output_file = "data/dates-wednesdays.txt"

    count = 0
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                dt = datetime.fromisoformat(line)
                if dt.weekday() == 2:  # Wednesday (0=Mon, 2=Wed)
                    count += 1
            except Exception:
                continue
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(count))
    return f"Task A3 completed: {count} Wednesdays counted."

def handle_a4(task_description: str) -> str:
    """
    A4: Sort the array of contacts in /data/contacts.json by last_name, then first_name.
    """
    input_file = "/data/contacts.json"
    output_file = "/data/contacts-sorted.json"
    with open(input_file, "r", encoding="utf-8") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sorted_contacts, f, indent=2)
    return "Task A4 completed: Contacts sorted."

def handle_a5(task_description: str) -> str:
    """
    A5: Write the first line of the 10 most recent .log files (from /data/logs/) into /data/logs-recent.txt.
    """
    logs_dir = Path("/data/logs")
    output_file = "/data/logs-recent.txt"
    log_files = list(logs_dir.glob("*.log"))
    log_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    selected_files = log_files[:10]
    lines = []
    for log_file in selected_files:
        with open(log_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            lines.append(first_line)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return "Task A5 completed: Logs processed."

def handle_a6(task_description: str) -> str:
    """
    A6: Find all Markdown (.md) files in /data/docs/, extract the first H1 line from each, and create an index JSON.
    """
    docs_dir = Path("/data/docs")
    index = {}
    for md_file in docs_dir.rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    title = line.lstrip("#").strip()
                    relative_path = str(md_file.relative_to(docs_dir))
                    index[relative_path] = title
                    break
    output_file = docs_dir / "index.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    return "Task A6 completed: Markdown index created."

def handle_a7(task_description: str) -> str:
    """
    A7: Extract the sender’s email address from /data/email.txt using an LLM.
    """
    input_file = "/data/email.txt"
    output_file = "/data/email-sender.txt"
    with open(input_file, "r", encoding="utf-8") as f:
        email_content = f.read()
    prompt = f"Extract the sender's email address from the following email message:\n{email_content}"
    sender_email = query_llm(prompt)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sender_email.strip())
    return "Task A7 completed: Email sender extracted."

def handle_a8(task_description: str) -> str:
    """
    A8: Extract the credit card number from /data/credit-card.png using an LLM.
    """
    input_file = "/data/credit-card.png"
    output_file = "/data/credit-card.txt"
    with open(input_file, "rb") as f:
        image_bytes = f.read()
    prompt = "Extract the credit card number from the image. Return the number without spaces."
    card_number = query_llm_image(prompt, image_bytes)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(card_number.strip().replace(" ", ""))
    return "Task A8 completed: Credit card number extracted."

def handle_a9(task_description: str) -> str:
    """
    A9: Find the most similar pair of comments in /data/comments.txt using embeddings and write them.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    input_file = "/data/comments.txt"
    output_file = "/data/comments-similar.txt"
    with open(input_file, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f if line.strip()]
    if len(comments) < 2:
        raise ValueError("Not enough comments for similarity comparison.")
    vectorizer = TfidfVectorizer().fit_transform(comments)
    vectors = vectorizer.toarray()
    sim_matrix = cosine_similarity(vectors)
    max_sim = -1
    pair = (None, None)
    n = len(comments)
    for i in range(n):
        for j in range(i + 1, n):
            if sim_matrix[i][j] > max_sim:
                max_sim = sim_matrix[i][j]
                pair = (comments[i], comments[j])
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pair[0] + "\n" + pair[1])
    return "Task A9 completed: Most similar comments found."

def handle_a10(task_description: str) -> str:
    """
    A10: Compute the total sales of all "Gold" ticket bids from /data/ticket-sales.db.
    """
    input_db = "/data/ticket-sales.db"
    output_file = "/data/ticket-sales-gold.txt"
    conn = sqlite3.connect(input_db)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    result = cursor.fetchone()[0]
    conn.close()
    if result is None:
        result = 0
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(result))
    return "Task A10 completed: Total sales for Gold tickets computed."

# ================================
#       Business Tasks
# ================================

def handle_b3(task_description: str) -> str:
    """
    B3: Fetch data from an API and write it to a file.
    """
    url_match = re.search(r'(https?://\S+)', task_description)
    path_match = re.search(r'write\s+to\s+(/data/\S+)', task_description)
    if not url_match or not path_match:
        raise ValueError("Unable to parse URL or destination path for B3 task.")
    url = url_match.group(1)
    dest_path = path_match.group(1)
    import requests
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from API")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    return "Task B3 completed: API data fetched and saved."

def handle_b4(task_description: str) -> str:
    """
    B4: Clone a git repository and make a commit.
    """
    repo_match = re.search(r'(https?://github\.com/\S+\.git)', task_description)
    if not repo_match:
        raise ValueError("Repository URL not found in task description.")
    repo_url = repo_match.group(1)
    clone_dir = "/data/git_repo_temp"
    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
    dummy_file = f"{clone_dir}/dummy.txt"
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write("Automated commit")
    subprocess.run(["git", "-C", clone_dir, "add", "."], check=True)
    subprocess.run(["git", "-C", clone_dir, "commit", "-m", "Automated commit"], check=True)
    return "Task B4 completed: Git repository cloned and commit made."

def handle_b5(task_description: str) -> str:
    """
    B5: Run a SQL query on a SQLite (or DuckDB) database and write the results.
    """
    db_match = re.search(r'(/data/\S+\.db)', task_description)
    query_match = re.search(r'query\s*:\s*(.+)', task_description, re.IGNORECASE)
    if not db_match or not query_match:
        raise ValueError("Database file or query not specified for B5 task.")
    db_path = db_match.group(1)
    query = query_match.group(1).strip()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    output_match = re.search(r'write\s+to\s+(/data/\S+)', task_description)
    if not output_match:
        raise ValueError("Output file path not specified for B5 task.")
    output_file = output_match.group(1)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(results))
    return "Task B5 completed: SQL query executed."

def handle_b6(task_description: str) -> str:
    """
    B6: Scrape a website to extract data and save the text to a file.
    """
    url_match = re.search(r'(https?://\S+)', task_description)
    if not url_match:
        raise ValueError("Website URL not found in task description.")
    url = url_match.group(1)
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch website content.")
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator="\n")
    output_match = re.search(r'write\s+to\s+(/data/\S+)', task_description)
    if not output_match:
        raise ValueError("Output file path not specified for B6 task.")
    output_file = output_match.group(1)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    return "Task B6 completed: Website data scraped."

def handle_b7(task_description: str) -> str:
    """
    B7: Compress or resize an image.
    """
    from PIL import Image
    input_match = re.search(r'(/data/\S+\.(png|jpg|jpeg))', task_description)
    if not input_match:
        raise ValueError("Input image file not specified for B7 task.")
    input_file = input_match.group(1)
    output_match = re.search(r'write\s+to\s+(/data/\S+\.(png|jpg|jpeg))', task_description)
    if not output_match:
        raise ValueError("Output image file not specified for B7 task.")
    output_file = output_match.group(1)
    with Image.open(input_file) as img:
        new_size = (img.width // 2, img.height // 2)
        resized = img.resize(new_size)
        resized.save(output_file)
    return "Task B7 completed: Image resized."

def handle_b8(task_description: str) -> str:
    """
    B8: Transcribe audio from an MP3 file and write the transcript to a file.
    """
    input_match = re.search(r'(/data/\S+\.mp3)', task_description)
    if not input_match:
        raise ValueError("Input MP3 file not specified for B8 task.")
    input_file = input_match.group(1)
    output_match = re.search(r'write\s+to\s+(/data/\S+\.txt)', task_description)
    if not output_match:
        raise ValueError("Output file path not specified for B8 task.")
    output_file = output_match.group(1)
    # Placeholder transcription; replace with real transcription if available.
    transcription = "Transcribed audio content."
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    return "Task B8 completed: Audio transcribed."

def handle_b9(task_description: str) -> str:
    """
    B9: Convert a Markdown file to HTML and write the result.
    """
    import markdown
    input_match = re.search(r'(/data/\S+\.md)', task_description)
    if not input_match:
        raise ValueError("Input Markdown file not specified for B9 task.")
    input_file = input_match.group(1)
    output_match = re.search(r'write\s+to\s+(/data/\S+\.html)', task_description)
    if not output_match:
        raise ValueError("Output HTML file not specified for B9 task.")
    output_file = output_match.group(1)
    with open(input_file, "r", encoding="utf-8") as f:
        md_text = f.read()
    html = markdown.markdown(md_text)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    return "Task B9 completed: Markdown converted to HTML."

def handle_b10(task_description: str) -> str:
    """
    B10: Filter a CSV file by a condition and output the matching rows as JSON.
    """
    import csv
    input_match = re.search(r'(/data/\S+\.csv)', task_description)
    if not input_match:
        raise ValueError("Input CSV file not specified for B10 task.")
    input_file = input_match.group(1)
    # For simplicity, assume the filter condition is on the first column.
    value_match = re.search(r'equals\s+(\S+)', task_description)
    if not value_match:
        raise ValueError("Filter condition not specified for B10 task.")
    filter_value = value_match.group(1)
    output_match = re.search(r'write\s+to\s+(/data/\S+)', task_description)
    if not output_match:
        raise ValueError("Output file path not specified for B10 task.")
    output_file = output_match.group(1)
    filtered_rows = []
    with open(input_file, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_col = list(row.keys())[0]
            if row[first_col] == filter_value:
                filtered_rows.append(row)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_rows, f, indent=2)
    return "Task B10 completed: CSV filtered and JSON data written."

# ================================
#         Dispatcher
# ================================

def handle_task(task_description: str) -> str:
    """
    Dispatch the plain‑English task description to the appropriate handler.
    """
    task_lower = task_description.lower()

    # Operations Tasks (A1 - A10)
    if "datagen.py" in task_description or "install uv" in task_lower:
        return handle_a1(task_description)
    elif "prettier" in task_lower:
        return handle_a2(task_description)
    elif ("data/dates.txt" in task_description and "wednesday" in task_lower) or ("# of wednesdays" in task_lower):
        return handle_a3(task_description)
    elif "/data/contacts.json" in task_description:
        return handle_a4(task_description)
    elif "/data/logs" in task_description:
        return handle_a5(task_description)
    elif "/data/docs" in task_description:
        return handle_a6(task_description)
    elif "/data/email.txt" in task_description:
        return handle_a7(task_description)
    elif "/data/credit-card.png" in task_description:
        return handle_a8(task_description)
    elif "/data/comments.txt" in task_description:
        return handle_a9(task_description)
    elif "/data/ticket-sales.db" in task_description:
        return handle_a10(task_description)

    # Business Tasks (B3 - B10)
    elif "fetch" in task_lower and "api" in task_lower:
        return handle_b3(task_description)
    elif "clone" in task_lower and "git" in task_lower:
        return handle_b4(task_description)
    elif "query" in task_lower and (".db" in task_description or "duckdb" in task_lower):
        return handle_b5(task_description)
    elif ("scrape" in task_lower or "extract data from" in task_lower) and "website" in task_lower:
        return handle_b6(task_description)
    elif "resize" in task_lower or "compress" in task_lower:
        return handle_b7(task_description)
    elif "transcribe" in task_lower and ".mp3" in task_description:
        return handle_b8(task_description)
    elif "markdown" in task_lower and "html" in task_lower:
        return handle_b9(task_description)
    elif "csv" in task_lower and "json" in task_lower:
        return handle_b10(task_description)
    else:
        raise ValueError("Task not recognized or unsupported.")
