import streamlit as st
import logging
import sys
import os

# ── page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="VideoMind AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── inject CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── global reset ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0d0d12;
    color: #e8e6f0;
}
.stApp { background-color: #0d0d12; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

/* ── hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── hero wordmark ── */
.hero {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin-bottom: 0.2rem;
    margin-top: 0.5rem;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #ffffff;
    line-height: 1;
}
.hero-accent {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #7c5cfc;
    line-height: 1;
}
.hero-sub {
    font-size: 0.95rem;
    color: #7a7890;
    margin-bottom: 2rem;
    letter-spacing: 0.01em;
}

/* ── input card ── */
.input-card {
    background: #16151f;
    border: 1px solid #2a2838;
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
}

/* ── pipeline progress ── */
.pipeline-wrap {
    display: flex;
    align-items: flex-start;
    gap: 0;
    margin: 1.8rem 0 2rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
}
.pipeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    min-width: 90px;
    position: relative;
}
.pipeline-step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px;
    left: calc(50% + 20px);
    width: calc(100% - 40px);
    height: 2px;
    background: #2a2838;
    z-index: 0;
}
.pipeline-step.done:not(:last-child)::after { background: #7c5cfc; }
.pipeline-step.active:not(:last-child)::after { background: #2a2838; }

.step-dot {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    z-index: 1;
    border: 2px solid #2a2838;
    background: #0d0d12;
    color: #3a3850;
    transition: all 0.3s;
}
.pipeline-step.done .step-dot {
    background: #7c5cfc;
    border-color: #7c5cfc;
    color: #fff;
}
.pipeline-step.active .step-dot {
    background: #0d0d12;
    border-color: #7c5cfc;
    color: #7c5cfc;
    box-shadow: 0 0 12px #7c5cfc55;
    animation: pulse-border 1.4s infinite;
}
@keyframes pulse-border {
    0%,100% { box-shadow: 0 0 6px #7c5cfc55; }
    50%      { box-shadow: 0 0 18px #7c5cfcbb; }
}
.step-label {
    font-size: 0.68rem;
    margin-top: 6px;
    text-align: center;
    color: #4a4860;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-weight: 600;
    max-width: 80px;
}
.pipeline-step.done .step-label  { color: #a393fc; }
.pipeline-step.active .step-label { color: #7c5cfc; }

/* ── result cards ── */
.result-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-top: 1.5rem; }
.result-card {
    background: #16151f;
    border: 1px solid #2a2838;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
}
.result-card.full { grid-column: 1 / -1; }
.card-label {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7c5cfc;
    font-weight: 700;
    margin-bottom: 0.6rem;
    font-family: 'Space Mono', monospace;
}
.card-body { font-size: 0.92rem; color: #c8c6d8; line-height: 1.65; }
.card-title { font-size: 1.3rem; font-weight: 600; color: #ffffff; line-height: 1.3; }

/* ── bullet items ── */
.item-list { list-style: none; padding: 0; margin: 0; }
.item-list li {
    display: flex;
    gap: 0.6rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid #1e1d2a;
    font-size: 0.88rem;
    color: #c8c6d8;
    line-height: 1.5;
}
.item-list li:last-child { border-bottom: none; }
.item-bullet {
    flex-shrink: 0;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #7c5cfc;
    margin-top: 7px;
}

/* ── chat section ── */
.chat-wrap {
    background: #16151f;
    border: 1px solid #2a2838;
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    margin-top: 2rem;
}
.chat-header {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7c5cfc;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    margin-bottom: 1rem;
}
.msg-user {
    background: #1e1d2e;
    border: 1px solid #2e2c42;
    border-radius: 8px 8px 4px 8px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    color: #e8e6f0;
    text-align: right;
}
.msg-ai {
    background: #12111a;
    border: 1px solid #24222e;
    border-left: 3px solid #7c5cfc;
    border-radius: 4px 8px 8px 8px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    color: #c8c6d8;
    line-height: 1.6;
}
.chat-empty {
    text-align: center;
    color: #3a3850;
    font-size: 0.88rem;
    padding: 1.5rem 0;
    font-style: italic;
}

/* ── status badge ── */
.status-badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.badge-processing { background: #1e1428; color: #a383fc; border: 1px solid #5a3adc; }
.badge-done       { background: #121e18; color: #4cca8e; border: 1px solid #2a8c5a; }
.badge-error      { background: #1e1218; color: #fc6363; border: 1px solid #8c2a2a; }

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0d0d12 !important;
    border: 1px solid #2a2838 !important;
    border-radius: 8px !important;
    color: #e8e6f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c5cfc !important;
    box-shadow: 0 0 0 2px #7c5cfc33 !important;
}
.stButton > button {
    background: #7c5cfc !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 0.55rem 1.4rem !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #6a4ae8 !important; }
.stButton > button:disabled { background: #2a2838 !important; color: #4a4860 !important; }

div[data-testid="stExpander"] {
    background: #16151f;
    border: 1px solid #2a2838 !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary {
    color: #a393fc !important;
    font-size: 0.88rem;
}

hr { border-color: #2a2838 !important; margin: 1.5rem 0 !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0d0d12; }
::-webkit-scrollbar-thumb { background: #2a2838; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── logging setup ─────────────────────────────────────────────────────────
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ── pipeline step definitions ─────────────────────────────────────────────
STEPS = [
    ("01", "Load Input"),
    ("02", "Transcribe"),
    ("03", "Summarise"),
    ("04", "Extract"),
    ("05", "Build RAG"),
]


def render_pipeline(current: int):
    """Render the horizontal pipeline progress bar."""
    html = '<div class="pipeline-wrap">'
    for i, (num, label) in enumerate(STEPS):
        if i < current:
            cls = "done"
            icon = "✓"
        elif i == current:
            cls = "active"
            icon = num
        else:
            cls = ""
            icon = num
        html += f"""
        <div class="pipeline-step {cls}">
            <div class="step-dot">{icon}</div>
            <div class="step-label">{label}</div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_bullet_list(items):
    if not items:
        return '<p class="card-body" style="color:#4a4860;font-style:italic;">None identified.</p>'
    html = '<ul class="item-list">'
    for item in items:
        item = item.strip().lstrip("-•·*").strip()
        if item:
            html += f'<li><span class="item-bullet"></span>{item}</li>'
    html += "</ul>"
    return html


def parse_list(raw):
    """Turn a string or list into a Python list of strings."""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        return lines
    return []


# ── session state defaults ─────────────────────────────────────────────────
defaults = {
    "pipeline_done": False,
    "pipeline_step": -1,   # -1 = idle
    "result": None,
    "chat_history": [],
    "error": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <span class="hero-title">Video</span>
    <span class="hero-accent">Mind</span>
</div>
<p class="hero-sub">Drop a YouTube URL or a local audio file — get a full transcript, smart summary, and a Q&A chat in seconds.</p>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  INPUT CARD
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="input-card">', unsafe_allow_html=True)
source = st.text_input(
    label="Source",
    placeholder="https://youtube.com/watch?v=…   or   /path/to/audio.mp3",
    label_visibility="collapsed",
)
col_btn, col_status = st.columns([1, 4])
with col_btn:
    run_btn = st.button("Analyse →", disabled=st.session_state.pipeline_step >= 0 and not st.session_state.pipeline_done)
st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PIPELINE TRIGGER
# ══════════════════════════════════════════════════════════════════
if run_btn and source.strip():
    # Reset
    st.session_state.pipeline_done = False
    st.session_state.result = None
    st.session_state.chat_history = []
    st.session_state.error = None
    st.session_state.pipeline_step = 0

    pipeline_ph = st.empty()
    status_ph   = st.empty()

    def update_ui(step: int, msg: str):
        with pipeline_ph.container():
            render_pipeline(step)
        status_ph.markdown(
            f'<span class="status-badge badge-processing">⚙ {msg}</span>',
            unsafe_allow_html=True,
        )

    try:
        # ── Step 0: Load / chunk ──────────────────────────────────────────
        update_ui(0, "Loading & chunking input…")
        from utils.audio_processor import process_input
        chunks = process_input(source.strip())

        # ── Step 1: Transcribe ────────────────────────────────────────────
        update_ui(1, "Transcribing audio…")
        from core.transcriber import transcribe_all
        transcript = transcribe_all(chunks, translate=True)

        # ── Step 2: Summarise ─────────────────────────────────────────────
        update_ui(2, "Summarising & generating title…")
        from core.summarize import summmarize, generate_title
        title   = generate_title(transcript)
        summary = summmarize(transcript)

        # ── Step 3: Extract ───────────────────────────────────────────────
        update_ui(3, "Extracting action items, decisions & questions…")
        from core.extractor import extract_action_items, extract_key_decisions, extract_questions
        action_items   = extract_action_items(transcript)
        key_decisions  = extract_key_decisions(transcript)
        questions      = extract_questions(transcript)

        # ── Step 4: Build RAG ─────────────────────────────────────────────
        update_ui(4, "Building Q&A engine…")
        from core.rag_engine import build_rag_chain
        rag_chain = build_rag_chain(transcript)

        # ── Done ──────────────────────────────────────────────────────────
        st.session_state.result = {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": parse_list(action_items),
            "key_decisions": parse_list(key_decisions),
            "questions": parse_list(questions),
            "rag_chain": rag_chain,
        }
        st.session_state.pipeline_done = True
        st.session_state.pipeline_step = len(STEPS)

        status_ph.markdown(
            '<span class="status-badge badge-done">✓ Analysis complete</span>',
            unsafe_allow_html=True,
        )
        with pipeline_ph.container():
            render_pipeline(len(STEPS))   # all done

    except FileNotFoundError as e:
        st.session_state.error = f"File not found: {e}"
        st.session_state.pipeline_done = True
    except ValueError as e:
        st.session_state.error = f"Invalid input: {e}"
        st.session_state.pipeline_done = True
    except Exception as e:
        logging.exception("Unhandled exception in Streamlit pipeline")
        st.session_state.error = f"{type(e).__name__}: {e}"
        st.session_state.pipeline_done = True

elif source.strip() == "" and run_btn:
    st.warning("Please enter a YouTube URL or file path first.")

# ══════════════════════════════════════════════════════════════════
#  SHOW PIPELINE STATE (persistent between reruns)
# ══════════════════════════════════════════════════════════════════
if st.session_state.pipeline_step == len(STEPS) and st.session_state.pipeline_done:
    render_pipeline(len(STEPS))
    st.markdown('<span class="status-badge badge-done">✓ Analysis complete</span>', unsafe_allow_html=True)
elif st.session_state.error:
    render_pipeline(st.session_state.pipeline_step if st.session_state.pipeline_step >= 0 else 0)
    st.markdown(
        f'<span class="status-badge badge-error">✗ {st.session_state.error}</span>',
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════
if st.session_state.result:
    r = st.session_state.result
    st.markdown("<hr>", unsafe_allow_html=True)

    # Title + summary
    st.markdown(f"""
    <div class="result-grid">
        <div class="result-card full">
            <div class="card-label">Title</div>
            <div class="card-title">{r['title']}</div>
        </div>
        <div class="result-card full">
            <div class="card-label">Summary</div>
            <div class="card-body">{r['summary']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Three-column extractions
    st.markdown(f"""
    <div class="result-grid" style="grid-template-columns:1fr 1fr 1fr; margin-top:1.2rem;">
        <div class="result-card">
            <div class="card-label">Action Items</div>
            {render_bullet_list(r['action_items'])}
        </div>
        <div class="result-card">
            <div class="card-label">Key Decisions</div>
            {render_bullet_list(r['key_decisions'])}
        </div>
        <div class="result-card">
            <div class="card-label">Open Questions</div>
            {render_bullet_list(r['questions'])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Transcript expander
    with st.expander("📄  Full Transcript"):
        st.text_area(
            label="",
            value=r["transcript"],
            height=300,
            label_visibility="collapsed",
        )

    # ── Chat ─────────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">💬  Ask the transcript</div>', unsafe_allow_html=True)

    # Render history
    if st.session_state.chat_history:
        msgs_html = ""
        for role, text in st.session_state.chat_history:
            if role == "user":
                msgs_html += f'<div class="msg-user">{text}</div>'
            else:
                msgs_html += f'<div class="msg-ai">{text}</div>'
        st.markdown(msgs_html, unsafe_allow_html=True)
    else:
        st.markdown('<p class="chat-empty">Ask anything about the video…</p>', unsafe_allow_html=True)

    # Input row
    q_col, send_col = st.columns([5, 1])
    with q_col:
        user_query = st.text_input(
            "Query",
            placeholder="What were the main takeaways?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with send_col:
        send_btn = st.button("Send")

    if send_btn and user_query.strip():
        from core.rag_engine import ask_question
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_query.strip())
        st.session_state.chat_history.append(("user", user_query.strip()))
        st.session_state.chat_history.append(("ai", answer))
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)