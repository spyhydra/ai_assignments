import sqlite3
from openai import OpenAI
from datetime import datetime
import os
from typing import List, Dict, Any


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


# Task 7: Blog Generator
def handle_blog_generation(keywords: str) -> str:
    prompt = f"""Generate a well-structured, engaging blog post (400-500 words) based on these keywords: {keywords}
    Include:
    - An attention-grabbing title
    - Clear introduction
    - Main points with examples
    - Conclusion"""

    blog_content = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO blog_posts (keywords, content, timestamp) VALUES (?, ?, ?)",
        (keywords, blog_content, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return blog_content


def get_blog_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT keywords, content, timestamp FROM blog_posts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{'keywords': row[0], 'content': row[1], 'timestamp': row[2]} for row in rows]


# Task 8: Quiz Generator
def handle_quiz_generation(topic: str) -> str:
    prompt = f"""Generate 5 quiz questions about: {topic}
    For each question include:
    - The question
    - Multiple choice options (A, B, C, D)
    - The correct answer
    - A brief explanation"""

    quiz = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quizzes (topic, questions_answers, timestamp) VALUES (?, ?, ?)",
        (topic, quiz, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return quiz


def get_quiz_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT topic, questions_answers, timestamp FROM quizzes ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{'topic': row[0], 'quiz': row[1], 'timestamp': row[2]} for row in rows]


# Task 9: Sentiment Analysis
def handle_sentiment_analysis(text: str) -> str:
    prompt = f"""Analyze the sentiment of this text and provide:
    1. Overall classification (Positive/Negative/Neutral)
    2. Confidence level
    3. Key emotional indicators
    4. Brief explanation of the analysis

    Text: {text}"""

    analysis = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sentiment_analysis (text, sentiment, timestamp) VALUES (?, ?, ?)",
        (text, analysis, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return analysis


def get_sentiment_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, sentiment, timestamp FROM sentiment_analysis ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{'text': row[0], 'sentiment': row[1], 'timestamp': row[2]} for row in rows]


# Task 10: Product Review Summarizer
def handle_review_summarization(reviews: str) -> str:
    prompt = f"""Analyze and summarize these product reviews with:
    1. Overall sentiment and rating trend
    2. Key positive points
    3. Key negative points
    4. Common user experiences
    5. Notable recommendations

    Reviews:
    {reviews}"""

    summary = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO product_reviews (reviews, summary, timestamp) VALUES (?, ?, ?)",
        (reviews, summary, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return summary


def get_review_summary_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT reviews, summary, timestamp FROM product_reviews ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{'reviews': row[0], 'summary': row[1], 'timestamp': row[2]} for row in rows]


# Task 11: Course Chapter Generator
def handle_chapter_generation(description: str, subject: str, level: str) -> str:
    prompt = f"""Create a detailed course outline with the following:
    1. Course Overview
    2. Learning Objectives
    3. Detailed chapter breakdown with subsections
    4. Estimated time per chapter
    5. Recommended prerequisites

    Details:
    Description: {description}
    Subject: {subject}
    Level: {level}"""

    contents = get_chatgpt_response(prompt)

    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO course_chapters (description, subject, level, contents, timestamp) VALUES (?, ?, ?, ?, ?)",
        (description, subject, level, contents, datetime_to_str(datetime.now()))
    )
    conn.commit()
    conn.close()

    return contents


