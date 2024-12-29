import sqlite3
from openai import OpenAI
from datetime import datetime
import os
from typing import List, Dict, Any
import json

# Replace with your OpenAI API key
client = OpenAI(api_key="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")


# Function to convert datetime to string for SQLite
def datetime_to_str(dt):
    return dt.isoformat()


# Database setup
def setup_database():
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()

    # FAQ System table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        response TEXT,
        timestamp TEXT
    )''')

    # Content Summarizer table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_text TEXT,
        summary TEXT,
        timestamp TEXT
    )''')

    # Journal entries table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry TEXT,
        reflection TEXT,
        timestamp TEXT
    )''')

    # Ideas table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        ideas TEXT,
        timestamp TEXT
    )''')

    # Email replies table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_replies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_email TEXT,
        reply TEXT,
        timestamp TEXT
    )''')

    # Code snippets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS code_snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        code TEXT,
        timestamp TEXT
    )''')

    # Blog posts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blog_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keywords TEXT,
        content TEXT,
        timestamp TEXT
    )''')

    # Quiz table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        questions_answers TEXT,
        timestamp TEXT
    )''')

    # Sentiment analysis table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sentiment_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        sentiment TEXT,
        timestamp TEXT
    )''')

    # Product reviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reviews TEXT,
        summary TEXT,
        timestamp TEXT
    )''')

    # Course chapters table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS course_chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        subject TEXT,
        level TEXT,
        contents TEXT,
        timestamp TEXT
    )''')

    conn.commit()
    conn.close()


def get_chatgpt_response(prompt: str) -> str:
    """Generic function to get response from ChatGPT API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"


# Task 1: FAQ System
def handle_faq(question: str) -> str:
    prompt = f"You are a support assistant. Answer the following question in one paragraph: {question}"
    response = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO faq_logs (question, response, timestamp) VALUES (?, ?, ?)",
        (question, response, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return response

# Task 2: Content Summarizer
def handle_summarization(text: str) -> str:
    prompt = f"Summarize the following text in under 150 words:\n\n{text}"
    summary = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO summaries (original_text, summary, timestamp) VALUES (?, ?, ?)",
        (text, summary, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return summary

def get_summary_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT original_text, summary, timestamp FROM summaries ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            'original_text': row[0],
            'summary': row[1],
            'timestamp': row[2]
        })
    return history

# Task 3: Daily Journal
def handle_journal_entry(entry: str) -> str:
    prompt = f"""Generate a positive, empathetic, and insightful reflection based on this journal entry. 
    Include both emotional support and constructive insights. Journal entry: {entry}"""
    reflection = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO journal_entries (entry, reflection, timestamp) VALUES (?, ?, ?)",
        (entry, reflection, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return reflection

def get_journal_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT entry, reflection, timestamp FROM journal_entries ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            'entry': row[0],
            'reflection': row[1],
            'timestamp': row[2]
        })
    return history


# Task 4: Idea Generator
def handle_idea_generation(topic: str) -> str:
    prompt = f"""Generate three unique, creative, and detailed ideas related to this topic: {topic}
    For each idea, provide:
    - A descriptive title
    - A brief explanation
    - At least one practical implementation suggestion"""

    ideas = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ideas (topic, ideas, timestamp) VALUES (?, ?, ?)",
        (topic, ideas, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return ideas


def get_ideas_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT topic, ideas, timestamp FROM ideas ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            'topic': row[0],
            'ideas': row[1],
            'timestamp': row[2]
        })
    return history


def search_ideas(keyword: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        """SELECT topic, ideas, timestamp FROM ideas 
        WHERE topic LIKE ? OR ideas LIKE ? 
        ORDER BY timestamp DESC""",
        (f'%{keyword}%', f'%{keyword}%')
    )
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            'topic': row[0],
            'ideas': row[1],
            'timestamp': row[2]
        })
    return results


# Task 5: Email Reply Generator
def handle_email_reply(email: str) -> str:
    prompt = f"""Generate a professional, courteous, and clear reply to the following email. 
    The reply should be well-structured and maintain a positive tone while addressing all points in the original email:

    Original Email:
    {email}"""

    reply = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO email_replies (original_email, reply, timestamp) VALUES (?, ?, ?)",
        (email, reply, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return reply


def get_email_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT original_email, reply, timestamp FROM email_replies ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    return [{'original_email': row[0], 'reply': row[1], 'timestamp': row[2]} for row in rows]


# Task 6: Code Snippet Generator
def handle_code_generation(task: str) -> str:
    prompt = f"""Generate a well-documented code solution for the following task. 
    Include:
    - Brief explanation of the approach
    - Code with clear comments
    - Example usage if applicable

    Task: {task}"""

    code = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO code_snippets (task, code, timestamp) VALUES (?, ?, ?)",
        (task, code, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return code


def get_code_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT task, code, timestamp FROM code_snippets ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    return [{'task': row[0], 'code': row[1], 'timestamp': row[2]} for row in rows]


def main():
    # Create database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)

    setup_database()

    while True:
        print("\nAI Tasks Menu:")
        print("1. FAQ System")
        print("2. Content Summarizer")
        print("3. Daily Journal")
        print("4. Idea Generator")
        print("5. Email Reply Generator")
        print("6. Code Snippet Generator")
        print("7. Blog Generator")
        print("8. Quiz Generator")
        print("9. Sentiment Analysis")
        print("10. Product Review Summarizer")
        print("11. Course Chapter Generator")
        print("0. Exit")

        choice = input("\nEnter your choice (0-11): ")

        if choice == "0":
            break

        if choice == "1":
            question = input("Enter your question: ")
            print("\nResponse:", handle_faq(question))

        if choice == "2":
            print("\nContent Summarizer")
            print("1. Create new summary")
            print("2. View summary history")
            subchoice = input("Enter your choice (1-2): ")

            if subchoice == "1":
                text = input("Enter or paste the text you want to summarize:\n")
                summary = handle_summarization(text)
                print("\nSummary:")
                print(summary)

            elif subchoice == "2":
                history = get_summary_history()
                if not history:
                    print("\nNo summaries found in history.")
                else:
                    print("\nSummary History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nEntry {i}:")
                        print(f"Timestamp: {entry['timestamp']}")
                        print(f"Summary: {entry['summary']}")
                        print("-" * 50)

        if choice == "3":
                print("\nDaily Journal")
                print("1. Write new journal entry")
                print("2. View journal history")
                subchoice = input("Enter your choice (1-2): ")

                if subchoice == "1":
                    print("\nWrite your journal entry (press Enter twice to finish):")
                    lines = []
                    while True:
                        line = input()
                        if line == "":
                            break
                        lines.append(line)
                    entry = "\n".join(lines)

                    if entry:
                        reflection = handle_journal_entry(entry)
                        print("\nAI Reflection:")
                        print(reflection)
                    else:
                        print("Journal entry cannot be empty.")

                elif subchoice == "2":
                    history = get_journal_history()
                    if not history:
                        print("\nNo journal entries found.")
                    else:
                        print("\nJournal History:")
                        for i, entry in enumerate(history, 1):
                            print(f"\nEntry {i} - {entry['timestamp']}")
                            print("\nJournal Entry:")
                            print(entry['entry'])
                            print("\nAI Reflection:")
                            print(entry['reflection'])
                            print("-" * 50)

        if choice == "4":
            print("\nIdea Generator")
            print("1. Generate new ideas")
            print("2. View idea history")
            print("3. Search ideas")
            subchoice = input("Enter your choice (1-3): ")

            if subchoice == "1":
                topic = input("Enter the topic or theme for idea generation: ")
                if topic:
                    print("\nGenerating ideas...")
                    ideas = handle_idea_generation(topic)
                    print("\nGenerated Ideas:")
                    print(ideas)
                else:
                    print("Topic cannot be empty.")

            elif subchoice == "2":
                history = get_ideas_history()
                if not history:
                    print("\nNo ideas found in history.")
                else:
                    print("\nIdea History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nEntry {i} - {entry['timestamp']}")
                        print(f"Topic: {entry['topic']}")
                        print("\nIdeas:")
                        print(entry['ideas'])
                        print("-" * 50)

            elif subchoice == "3":
                keyword = input("Enter keyword to search for: ")
                if keyword:
                    results = search_ideas(keyword)
                    if not results:
                        print("\nNo matching ideas found.")
                    else:
                        print(f"\nFound {len(results)} matching entries:")
                        for i, entry in enumerate(results, 1):
                            print(f"\nMatch {i} - {entry['timestamp']}")
                            print(f"Topic: {entry['topic']}")
                            print("\nIdeas:")
                            print(entry['ideas'])
                            print("-" * 50)
                else:
                    print("Search keyword cannot be empty.")



if __name__ == "__main__":
    main()