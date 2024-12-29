# AI Task Assistant 🤖

A versatile Python application that leverages OpenAI's GPT models to perform various AI-powered tasks. This tool helps automate and enhance different aspects of content creation, analysis, and management.

## Features 🌟

### FAQ System
- Generate professional answers to common questions.
- Store Q&A history for future reference.

### Content Summarizer
- Summarize long texts efficiently.
- Maintain a database of summaries.

### Daily Journal with AI Reflection
- Record journal entries.
- Get AI-powered reflections and insights.

### Idea Generator
- Generate creative ideas for any topic.
- Search through past ideas.

### Email Reply Generator
- Create professional email responses.
- Store email correspondence history.

### Code Snippet Generator
- Generate code solutions for programming tasks.
- Include documentation and examples.

### Blog Generator
- Create blog posts from keywords.
- Store and manage blog content.

### Quiz Generator
- Generate quiz questions and answers.
- Track quiz history.

### Sentiment Analysis
- Analyze text sentiment.
- Store analysis results.

### Product Review Summarizer
- Summarize multiple product reviews.
- Extract key insights.

### Course Chapter Generator
- Create course outlines.
- Generate detailed chapter contents.

## Setup Instructions 🚀

### Prerequisites
- Python 3.8 or higher.
- SQLite3.
- OpenAI API key.

### Installation Steps

#### Clone the Repository
```bash
git clone https://github.com/yourusername/ai-task-assistant.git
cd ai_assignments
```

#### Create Virtual Environment
```bash
python -m venv venv

# For Windows
venv\Scripts\activate

# For macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Set Up OpenAI API Key
Replace the API key in the code with your OpenAI API key:
```python
client = OpenAI(api_key="your-api-key-here")
```

#### Initialize Database
```bash
python app.py
```

## Usage 💡

1. Run the application:
    ```bash
    python main.py
    ```
2. Choose from the available options (1-11).
3. Follow the prompts to use each feature.
4. View the history of previous generations when needed.

## Database Structure 📁
The application uses SQLite to store:
- FAQ entries
- Content summaries
- Journal entries
- Generated ideas
- Email responses
- Code snippets
- Blog posts
- Quiz questions
- Sentiment analyses
- Product reviews
- Course chapters

## Project Structure 📂
```plaintext
ai-task-assistant/
├── main.py
├── requirements.txt
├── README.md
├── database/
│   └── ai_tasks.db
└── .gitignore
```

## Error Handling 🛠️
The application includes error handling for:
- Database operations.
- API calls.
- User input validation.
- File operations.
