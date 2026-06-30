import streamlit as st
import logging

# ── page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VideoMind AI",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Aurora CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* ── base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #060610;
    color: #ddd8f8;
}
.stApp { background-color: #060610; }
.block-container { padding: 2.5rem 3.5rem 5rem; max-width: 1140px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── ambient aurora orbs (fixed, behind everything) ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -120px; left: -100px;
    width: 520px; height: 520px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(109,40,217,0.18) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -80px; right: -60px;
    width: 420px; height: 420px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(13,148,136,0.15) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── hero ── */
.hero {
    margin: 0.5rem 0 0.3rem;
    display: flex;
    align-items: baseline;
    gap: 0;
}
.hero-word {
    font-family: 'Space Mono', monospace;
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1;
}
.hero-video { color: #a78bfa; }
.hero-mind  {
    background: linear-gradient(90deg, #a78bfa 0%, #2dd4bf 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-badge {
    display: inline-block;
    margin-left: 0.9rem;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace;
    background: rgba(167,139,250,0.12);
    border: 1px solid rgba(167,139,250,0.3);
    color: #a78bfa;
    vertical-align: middle;
    position: relative;
    top: -4px;
}
.hero-sub {
    font-size: 0.9rem;
    color: #5a527a;
    margin: 0.45rem 0 2rem;
    font-weight: 400;
    letter-spacing: 0.01em;
}

/* ── input card ── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(167,139,250,0.15);
    border-radius: 16px;
    padding: 1.8rem 2rem 1.4rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.5), rgba(45,212,191,0.4), transparent);
}

/* ── pipeline ── */
.pipeline-wrap {
    display: flex;
    align-items: flex-start;
    gap: 0;
    margin: 1.6rem 0 1.8rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
}
.pipeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    min-width: 95px;
    position: relative;
}
.pipeline-step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px;
    left: calc(50% + 20px);
    width: calc(100% - 40px);
    height: 1.5px;
    background: rgba(255,255,255,0.07);
    z-index: 0;
}
.pipeline-step.done:not(:last-child)::after {
    background: linear-gradient(90deg, #7c3aed, #0d9488);
}
.step-dot {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem; font-weight: 700;
    font-family: 'Space Mono', monospace;
    z-index: 1;
    border: 1.5px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    color: #2a2250;
    transition: all 0.3s ease;
}
.pipeline-step.done .step-dot {
    background: linear-gradient(135deg, #7c3aed, #0d9488);
    border-color: transparent;
    color: #fff;
    box-shadow: 0 0 14px rgba(124,58,237,0.45);
}
.pipeline-step.active .step-dot {
    background: rgba(167,139,250,0.08);
    border-color: #a78bfa;
    color: #a78bfa;
    animation: aurora-pulse 1.6s ease-in-out infinite;
}
@keyframes aurora-pulse {
    0%,100% { box-shadow: 0 0 8px rgba(167,139,250,0.3), 0 0 0 0 rgba(167,139,250,0.15); }
    50%      { box-shadow: 0 0 20px rgba(167,139,250,0.6), 0 0 0 6px rgba(167,139,250,0.05); }
}
.step-label {
    font-size: 0.63rem;
    margin-top: 6px;
    text-align: center;
    color: #2a2250;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-weight: 600;
    max-width: 85px;
}
.pipeline-step.done .step-label  { color: #7c6fc0; }
.pipeline-step.active .step-label { color: #a78bfa; }

/* ── divider ── */
.aurora-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.2), rgba(45,212,191,0.15), transparent);
    margin: 1.8rem 0;
    border: none;
}

/* ── result cards ── */
.result-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.2rem; }
.result-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: rgba(167,139,250,0.25); }
.result-card.full { grid-column: 1 / -1; }
.result-card.accent-purple::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, #7c3aed, rgba(167,139,250,0.3), transparent);
}
.result-card.accent-teal::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, #0d9488, rgba(45,212,191,0.3), transparent);
}
.card-label {
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.65rem;
    font-family: 'Space Mono', monospace;
}
.label-purple { color: #a78bfa; }
.label-teal   { color: #2dd4bf; }
.card-body  { font-size: 0.9rem; color: #9d97c0; line-height: 1.7; }
.card-title { font-size: 1.25rem; font-weight: 600; color: #f0ecff; line-height: 1.35; }

/* ── bullet list ── */
.item-list { list-style: none; padding: 0; margin: 0; }
.item-list li {
    display: flex; gap: 0.65rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.87rem; color: #9d97c0; line-height: 1.55;
}
.item-list li:last-child { border-bottom: none; }
.bullet-purple { flex-shrink:0; width:5px; height:5px; border-radius:50%; background:#a78bfa; margin-top:8px; }
.bullet-teal   { flex-shrink:0; width:5px; height:5px; border-radius:50%; background:#2dd4bf; margin-top:8px; }

/* ── chat ── */
.chat-wrap {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-top: 1.8rem;
    position: relative;
    overflow: hidden;
}
.chat-wrap::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), rgba(45,212,191,0.3), transparent);
}
.chat-header {
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #a78bfa;
    font-weight: 600;
    font-family: 'Space Mono', monospace;
    margin-bottom: 1.2rem;
}
.msg-user {
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 12px 12px 3px 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.7rem;
    font-size: 0.88rem; color: #ddd8f8;
    text-align: right;
}
.msg-ai {
    background: rgba(13,148,136,0.07);
    border: 1px solid rgba(45,212,191,0.15);
    border-left: 2px solid #2dd4bf;
    border-radius: 3px 12px 12px 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.7rem;
    font-size: 0.88rem; color: #9d97c0; line-height: 1.65;
}
.chat-empty {
    text-align: center; color: #2a2250;
    font-size: 0.86rem; padding: 1.8rem 0; font-style: italic;
}

/* ── status badge ── */
.status-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.28rem 0.75rem;
    border-radius: 20px;
    font-size: 0.68rem; font-weight: 600;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.08em; text-transform: uppercase;
}
.badge-processing {
    background: rgba(167,139,250,0.1);
    color: #c4b5fd;
    border: 1px solid rgba(167,139,250,0.3);
}
.badge-done {
    background: rgba(45,212,191,0.08);
    color: #2dd4bf;
    border: 1px solid rgba(45,212,191,0.25);
}
.badge-error {
    background: rgba(239,68,68,0.08);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.2);
}

/* ── Streamlit overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    border-radius: 10px !important;
    color: #ddd8f8 !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(167,139,250,0.6) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.08) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #2a2250 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #0d9488) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 0.55rem 1.5rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 2px 16px rgba(124,58,237,0.3) !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled {
    background: rgba(255,255,255,0.05) !important;
    color: #2a2250 !important;
    box-shadow: none !important;
}
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary { color: #a78bfa !important; font-size: 0.88rem; }
.stSpinner > div { border-top-color: #a78bfa !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.2); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# ── pipeline steps ─────────────────────────────────────────────────────────
STEPS = [
    ("01", "Load"),
    ("02", "Transcribe"),
    ("03", "Summarise"),
    ("04", "Extract"),
    ("05", "Build RAG"),
]


def render_pipeline(current: int):
    html = '<div class="pipeline-wrap">'
    for i, (num, label) in enumerate(STEPS):
        if i < current:
            cls, icon = "done", "✓"
        elif i == current:
            cls, icon = "active", num
        else:
            cls, icon = "", num
        html += f"""
        <div class="pipeline-step {cls}">
            <div class="step-dot">{icon}</div>
            <div class="step-label">{label}</div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_bullet_list(items, bullet_class="bullet-purple"):
    if not items:
        return '<p class="card-body" style="color:#2a2250;font-style:italic;">None identified.</p>'
    html = '<ul class="item-list">'
    for item in items:
        item = item.strip().lstrip("-•·*").strip()
        if item:
            html += f'<li><span class="{bullet_class}"></span>{item}</li>'
    html += "</ul>"
    return html


def parse_list(raw):
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        return [l.strip() for l in raw.split("\n") if l.strip()]
    return []


# ── session state ──────────────────────────────────────────────────────────
for k, v in {"pipeline_done": False, "pipeline_step": -1, "result": None,
              "chat_history": [], "error": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <span class="hero-word hero-video">Video</span><span class="hero-word hero-mind">Mind</span>
    <span class="hero-badge">AI</span>
</div>
<p class="hero-sub">Drop a YouTube URL or local audio file — get a transcript, smart summary, and interactive Q&amp;A.</p>
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
col_btn, _ = st.columns([1, 5])
with col_btn:
    run_btn = st.button(
        "Analyse →",
        disabled=st.session_state.pipeline_step >= 0 and not st.session_state.pipeline_done,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PIPELINE TRIGGER
# ══════════════════════════════════════════════════════════════════
if run_btn and source.strip():
    st.session_state.update(
        pipeline_done=False, result=None,
        chat_history=[], error=None, pipeline_step=0,
    )

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
        update_ui(0, "Loading & chunking input…")
        from utils.audio_processor import process_input
        chunks = process_input(source.strip())

        update_ui(1, "Transcribing audio…")
        from core.transcriber import transcribe_all
        transcript = transcribe_all(chunks, translate=True)

        update_ui(2, "Summarising & generating title…")
        from core.summarize import summmarize, generate_title
        title   = generate_title(transcript)
        summary = summmarize(transcript)

        update_ui(3, "Extracting action items, decisions & questions…")
        from core.extractor import extract_action_items, extract_key_decisions, extract_questions
        action_items  = extract_action_items(transcript)
        key_decisions = extract_key_decisions(transcript)
        questions     = extract_questions(transcript)

        update_ui(4, "Building Q&A engine…")
        from core.rag_engine import build_rag_chain
        rag_chain = build_rag_chain(transcript)

        st.session_state.result = {
            "title":        title,
            "transcript":   transcript,
            "summary":      summary,
            "action_items": parse_list(action_items),
            "key_decisions":parse_list(key_decisions),
            "questions":    parse_list(questions),
            "rag_chain":    rag_chain,
        }
        st.session_state.pipeline_done = True
        st.session_state.pipeline_step = len(STEPS)

        with pipeline_ph.container():
            render_pipeline(len(STEPS))
        status_ph.markdown(
            '<span class="status-badge badge-done">✓ Analysis complete</span>',
            unsafe_allow_html=True,
        )

    except FileNotFoundError as e:
        st.session_state.error = f"File not found: {e}"
        st.session_state.pipeline_done = True
    except ValueError as e:
        st.session_state.error = f"Invalid input: {e}"
        st.session_state.pipeline_done = True
    except Exception as e:
        logging.exception("Unhandled exception")
        st.session_state.error = f"{type(e).__name__}: {e}"
        st.session_state.pipeline_done = True

elif run_btn:
    st.warning("Please enter a YouTube URL or file path first.")

# ── persistent pipeline state ──────────────────────────────────────────────
if st.session_state.pipeline_step == len(STEPS) and st.session_state.pipeline_done:
    render_pipeline(len(STEPS))
    st.markdown('<span class="status-badge badge-done">✓ Analysis complete</span>', unsafe_allow_html=True)
elif st.session_state.error:
    render_pipeline(max(st.session_state.pipeline_step, 0))
    st.markdown(
        f'<span class="status-badge badge-error">✗ {st.session_state.error}</span>',
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════
if st.session_state.result:
    r = st.session_state.result
    st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)

    # ── Title & Summary ──
    st.markdown(f"""
    <div class="result-grid">
        <div class="result-card full accent-purple">
            <div class="card-label label-purple">Title</div>
            <div class="card-title">{r['title']}</div>
        </div>
        <div class="result-card full accent-teal">
            <div class="card-label label-teal">Summary</div>
            <div class="card-body">{r['summary']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Extractions ──
    st.markdown(f"""
    <div class="result-grid" style="grid-template-columns:1fr 1fr 1fr; margin-top:1rem;">
        <div class="result-card accent-purple">
            <div class="card-label label-purple">Action Items</div>
            {render_bullet_list(r['action_items'], 'bullet-purple')}
        </div>
        <div class="result-card accent-teal">
            <div class="card-label label-teal">Key Decisions</div>
            {render_bullet_list(r['key_decisions'], 'bullet-teal')}
        </div>
        <div class="result-card accent-purple">
            <div class="card-label label-purple">Open Questions</div>
            {render_bullet_list(r['questions'], 'bullet-purple')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Transcript expander ──
    with st.expander("🪐  Full Transcript"):
        st.text_area(
            label="",
            value=r["transcript"],
            height=300,
            label_visibility="collapsed",
        )

    # ══════════════════════════════════════════════════════════════════
    #  CHAT
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="aurora-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">Ask the transcript</div>', unsafe_allow_html=True)

    if st.session_state.chat_history:
        msgs_html = ""
        for role, text in st.session_state.chat_history:
            cls = "msg-user" if role == "user" else "msg-ai"
            msgs_html += f'<div class="{cls}">{text}</div>'
        st.markdown(msgs_html, unsafe_allow_html=True)
    else:
        st.markdown('<p class="chat-empty">Ask anything about the video…</p>', unsafe_allow_html=True)

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
        st.session_state.chat_history.append(("ai",   answer))
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)