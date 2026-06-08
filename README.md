# PrepMate AI

An AI-powered interview prep tool I built to help students (including myself) actually practice answering interview questions instead of just reading theory.

---

## Why I built this

Honestly, I kept reading interview prep stuff but never actually *practicing*. I'd go blank in real interviews because I never trained myself to put answers into words under pressure. So I built PrepMate — pick a role, get a question, write your answer, and get real feedback on it. Simple idea, but it actually helps.

---

## What it does

- Generates interview questions based on your target role, difficulty, and category
- You type your answer in a text box
- It evaluates your answer and gives you a score out of 10
- Shows what you did well, what you missed, and shows an ideal answer
- Keeps track of your scores during the session so you can see improvement
- Once you finish a question, next question loads in the same category — no need to reconfigure

---

## Tech used

- Python + Streamlit for the UI
- Groq API with llama-3.1-8b-instant as the LLM
- python-dotenv for managing the API key

---

## How to run it locally

**Step 1 — Clone the repo**
```bash
git clone https://github.com/amalujose189/prepmate.git
cd prepmate
```

**Step 2 — Create a virtual environment**
```bash
python -m venv env
```

Activate it:
- Windows: `.\env\Scripts\Activate.ps1`
- Mac/Linux: `source env/bin/activate`

**Step 3 — Install the packages**
```bash
pip install streamlit groq python-dotenv
```

**Step 4 — Add your Groq API key**

Create a file called `.env` in the project folder and add:
```
GROQ_API_KEY=your_key_here
```

You can get a free key at https://console.groq.com

Or just set it directly in PowerShell if you're on Windows:
```powershell
$env:GROQ_API_KEY = "your_key_here"
```

**Step 5 — Run it**
```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## Folder structure

```
prepmate/
├── app.py            # everything is here — UI, API calls, logic
├── .env              # your API key (not pushed to git)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Roles and categories supported

Roles: AI/ML Engineer, Data Scientist, Software Engineer, Data Analyst, Backend Developer, Full Stack Developer

Categories: Technical/Coding, Machine Learning, System Design, SQL, Python, Behavioural, Statistics

---

## Stuff I ran into while building this

- The model kept returning code inside JSON which would break the JSON parser completely. Took a while to figure out — ended up splitting it into two separate API calls, one for the score/feedback and one for the ideal answer as plain text
- Scoring was inconsistent — same answer would get different scores on different runs. Fixed it by setting temperature=0 and seed=42 on the scoring call
- On Windows the emoji characters were all corrupted because the file wasn't saved as UTF-8. Had to rewrite the whole file explicitly in UTF-8
- Streamlit's dropdown components use BaseWeb internally so normal CSS doesn't reach them — had to target `data-baseweb` attributes directly

---

## Note

Keep your `.env` file out of git. The `.gitignore` already handles this but just double check before pushing.

---

Made by Amalu Jose
