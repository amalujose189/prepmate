import streamlit as st
from groq import Groq
import json

# â”€â”€ Page config â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.set_page_config(
    page_title="PrepMate AI | Interview Coach",
    page_icon="ðŸŽ¯",
    layout="centered",
)

# â”€â”€ Custom CSS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f0f1a 100%);
    min-height: 100vh;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Title */
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 0;
}
.hero-sub {
    font-size: 0.95rem;
    color: #6b7280;
    margin-top: 4px;
    margin-bottom: 2rem;
}
.accent { color: #6ee7b7; }

/* Cards */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}

/* Question box */
.question-box {
    background: linear-gradient(135deg, rgba(110,231,183,0.08), rgba(59,130,246,0.08));
    border: 1px solid rgba(110,231,183,0.25);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    font-size: 1.05rem;
    color: #e2e8f0;
    line-height: 1.6;
}

/* Feedback sections */
.fb-strength {
    background: rgba(16,185,129,0.08);
    border-left: 3px solid #10b981;
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.5rem 0;
    color: #d1fae5;
}
.fb-gap {
    background: rgba(245,158,11,0.08);
    border-left: 3px solid #f59e0b;
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.5rem 0;
    color: #fef3c7;
}
.fb-improved {
    background: rgba(99,102,241,0.08);
    border-left: 3px solid #818cf8;
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.5rem 0;
    color: #e0e7ff;
}
.fb-score {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    text-align: center;
    padding: 0.5rem;
}

/* Stat chips */
.stat-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}
.chip {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-size: 0.78rem;
    color: #9ca3af;
}

