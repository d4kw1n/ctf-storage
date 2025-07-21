import sqlite3
import os
import re

FLAG = os.getenv("FLAG", "HCMUS-CTF{*** REDACTED ***}")

# Read and parse input file
with open("papers.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Group every 2 lines as a paper
papers = []
for i in range(0, len(lines), 2):
    title = lines[i]
    author_line = lines[i + 1]
    authors = []
    for author_entry in author_line.split(", "):
        # Match "Name (Aff1,Aff2)"
        match = re.match(r"^(.*?)\s+\((.*?)\)$", author_entry)
        if match:
            name = match.group(1).strip()
            affiliations = [aff.strip() for aff in match.group(2).split(",")]
            authors.append((name, affiliations))
    papers.append((title, authors))

# Init DB
conn = sqlite3.connect("database.db")

conn.execute("""CREATE TABLE paper (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);""")

conn.execute("""CREATE TABLE author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);""")

conn.execute("""CREATE TABLE paper_author (
    paper_id INTEGER,
    author_id INTEGER,
    affiliation TEXT,
    FOREIGN KEY (paper_id) REFERENCES paper(id),
    FOREIGN KEY (author_id) REFERENCES author(id)
);""")

conn.execute("""CREATE TABLE flag (
    flag TEXT NOT NULL
);""")
conn.execute("INSERT INTO flag VALUES (?)", (FLAG,))

# Insert papers and authors
author_cache = {}  # to avoid duplicates
for title, authors in papers:
    cursor = conn.execute("INSERT INTO paper (title) VALUES (?)", (title,))
    paper_id = cursor.lastrowid

    for name, affiliations in authors:
        if name not in author_cache:
            cursor = conn.execute("INSERT INTO author (name) VALUES (?)", (name,))
            author_id = cursor.lastrowid
            author_cache[name] = author_id
        else:
            author_id = author_cache[name]

        for aff in affiliations:
            conn.execute(
                "INSERT INTO paper_author (paper_id, author_id, affiliation) VALUES (?, ?, ?)",
                (paper_id, author_id, aff),
            )

conn.commit()
conn.close()
