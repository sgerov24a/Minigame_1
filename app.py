import time

import streamlit as st

st.set_page_config(
    page_title="Сравнение на числа",
    page_icon="🔵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

FIELDS = 6

PAGE_THEMES = {
    1: {
        "title": "Първа група числа",
        "subtitle": "Въведи шест числа – по три във всяка колона",
        "bg1": "#e8f3ff",
        "bg2": "#bcdcff",
        "border": "#1456d6",
        "soft": "#cfe0fb",
        "focus": "#2f8bff",
    },
    2: {
        "title": "Втора група числа",
        "subtitle": "Сега въведи втората група със същите граници",
        "bg1": "#ffeaf4",
        "bg2": "#ffc3de",
        "border": "#f0559b",
        "soft": "#ffd0e4",
        "focus": "#f0559b",
    },
}

# ---------- ОБЩ ДИЗАЙН ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp, .stApp * { font-family: 'Inter', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(255,255,255,0.85) 0, rgba(255,255,255,0) 38%),
        radial-gradient(circle at 90% 95%, rgba(255,255,255,0.55) 0, rgba(255,255,255,0) 40%),
        linear-gradient(160deg, var(--bg1, #e8f3ff) 0%, var(--bg2, #bcdcff) 100%);
    background-attachment: fixed;
}

.block-container { max-width: 720px; padding-top: 2.4rem; padding-bottom: 2.5rem; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeUp 0.5s ease both; }

/* ----- Заглавие и стъпки ----- */
.steps {
    display: flex; justify-content: center; align-items: center; gap: 0.6rem;
    margin-bottom: 1.1rem;
}
.step-dot {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.95rem;
    background: rgba(255,255,255,0.75); color: #5b7aa8;
    border: 2px solid rgba(29,111,232,0.25);
}
.step-dot.active {
    background: linear-gradient(135deg, #2f8bff, #1456d6);
    color: #ffffff; border-color: transparent;
    box-shadow: 0 6px 16px rgba(20,86,214,0.35);
}
.step-dot.done {
    background: #1456d6; color: #ffffff; border-color: transparent;
}
.step-line { width: 46px; height: 3px; border-radius: 3px; background: rgba(29,111,232,0.25); }
.step-line.done { background: #1456d6; }

.page-title {
    font-size: 1.9rem; font-weight: 800; text-align: center;
    color: #0a2554; letter-spacing: -0.02em; margin-bottom: 0.25rem;
}
.page-subtitle {
    text-align: center; color: #3f5f93; margin-bottom: 1.5rem; font-size: 1rem;
}

/* ----- Карта с полетата ----- */
.st-key-panel {
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 8px solid var(--panel-border, #1456d6);
    border-radius: 34px;
    padding: 2.8rem 3rem 2.4rem;
    box-shadow: 0 18px 50px rgba(20, 86, 214, 0.18);
    animation: fadeUp 0.5s ease both;
}

.field-label {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.93rem; font-weight: 600; color: #0a2554; margin-bottom: 0.25rem;
}
.range-chip {
    font-size: 0.74rem; font-weight: 700; color: #1456d6;
    background: #e3eeff; padding: 0.12rem 0.55rem; border-radius: 999px;
}

div[data-testid="stNumberInput"] input {
    background: #f3f8ff !important;
    color: #0a2554 !important;
    border-radius: 14px !important;
    text-align: center;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
}
div[data-testid="stNumberInput"] > div { border-radius: 14px !important; }
div[data-testid="stNumberInput"] button { display: none !important; }
div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stNumberInput"] div[data-baseweb="base-input"] {
    border-radius: 16px !important;
    border: 4px solid var(--field-soft, #cfe0fb) !important;
    background: #ffffff !important;
    padding: 0.35rem 0.4rem !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
div[data-testid="stNumberInput"] div[data-baseweb="base-input"]:focus-within {
    border-color: var(--field-focus, #2f8bff) !important;
    box-shadow: 0 0 0 5px rgba(47,139,255,0.15) !important;
}

/* ----- Бутони ----- */
.stButton > button {
    border-radius: 16px !important;
    min-height: 2.9rem;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: 2px solid transparent !important;
    transition: transform 0.12s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
.stButton > button:hover:not(:disabled) {
    transform: translateY(-2px);
    filter: brightness(1.04);
}

[class*="st-key-clear_"] button {
    background: #ffffff !important;
    color: #d62839 !important;
    border-color: #f3b4bb !important;
}
[class*="st-key-clear_"] button:hover:not(:disabled) {
    box-shadow: 0 8px 18px rgba(214,40,57,0.18);
}

[class*="st-key-continue_"] button,
.st-key-restart button {
    background: linear-gradient(135deg, #2f8bff, #1456d6) !important;
    color: #ffffff !important;
    box-shadow: 0 10px 22px rgba(20,86,214,0.32);
}
[class*="st-key-continue_"] button:disabled {
    background: #c4d7f3 !important;
    color: #ffffff !important;
    box-shadow: none;
}

.stCaption, [data-testid="stCaptionContainer"] { text-align: center; color: #3f5f93 !important; }

/* ----- Зареждане ----- */
.loading-wrap {
    min-height: 60vh; display: flex; flex-direction: column;
    justify-content: center; align-items: center; gap: 1.4rem;
}
.loading-spinner {
    width: 84px; height: 84px; border-radius: 50%;
    border: 8px solid rgba(255,255,255,0.9);
    border-top-color: #1456d6; border-right-color: #2f8bff;
    animation: spin 0.9s linear infinite;
    box-shadow: 0 10px 28px rgba(20,86,214,0.25);
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-text { font-size: 1.2rem; font-weight: 700; color: #0a2554; }
.loading-sub { font-size: 0.95rem; color: #3f5f93; margin-top: -0.8rem; }

/* ----- Резултат ----- */
.result-ring {
    --pct: 0;
    width: 250px; height: 250px; margin: 1.2rem auto 1.5rem;
    border-radius: 50%;
    background: conic-gradient(var(--result-color, #1456d6) calc(var(--pct) * 1%), #dbe7f8 0);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 18px 44px rgba(10, 37, 84, 0.2);
    animation: fadeUp 0.6s ease both;
}
.result-inner {
    width: 202px; height: 202px; border-radius: 50%; background: #ffffff;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.result-value { font-size: 2.9rem; font-weight: 800; color: #0a2554; letter-spacing: -0.03em; }
.result-caption { font-size: 0.82rem; font-weight: 600; color: #5b7aa8; text-transform: uppercase; letter-spacing: 0.08em; }

.result-message {
    max-width: 520px; margin: 0 auto 1.4rem; text-align: center;
    color: #0a2554; font-size: 1.12rem; font-weight: 500; line-height: 1.6;
}

.pair-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.7rem;
    max-width: 560px; margin: 0 auto 1.2rem;
}
.pair-card {
    background: rgba(255,255,255,0.85); border-radius: 18px; padding: 0.7rem 0.5rem;
    text-align: center; box-shadow: 0 8px 20px rgba(20,86,214,0.12);
    border: 1px solid rgba(255,255,255,0.95);
}
.pair-name { font-size: 0.74rem; font-weight: 600; color: #5b7aa8; }
.pair-numbers { font-size: 1.05rem; font-weight: 700; color: #0a2554; margin: 0.1rem 0; }
.pair-pct { font-size: 0.9rem; font-weight: 700; color: #1456d6; }

@media (max-width: 640px) {
    .page-title { font-size: 1.55rem; }
    .st-key-panel { padding: 1.6rem 1.3rem 1.3rem; border-width: 6px; }
    .pair-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
""",
    unsafe_allow_html=True,
)


def set_theme(bg1, bg2, border="#1456d6", soft="#cfe0fb", focus="#2f8bff"):
    st.markdown(
        "<style>.stApp { --bg1: %s; --bg2: %s; --panel-border: %s; "
        "--field-soft: %s; --field-focus: %s; }</style>"
        % (bg1, bg2, border, soft, focus),
        unsafe_allow_html=True,
    )


# ---------- СЪСТОЯНИЕ ----------
defaults = {
    "page": 1,
    "values_page_1": [None] * FIELDS,
    "values_page_2": [None] * FIELDS,
    "loading_started": False,
    "result": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def field_key(page_number, i):
    return f"p{page_number}_field_{i}"


def read_values(page_number):
    return [st.session_state.get(field_key(page_number, i)) for i in range(FIELDS)]


# ---------- CALLBACK-ове (променят състоянието преди ново рисуване) ----------
def clear_page(page_number):
    for i in range(FIELDS):
        st.session_state[field_key(page_number, i)] = None


def go_next(page_number):
    values = read_values(page_number)
    if any(v is None for v in values):
        return
    st.session_state[f"values_page_{page_number}"] = values
    if page_number == 1:
        st.session_state.page = 2
    else:
        st.session_state.page = 3
        st.session_state.loading_started = False
        st.session_state.result = None


def restart():
    for page_number in (1, 2):
        for i in range(FIELDS):
            st.session_state.pop(field_key(page_number, i), None)
    st.session_state.page = 1
    st.session_state.values_page_1 = [None] * FIELDS
    st.session_state.values_page_2 = [None] * FIELDS
    st.session_state.loading_started = False
    st.session_state.result = None


# ---------- ПОМОЩНИ ЕЛЕМЕНТИ ----------
def steps_html(active):
    def dot(n):
        if n < active:
            return f'<div class="step-dot done">✓</div>'
        if n == active:
            return f'<div class="step-dot active">{n}</div>'
        return f'<div class="step-dot">{n}</div>'

    def line(n):
        cls = "step-line done" if n < active else "step-line"
        return f'<div class="{cls}"></div>'

    return (
        '<div class="steps fade-in">'
        + dot(1) + line(1) + dot(2) + line(2) + dot(3)
        + "</div>"
    )


# ---------- СТРАНИЦИ 1 И 2 ----------
def render_input_page(page_number):
    theme = PAGE_THEMES[page_number]
    set_theme(
        theme["bg1"],
        theme["bg2"],
        theme["border"],
        theme["soft"],
        theme["focus"],
    )

    st.markdown(steps_html(page_number), unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-title fade-in">{theme["title"]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="page-subtitle fade-in">{theme["subtitle"]}</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="panel"):
        left, right = st.columns(2, gap="large")
        for col, indices in ((left, (0, 1, 2)), (right, (3, 4, 5))):
            with col:
                for i in indices:
                    if i < 3:
                        label, lo, hi = f"Поле {i + 1}", 2, 6
                        placeholder = "от 2 до 6"
                    else:
                        label, lo, hi = f"Поле {i + 1}", 1, 10
                        placeholder = "от 1 до 10"

                    st.markdown(
                        f'<div class="field-label"><span>{label}</span>'
                        f'<span class="range-chip">{lo}–{hi}</span></div>',
                        unsafe_allow_html=True,
                    )
                    st.number_input(
                        f"{label} ({lo}–{hi})",
                        min_value=lo,
                        max_value=hi,
                        value=None,
                        step=1,
                        key=field_key(page_number, i),
                        label_visibility="collapsed",
                        placeholder=placeholder,
                    )

    all_filled = all(v is not None for v in read_values(page_number))

    st.write("")
    delete_col, _, continue_col = st.columns([1.2, 2.0, 1.5])
    with delete_col:
        st.button(
            "Изтрий",
            key=f"clear_{page_number}",
            use_container_width=True,
            on_click=clear_page,
            args=(page_number,),
        )
    with continue_col:
        st.button(
            "Продължи →" if page_number == 1 else "Изчисли →",
            key=f"continue_{page_number}",
            use_container_width=True,
            disabled=not all_filled,
            on_click=go_next,
            args=(page_number,),
        )

    if not all_filled:
        st.caption("Попълни всички 6 полета, за да продължиш.")


# ---------- РЕЗУЛТАТ ----------
def result_style_and_message(percent):
    if percent < 20:
        return "#e5383b", "Сходството е много ниско. Двете групи числа се различават значително."
    if percent < 40:
        return "#f77f00", "Сходството е ниско. Има известна прилика, но разликите са големи."
    if percent < 60:
        return "#e0b400", "Сходството е умерено. Двете групи числа имат частична прилика."
    if percent < 80:
        return "#4caf50", "Сходството е високо. Двете групи числа са сравнително близки."
    return "#1b8a3e", "Сходството е много високо. Двете групи числа са почти напълно сходни."


def pair_percent(a, b):
    # По-малкото число се дели на по-голямото -> 0..100% за всяка двойка.
    if not a or not b:
        return 0.0
    return (min(a, b) / max(a, b)) * 100


def compute_similarity(first, second):
    pairs = [pair_percent(a, b) for a, b in zip(first, second)]
    return sum(pairs) / len(pairs) if pairs else 0.0


def pairs_html(first, second):
    cards = []
    for i, (a, b) in enumerate(zip(first, second), start=1):
        cards.append(
            '<div class="pair-card">'
            f'<div class="pair-name">Двойка {i}</div>'
            f'<div class="pair-numbers">{a} · {b}</div>'
            f'<div class="pair-pct">{pair_percent(a, b):.0f}%</div>'
            "</div>"
        )
    return '<div class="pair-grid fade-in">' + "".join(cards) + "</div>"


# ---------- РОУТЕР ----------
page = st.session_state.page

if page in (1, 2):
    render_input_page(page)

else:
    set_theme("#eef3fa", "#c9d8ee")

    if not st.session_state.loading_started:
        loading = st.empty()
        loading.markdown(
            '<div class="loading-wrap">'
            '<div class="loading-spinner"></div>'
            '<div class="loading-text">Изчисляване на сходството...</div>'
            '<div class="loading-sub">Моля, изчакай няколко секунди</div>'
            "</div>",
            unsafe_allow_html=True,
        )
        time.sleep(5)
        st.session_state.result = compute_similarity(
            st.session_state.values_page_1,
            st.session_state.values_page_2,
        )
        st.session_state.loading_started = True
        loading.empty()
        st.rerun()

    result = st.session_state.result
    ring_color, message = result_style_and_message(result)

    st.markdown(steps_html(4), unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-ring" style="--pct: {result:.1f}; --result-color: {ring_color};">'
        '<div class="result-inner">'
        f'<div class="result-value">{result:.1f}%</div>'
        '<div class="result-caption">сходство</div>'
        "</div></div>"
        f'<div class="result-message fade-in">{message}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        pairs_html(st.session_state.values_page_1, st.session_state.values_page_2),
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 1.5, 1])
    with mid:
        st.button(
            "Ново изчисление",
            key="restart",
            use_container_width=True,
            on_click=restart,
        )
