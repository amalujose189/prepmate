import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

import streamlit as st
from groq import Groq

st.set_page_config(page_title="PrepMate AI", page_icon="P", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: "DM Sans", sans-serif; }
.stApp { background: #07090f; min-height: 100vh; }
#MainMenu, footer, header { visibility: hidden; }

.hero { padding: 2.5rem 0 1.8rem; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 2rem; }
.hero-badge { display: inline-block; font-family: "DM Mono", monospace; font-size: 0.62rem; letter-spacing: 3px; text-transform: uppercase; color: #34d399; background: rgba(52,211,153,0.08); border: 1px solid rgba(52,211,153,0.2); border-radius: 3px; padding: 0.2rem 0.75rem; margin-bottom: 1rem; }
.hero-title { font-family: "DM Mono", monospace; font-size: 2.8rem; font-weight: 400; color: #f8fafc; letter-spacing: -2px; line-height: 1; margin-bottom: 0.5rem; }
.hero-title .accent { color: #34d399; }
.hero-sub { font-size: 0.88rem; color: #475569; font-weight: 300; }

.stat-row { display: flex; gap: 0.6rem; margin-bottom: 1.8rem; flex-wrap: wrap; }
.stat-chip { font-family: "DM Mono", monospace; font-size: 0.72rem; padding: 0.32rem 0.9rem; border-radius: 5px; border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.03); color: #94a3b8; }
.stat-chip.green { color: #34d399; border-color: rgba(52,211,153,0.2); background: rgba(52,211,153,0.04); }

.question-box { background: linear-gradient(145deg, rgba(52,211,153,0.04), rgba(99,102,241,0.04)); border: 1px solid rgba(52,211,153,0.18); border-radius: 12px; padding: 1.8rem; margin: 1.2rem 0 1.6rem; line-height: 1.7; color: #f1f5f9; font-size: 1.05rem; }
.q-meta { font-family: "DM Mono", monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; color: #34d399; margin-bottom: 0.9rem; opacity: 0.85; }

.score-section { text-align: center; padding: 1.8rem 0 1.2rem; }
.score-big { font-family: "DM Mono", monospace; font-size: 4rem; font-weight: 400; line-height: 1; }
.score-denom { font-size: 1.5rem; color: #334155; }
.score-label { font-family: "DM Mono", monospace; font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase; color: #475569; margin-top: 0.4rem; }

.fb-card { border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 0.75rem; }
.fb-card.green  { background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.18); }
.fb-card.amber  { background: rgba(245,158,11,0.06);  border: 1px solid rgba(245,158,11,0.18); }
.fb-card.indigo { background: rgba(99,102,241,0.06);  border: 1px solid rgba(99,102,241,0.18); }
.fb-tag { font-family: "DM Mono", monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.5rem; font-weight: 500; }
.fb-card.green  .fb-tag { color: #34d399; }
.fb-card.amber  .fb-tag { color: #f59e0b; }
.fb-card.indigo .fb-tag { color: #818cf8; }
.fb-body { font-size: 0.9rem; color: #cbd5e1; line-height: 1.65; }

.ideal-label { font-family: "DM Mono", monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; color: #818cf8; margin-bottom: 0.6rem; font-weight: 500; }
.ideal-text { font-size: 0.9rem; color: #cbd5e1; line-height: 1.7; background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.18); border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 0.75rem; }

.hist-row { display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 0.85rem 1.1rem; margin-bottom: 0.5rem; }
.hist-role { font-family: "DM Mono", monospace; font-size: 0.6rem; letter-spacing: 1.5px; text-transform: uppercase; color: #34d399; margin-bottom: 0.2rem; }
.hist-q { font-size: 0.82rem; color: #64748b; }
.hist-badge { font-family: "DM Mono", monospace; font-size: 0.9rem; font-weight: 500; padding: 0.2rem 0.65rem; border-radius: 5px; white-space: nowrap; margin-left: 1rem; flex-shrink: 0; }

.section-title { font-family: "DM Mono", monospace; font-size: 0.65rem; letter-spacing: 2.5px; text-transform: uppercase; color: #475569; margin-bottom: 1rem; }
.hr { border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 2rem 0; }

.stButton > button { background: linear-gradient(135deg, #34d399, #6366f1) !important; color: #07090f !important; font-weight: 700 !important; border: none !important; border-radius: 8px !important; padding: 0.62rem 1.4rem !important; font-family: "DM Sans", sans-serif !important; font-size: 0.87rem !important; transition: opacity 0.15s ease !important; width: 100% !important; }
.stButton > button:hover { opacity: 0.82 !important; }
div[data-testid="column"]:nth-child(2) .stButton > button { background: transparent !important; color: #64748b !important; border: 1px solid rgba(255,255,255,0.09) !important; font-weight: 500 !important; }
div[data-testid="column"]:nth-child(2) .stButton > button:hover { color: #94a3b8 !important; border-color: rgba(255,255,255,0.18) !important; opacity: 1 !important; }

.stTextArea textarea { background: #1a1f2e !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 8px !important; color: #f1f5f9 !important; font-family: "DM Sans", sans-serif !important; font-size: 0.92rem !important; line-height: 1.65 !important; caret-color: #34d399 !important; }            
.stTextArea textarea::placeholder { color: #4a5568 !important; }
.stTextArea textarea:focus { border-color: rgba(52,211,153,0.4) !important; box-shadow: 0 0 0 3px rgba(52,211,153,0.06) !important; }

div[data-baseweb="select"] > div { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 8px !important; }
div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: #cbd5e1 !important; background: transparent !important; font-family: "DM Sans", sans-serif !important; }
ul[data-baseweb="menu"], div[data-baseweb="popover"] { background: #0f1117 !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 8px !important; }
li[role="option"], div[role="option"] { background: #0f1117 !important; color: #94a3b8 !important; font-size: 0.88rem !important; }
li[role="option"]:hover, div[role="option"]:hover { background: rgba(52,211,153,0.08) !important; color: #34d399 !important; }
li[aria-selected="true"], div[aria-selected="true"] { background: rgba(52,211,153,0.1) !important; color: #34d399 !important; }
div[data-baseweb="select"] svg { fill: #475569 !important; }
label { color: #475569 !important; font-size: 0.78rem !important; }
.streamlit-expanderHeader { background: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 8px !important; color: #64748b !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

defaults = {
    "history": [], "current_question": None, "feedback": None,
    "q_count": 0, "role": "AI/ML Engineer",
    "difficulty": "Easy", "category": "Technical / Coding",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

GROQ_MODEL = "llama-3.1-8b-instant"

def make_client():
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        st.error("GROQ_API_KEY not found. Run: $env:GROQ_API_KEY = 'gsk_...'")
        st.stop()
    return Groq(api_key=key)

def generate_question(role, difficulty, category):
    client = make_client()
    prompt = (
        f"You are an expert technical interviewer for {role} positions.\n"
        f"Generate ONE {difficulty}-level interview question for the category: {category}.\n\n"
        "Rules:\n"
        "- Must be realistic and commonly asked in real interviews.\n"
        "- Do NOT include the answer or hints.\n"
        "- Return ONLY the question text. No preamble, no numbering, no extra text."
    )
    r = client.chat.completions.create(
        model=GROQ_MODEL, max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content.strip()

def evaluate_answer(role, question, answer):
    client = make_client()

    score_prompt = (
        f"You are a strict senior interviewer for a {role} role.\n\n"
        f"Question: {question}\n"
        f"Candidate answer: {answer}\n\n"
        "SCORING RUBRIC - apply strictly:\n"
        "1  = Completely wrong, gibberish, or blank.\n"
        "2  = Mentions topic but no real explanation.\n"
        "3  = Major misunderstandings, mostly incorrect.\n"
        "4  = Partial understanding, key parts missing.\n"
        "5  = Basic understanding, incomplete implementation.\n"
        "6  = Correct approach, moderate detail, minor gaps.\n"
        "7  = Good answer, covers main points, small omissions.\n"
        "8  = Strong, well-structured, covers edge cases.\n"
        "9  = Excellent, comprehensive, production-quality.\n"
        "10 = Perfect, nothing to improve.\n\n"
        "A working correct code solution with proper logic scores at least 7.\n"
        "Do NOT penalize for minor style issues if logic is correct.\n\n"
        "Reply ONLY with this exact JSON (no markdown, no extra text):\n"
        '{"score":<integer>,"strengths":"<2-3 sentences>","gaps":"<2-3 sentences>"}'
    )
    r1 = client.chat.completions.create(
        model=GROQ_MODEL, max_tokens=400, temperature=0,
        messages=[{"role": "user", "content": score_prompt}]
    )
    raw1 = r1.choices[0].message.content.strip()
    raw1 = raw1.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw1)
    except Exception:
        score_m = re.search(r'"score"\s*:\s*(\d+)', raw1)
        str_m   = re.search(r'"strengths"\s*:\s*"(.*?)"', raw1, re.DOTALL)
        gap_m   = re.search(r'"gaps"\s*:\s*"(.*?)"', raw1, re.DOTALL)
        parsed = {
            "score":     int(score_m.group(1)) if score_m else 5,
            "strengths": str_m.group(1).strip() if str_m else "Good attempt.",
            "gaps":      gap_m.group(1).strip() if gap_m else "Review your answer.",
        }

    ideal_prompt = (
        f"You are a senior {role} interviewer.\n\n"
        f"Question: {question}\n\n"
        "Write the ideal answer to this question.\n"
        "- If code is needed, write clean, correct, well-commented Python.\n"
        "- Include a brief explanation before or after the code.\n"
        "- Do NOT wrap in JSON.\n"
        "- Do NOT use markdown headers.\n"
        "- Write directly as if explaining to a candidate."
    )
    r2 = client.chat.completions.create(
        model=GROQ_MODEL, max_tokens=900,
        messages=[{"role": "user", "content": ideal_prompt}]
    )
    parsed["improved_answer"] = r2.choices[0].message.content.strip()
    return parsed

def render_ideal_answer(text):
    st.markdown('<div class="ideal-label">Ideal Answer</div>', unsafe_allow_html=True)
    parts = re.split(r'```(?:python)?\n?', text)
    if len(parts) == 1:
        code_signals = ["def ", "import ", "return ", "for ", "class ", "print("]
        if any(s in text for s in code_signals):
            st.code(text, language="python")
        else:
            st.markdown(f'<div class="ideal-text">{text}</div>', unsafe_allow_html=True)
    else:
        for i, part in enumerate(parts):
            part = part.strip("`\n ")
            if not part:
                continue
            if i % 2 == 1:
                st.code(part, language="python")
            else:
                st.markdown(f'<div class="ideal-text">{part}</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-badge">AI Interview Coach</div>
  <div class="hero-title">Prep<span class="accent">Mate</span></div>
  <div class="hero-sub">Powered by Groq &amp; Llama 3.1 - Practice smarter. Get hired faster.</div>
</div>
""", unsafe_allow_html=True)

total = len(st.session_state.history)
avg   = round(sum(h["score"] for h in st.session_state.history) / total, 1) if total else 0
st.markdown(f"""
<div class="stat-row">
  <div class="stat-chip">Questions answered: {total}</div>
  <div class="stat-chip green">Avg score: {avg} / 10</div>
</div>
""", unsafe_allow_html=True)

ROLES        = ["AI/ML Engineer","Data Analyst","Software Engineer","Data Scientist","Backend Developer","Full Stack Developer"]
DIFFICULTIES = ["Easy","Medium","Hard"]
CATEGORIES   = ["Technical / Coding","Machine Learning Concepts","System Design","Behavioural / HR","SQL & Databases","Python","Statistics & Probability"]

with st.expander("Configure your session", expanded=(st.session_state.current_question is None)):
    c1, c2, c3 = st.columns(3)
    role       = c1.selectbox("Target Role",  ROLES,        index=ROLES.index(st.session_state.role))
    difficulty = c2.selectbox("Difficulty",   DIFFICULTIES, index=DIFFICULTIES.index(st.session_state.difficulty))
    category   = c3.selectbox("Category",     CATEGORIES,   index=CATEGORIES.index(st.session_state.category))
    st.session_state.role       = role
    st.session_state.difficulty = difficulty
    st.session_state.category   = category

    if st.button("Generate Question", use_container_width=True):
        with st.spinner("Generating question..."):
            try:
                q = generate_question(role, difficulty, category)
                st.session_state.current_question = q
                st.session_state.feedback = None
                st.session_state.q_count += 1
            except Exception as ex:
                st.error(f"Error: {ex}")
        st.rerun()

if st.session_state.current_question:
    st.markdown(f"""
    <div class="question-box">
      <div class="q-meta">
        Question #{st.session_state.q_count} &nbsp;&bull;&nbsp;
        {st.session_state.difficulty} &nbsp;&bull;&nbsp;
        {st.session_state.category}
      </div>
      {st.session_state.current_question}
    </div>
    """, unsafe_allow_html=True)

    answer = st.text_area(
        "Your Answer",
        height=180,
        placeholder="",
        key=f"ans_{st.session_state.q_count}"
    )
    st.markdown("""
    <script>
    var textareas = window.parent.document.querySelectorAll('textarea');
    textareas.forEach(function(el) {
        el.setAttribute('autocomplete', 'off');
        el.setAttribute('autocorrect', 'off');
        el.setAttribute('autocapitalize', 'off');
        el.setAttribute('spellcheck', 'false');
    });
    </script>
    """, unsafe_allow_html=True)
    ca, cb = st.columns(2)
    submit = ca.button("Submit for Feedback", use_container_width=True)
    skip   = cb.button("Skip / Next Question", use_container_width=True)

    if skip:
        st.session_state.current_question = None
        st.session_state.feedback = None
        st.rerun()

    if submit:
        if not answer.strip():
            st.warning("Please write your answer before submitting.")
        else:
            with st.spinner("Evaluating your answer..."):
                try:
                    fb = evaluate_answer(
                        st.session_state.role,
                        st.session_state.current_question,
                        answer
                    )
                    st.session_state.feedback = fb
                    st.session_state.history.append({
                        "role":     st.session_state.role,
                        "question": st.session_state.current_question[:80] + "...",
                        "score":    fb["score"]
                    })
                except Exception as ex:
                    st.error(f"Evaluation error: {ex}")
            st.rerun()

if st.session_state.feedback:
    fb    = st.session_state.feedback
    score = fb["score"]
    color = "#10b981" if score >= 7 else "#f59e0b" if score >= 4 else "#ef4444"

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Feedback</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-section">
      <div class="score-big" style="color:{color}">
        {score}<span class="score-denom"> / 10</span>
      </div>
      <div class="score-label">Your Score</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="fb-card green">
      <div class="fb-tag">Strengths</div>
      <div class="fb-body">{fb["strengths"]}</div>
    </div>
    <div class="fb-card amber">
      <div class="fb-tag">Areas to Improve</div>
      <div class="fb-body">{fb["gaps"]}</div>
    </div>
    """, unsafe_allow_html=True)

    render_ideal_answer(fb["improved_answer"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next Question", use_container_width=True):
        with st.spinner("Generating next question..."):
            try:
                q = generate_question(
                    st.session_state.role,
                    st.session_state.difficulty,
                    st.session_state.category
                )
                st.session_state.current_question = q
                st.session_state.feedback = None
                st.session_state.q_count += 1
            except Exception as ex:
                st.error(f"Error: {ex}")
        st.rerun()

if st.session_state.history:
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Session History</div>', unsafe_allow_html=True)

    for i, h in enumerate(reversed(st.session_state.history), 1):
        sc  = h["score"]
        clr = "#10b981" if sc >= 7 else "#f59e0b" if sc >= 4 else "#ef4444"
        bg  = "rgba(16,185,129,0.1)" if sc >= 7 else "rgba(245,158,11,0.1)" if sc >= 4 else "rgba(239,68,68,0.1)"
        idx = len(st.session_state.history) - i + 1
        st.markdown(f"""
        <div class="hist-row">
          <div>
            <div class="hist-role">Q{idx} &nbsp;&bull;&nbsp; {h["role"]}</div>
            <div class="hist-q">{h["question"]}</div>
          </div>
          <div class="hist-badge" style="color:{clr}; background:{bg}">{sc}/10</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Clear History"):
        for k in ["history", "current_question", "feedback"]:
            st.session_state[k] = [] if k == "history" else None
        st.session_state.q_count = 0
        st.rerun()