/* Button overrides */
.stButton > button {
    background: linear-gradient(135deg, #6ee7b7, #3b82f6) !important;
    color: #0f0f1a !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Input overrides */
.stTextArea textarea, .stSelectbox select {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
label { color: #9ca3af !important; font-size: 0.85rem !important; }

/* History entry */
.hist-entry {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
.hist-q { color: #6ee7b7; font-size: 0.82rem; font-weight: 600; margin-bottom: 0.3rem; }
.hist-score { color: #f59e0b; font-family: 'Space Mono', monospace; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# â”€â”€ Session state â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if "history" not in st.session_state:
    st.session_state.history = []          # list of {role, question, score}
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "q_count" not in st.session_state:
    st.session_state.q_count = 0

# â”€â”€ Groq helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
GROQ_MODEL = "llama-3.1-8b-instant"   # Free, fast Llama 3 model on Groq

@st.cache_resource
def get_client():
    return Groq()   # Reads GROQ_API_KEY from environment automatically

def generate_question(role: str, difficulty: str, category: str) -> str:
    client = get_client()
    prompt = f"""You are an expert technical interviewer for {role} positions.
Generate ONE {difficulty}-level interview question in the category: {category}.

Rules:
- The question must be realistic and commonly asked in {role} interviews.
- Do NOT include the answer or any hints.
- Return ONLY the question text. No preamble, no numbering, no extra text.
"""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def evaluate_answer(role: str, question: str, answer: str) -> dict:
    client = get_client()
    prompt = f"""You are a senior interviewer evaluating a candidate for a {role} role.

Question asked: {question}

Candidate's answer: {answer}

Evaluate the answer and respond ONLY with a valid JSON object (no markdown, no backticks):
{{
  "score": <integer 1-10>,
  "strengths": "<2-3 sentences on what was good>",
  "gaps": "<2-3 sentences on what was missing or could improve>",
  "improved_answer": "<A concise, ideal sample answer in 3-5 sentences>"
}}
"""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    # Strip markdown fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

# â”€â”€ UI â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="hero-title">PrepMate <span class="accent">AI</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Your personal interview coach â€” powered by Groq + Llama 3</div>', unsafe_allow_html=True)

# Stats row
total = len(st.session_state.history)
avg_score = (
    round(sum(h["score"] for h in st.session_state.history) / total, 1) if total else "â€”"
)
st.markdown(f"""
<div class="stat-row">
  <div class="chip">ðŸŽ¯ Questions answered: {total}</div>
  <div class="chip">â­ Avg score: {avg_score}/10</div>
</div>
""", unsafe_allow_html=True)

# â”€â”€ Config panel â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
with st.expander("âš™ï¸ Configure your session", expanded=(st.session_state.current_question is None)):
    col1, col2, col3 = st.columns(3)
    with col1:
        role = st.selectbox("Target Role", [
            "AI/ML Engineer", "Data Analyst", "Software Engineer",
            "Data Scientist", "Backend Developer", "Full Stack Developer"
        ])
    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    with col3:
        category = st.selectbox("Category", [
            "Technical / Coding", "Machine Learning Concepts",
            "System Design", "Behavioural / HR", "SQL & Databases",
            "Python", "Statistics & Probability"
        ])

    if st.button("ðŸŽ² Generate Question", use_container_width=True):
        with st.spinner("Generating your question..."):
            q = generate_question(role, difficulty, category)
            st.session_state.current_question = q
            st.session_state.feedback = None
            st.session_state.q_count += 1
        st.rerun()

# â”€â”€ Active question â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if st.session_state.current_question:
    st.markdown(f"""
    <div class="question-box">
      <span style="font-size:0.75rem;color:#6ee7b7;font-weight:600;letter-spacing:1px;">QUESTION #{st.session_state.q_count}</span><br><br>
      {st.session_state.current_question}
    </div>
    """, unsafe_allow_html=True)

    user_answer = st.text_area(
        "Your Answer",
        height=160,
        placeholder="Type your answer here â€” think out loud, structure your thoughts...",
        key=f"answer_{st.session_state.q_count}"
    )

    col_a, col_b = st.columns([1, 1])
    with col_a:
        submit = st.button("âœ… Submit for Feedback", use_container_width=True)
    with col_b:
        skip = st.button("â­ Skip / Next Question", use_container_width=True)

    if skip:
        st.session_state.current_question = None
        st.session_state.feedback = None
        st.rerun()

    if submit:
        if not user_answer.strip():
            st.warning("Please write your answer before submitting.")
        else:
            with st.spinner("Evaluating your answer..."):
                try:
                    fb = evaluate_answer(role, st.session_state.current_question, user_answer)
                    st.session_state.feedback = fb
                    st.session_state.history.append({
                        "role": role,
                        "question": st.session_state.current_question[:80] + "...",
                        "score": fb["score"]
                    })
                except Exception as e:
                    st.error(f"Error parsing feedback: {e}")
            st.rerun()

# â”€â”€ Feedback panel â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if st.session_state.feedback:
    fb = st.session_state.feedback
    score = fb["score"]
    color = "#10b981" if score >= 7 else "#f59e0b" if score >= 4 else "#ef4444"

    st.markdown("---")
    st.markdown("### ðŸ“‹ Feedback")

    st.markdown(f'<div class="fb-score" style="color:{color}">{score}/10</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="fb-strength"><strong>âœ… Strengths</strong><br>{fb["strengths"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="fb-gap"><strong>âš ï¸ Areas to Improve</strong><br>{fb["gaps"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="fb-improved"><strong>ðŸ’¡ Ideal Answer</strong><br>{fb["improved_answer"]}</div>', unsafe_allow_html=True)

    if st.button("âž¡ï¸ Next Question", use_container_width=True):
        st.session_state.current_question = None
        st.session_state.feedback = None
        st.rerun()

# â”€â”€ History â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if st.session_state.history:
    st.markdown("---")
    st.markdown("### ðŸ“œ Session History")
    for i, h in enumerate(reversed(st.session_state.history), 1):
        score = h["score"]
        color = "#10b981" if score >= 7 else "#f59e0b" if score >= 4 else "#ef4444"
        st.markdown(f"""
        <div class="hist-entry">
          <div class="hist-q">Q{len(st.session_state.history)-i+1} Â· {h['role']}</div>
          <div style="color:#9ca3af;font-size:0.83rem;margin-bottom:0.3rem;">{h['question']}</div>
          <div class="hist-score" style="color:{color}">Score: {score}/10</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("ðŸ—‘ Clear History"):
        st.session_state.history = []
        st.session_state.current_question = None
        st.session_state.feedback = None
        st.session_state.q_count = 0
        st.rerun()