def get_course_history() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('database/ai_tasks.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT description, subject, level, contents, timestamp 
        FROM course_chapters 
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{
        'description': row[0],
        'subject': row[1],
        'level': row[2],
        'contents': row[3],
        'timestamp': row[4]
    } for row in rows]




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

        if choice == "5":
            print("\nEmail Reply Generator")
            print("1. Generate new email reply")
            print("2. View email history")
            subchoice = input("Enter your choice (1-2): ")

            if subchoice == "1":
                print("\nEnter the email you want to reply to (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                email = "\n".join(lines)

                if email:
                    print("\nGenerating reply...")
                    reply = handle_email_reply(email)
                    print("\nGenerated Reply:")
                    print(reply)
                else:
                    print("Email content cannot be empty.")

            elif subchoice == "2":
                history = get_email_history()
                if not history:
                    print("\nNo email replies found in history.")
                else:
                    print("\nEmail Reply History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nEntry {i} - {entry['timestamp']}")
                        print("\nOriginal Email:")
                        print(entry['original_email'])
                        print("\nGenerated Reply:")
                        print(entry['reply'])
                        print("-" * 50)

        if choice == "6":
            print("\nCode Snippet Generator")
            print("1. Generate new code snippet")
            print("2. View code history")
            subchoice = input("Enter your choice (1-2): ")

            if subchoice == "1":
                task = input("Enter the programming task or question:\n")
                if task:
                    print("\nGenerating code...")
                    code = handle_code_generation(task)
                    print("\nGenerated Code Solution:")
                    print(code)
                else:
                    print("Task description cannot be empty.")

            elif subchoice == "2":
                history = get_code_history()
                if not history:
                    print("\nNo code snippets found in history.")
                else:
                    print("\nCode Snippet History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nEntry {i} - {entry['timestamp']}")
                        print("Task:")
                        print(entry['task'])
                        print("\nCode Solution:")
                        print(entry['code'])
                        print("-" * 50)

        if choice == "7":
            print("\nBlog Generator")
            print("1. Generate new blog post")
            print("2. View blog history")
            subchoice = input("Enter your choice (1-2): ")

            if subchoice == "1":
                keywords = input("Enter keywords or topics for the blog post: ")
                if keywords:
                    print("\nGenerating blog post...")
                    blog = handle_blog_generation(keywords)
                    print("\nGenerated Blog Post:")
                    print(blog)
                else:
                    print("Keywords cannot be empty.")

            elif subchoice == "2":
                history = get_blog_history()
                if not history:
                    print("\nNo blog posts found in history.")
                else:
                    print("\nBlog History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nBlog {i} - {entry['timestamp']}")
                        print(f"Keywords: {entry['keywords']}")
                        print("\nContent:")
                        print(entry['content'])
                        print("-" * 50)

        if choice == "8":
            print("\nQuiz Generator")
            print("1. Generate new quiz")
            print("2. View quiz history")
            subchoice = input("Enter your choice (1-2): ")

            if subchoice == "1":
                topic = input("Enter the topic for quiz generation: ")
                if topic:
                    print("\nGenerating quiz...")
                    quiz = handle_quiz_generation(topic)
                    print("\nGenerated Quiz:")
                    print(quiz)
                else:
                    print("Topic cannot be empty.")

            elif subchoice == "2":
                history = get_quiz_history()
                if not history:
                    print("\nNo quizzes found in history.")
                else:
                    print("\nQuiz History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nQuiz {i} - {entry['timestamp']}")
                        print(f"Topic: {entry['topic']}")
                        print("\nQuestions and Answers:")
                        print(entry['quiz'])
                        print("-" * 50)

        if choice == "9":
            print("\nSentiment Analysis")
            print("1. Analyze new text")
            print("2. View analysis history")
            subchoice = input("Enter your choice (1-2): ")

            if subchoice == "1":
                print("\nEnter the text for sentiment analysis (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                text = "\n".join(lines)

                if text:
                    print("\nAnalyzing sentiment...")
                    analysis = handle_sentiment_analysis(text)
                    print("\nSentiment Analysis:")
                    print(analysis)
                else:
                    print("Text cannot be empty.")

            elif subchoice == "2":
                history = get_sentiment_history()
                if not history:
                    print("\nNo analyses found in history.")
                else:
                    print("\nAnalysis History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nAnalysis {i} - {entry['timestamp']}")
                        print("Original Text:")
                        print(entry['text'])
                        print("\nSentiment Analysis:")
                        print(entry['sentiment'])
                        print("-" * 50)

        if choice == "10":
            print("\nProduct Review Summarizer")
            print("1. Summarize new reviews")
            print("2. View summary history")
            subchoice = input("Enter your choice (1-2): ")

            if subchoice == "1":
                print("\nEnter the product reviews (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                reviews = "\n".join(lines)

                if reviews:
                    print("\nGenerating summary...")
                    summary = handle_review_summarization(reviews)
                    print("\nReview Summary:")
                    print(summary)
                else:
                    print("Reviews cannot be empty.")

            elif subchoice == "2":
                history = get_review_summary_history()
                if not history:
                    print("\nNo review summaries found in history.")
                else:
                    print("\nReview Summary History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nSummary {i} - {entry['timestamp']}")
                        print("Original Reviews:")
                        print(entry['reviews'])
                        print("\nGenerated Summary:")
                        print(entry['summary'])
                        print("-" * 50)

        if choice == "11":
            print("\nCourse Chapter Generator")
            print("1. Generate new course outline")
            print("2. View course history")
            subchoice = input("Enter your choice (1-2): ")

            if subchoice == "1":
                description = input("Enter course description: ")
                subject = input("Enter course subject: ")
                level = input("Enter course level (Beginner/Intermediate/Advanced): ")

                if description and subject and level:
                    print("\nGenerating course outline...")
                    contents = handle_chapter_generation(description, subject, level)
                    print("\nGenerated Course Outline:")
                    print(contents)
                else:
                    print("All fields are required.")

            elif subchoice == "2":
                history = get_course_history()
                if not history:
                    print("\nNo course outlines found in history.")
                else:
                    print("\nCourse History:")
                    for i, entry in enumerate(history, 1):
                        print(f"\nCourse {i} - {entry['timestamp']}")
                        print(f"Subject: {entry['subject']}")
                        print(f"Level: {entry['level']}")
                        print("\nDescription:")
                        print(entry['description'])
                        print("\nCourse Outline:")
                        print(entry['contents'])
                        print("-" * 50)





if __name__ == "__main__":
    main()