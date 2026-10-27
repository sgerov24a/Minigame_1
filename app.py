import time

import streamlit as st

st.set_page_config(
    page_title="Сравнение на числа",
    page_icon="🔵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

FIELDS = 6

# Цветове: фон на страницата и цвят на панела
THEMES = {
    1: {"title": "Страница 1", "bg": "#7bd3f5", "panel": "#05a9e8"},
    2: {"title": "Страница 2", "bg": "#f8c9df", "panel": "#f2a5ca"},
}

st.markdown(
    """
<style>
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }

.stApp { background: var(--page-bg, #7bd3f5); }
.block-container { max-width: 720px; padding-top: 2.5rem; padding-bottom: 2.5rem; }

.page-title {
    font-size: 2rem; font-weight: 800; text-align: center;
    color: #000000; margin-bottom: 1.2rem;
}

/* Голям цветен панел с дебела черна рамка и голям падинг */
.st-key-panel {
    background: var(--panel-bg, #05a9e8);
    border: 10px solid #000000;
    border-radius: 30px;
    padding: 3rem 3.2rem 2.6rem;
}

.field-label {
    font-size: 1rem; font-weight: 700; color: #000000; margin-bottom: 0.3rem;
}

div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stNumberInput"] div[data-baseweb="base-input"] {
    background: #ffffff !important;
    border: 4px solid #000000 !important;
    border-radius: 16px !important;
    padding: 0.3rem 0.4rem !important;
}
div[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    color: #000000 !important;
    text-align: center;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
}
div[data-testid="stNumberInput"] button { display: none !important; }

.stButton > button {
    border: 4px solid #000000 !important;
    border-radius: 16px !important;
    min-height: 3rem;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #000000 !important;
}
[class*="st-key-clear_"] button { background: #ff4d57 !important; }
[class*="st-key-continue_"] button, .st-key-restart button { background: #22d760 !important; }
[class*="st-key-continue_"] button:disabled {
    background: #d9d9d9 !important; color: #777777 !important; border-color: #777777 !important;
}

[data-testid="stCaptionContainer"] { text-align: center; color: #000000 !important; }

.loading-wrap {
    min-height: 60vh; display: flex; flex-direction: column;
    justify-content: center; align-items: center; gap: 1.2rem;
}
.loading-spinner {
    width: 80px; height: 80px; border-radius: 50%;
    border: 10px solid #ffffff; border-top-color: #000000;
    animation: spin 0.9s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-text { font-size: 1.2rem; font-weight: 700; color: #000000; }

.result-circle {
    width: 240px; height: 240px; margin: 1.5rem auto 1.5rem;
    border: 10px solid #000000; border-radius: 50%;
    background: #ffffff;
    box-shadow: inset 0 0 0 14px var(--result-color, #22d760);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.8rem; font-weight: 800; color: #000000;
}
.result-message {
    max-width: 520px; margin: 0 auto 1.5rem; text-align: center;
    color: #000000; font-size: 1.15rem; font-weight: 600; line-height: 1.6;
}

@media (max-width: 640px) {
    .st-key-panel { padding: 1.6rem 1.3rem 1.4rem; border-width: 8px; }
}
</style>
""",
    unsafe_allow_html=True,
)


def set_colors(bg, panel="#05a9e8"):
    st.markdown(
        "<style>.stApp { --page-bg: %s; --panel-bg: %s; }</style>" % (bg, panel),
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


# ---------- БУТОНИ (callback-ове) ----------
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


# ---------- СТРАНИЦИ 1 И 2 ----------
def render_input_page(page_number):
    theme = THEMES[page_number]
    set_colors(theme["bg"], theme["panel"])

    st.markdown(f'<div class="page-title">{theme["title"]}</div>', unsafe_allow_html=True)

    with st.container(key="panel"):
        left, right = st.columns(2, gap="large")
        for col, indices in ((left, (0, 1, 2)), (right, (3, 4, 5))):
            with col:
                for i in indices:
                    lo, hi = (2, 6) if i < 3 else (1, 10)
                    label = f"Поле {i + 1} ({lo}–{hi})"

                    st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
                    st.number_input(
                        label,
                        min_value=lo,
                        max_value=hi,
                        value=None,
                        step=1,
                        key=field_key(page_number, i),
                        label_visibility="collapsed",
                        placeholder=f"Число от {lo} до {hi}",
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
            "Продължи",
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
        return "#ef3038", "Сходството е много ниско. Двете групи числа се различават значително."
    if percent < 40:
        return "#ff8c24", "Сходството е ниско. Има известна прилика, но разликите са големи."
    if percent < 60:
        return "#f2d629", "Сходството е умерено. Двете групи числа имат частична прилика."
    if percent < 80:
        return "#8bdc65", "Сходството е високо. Двете групи числа са сравнително близки."
    return "#087d35", "Сходството е много високо. Двете групи числа са почти напълно сходни."


def compute_similarity(first, second):
    # За всяка двойка делим по-малкото число на по-голямото (0–100%),
    # после взимаме средното на шестте процента.
    pairs = [(min(a, b) / max(a, b)) * 100 for a, b in zip(first, second) if a and b]
    return sum(pairs) / len(pairs) if pairs else 0.0


# ---------- РОУТЕР ----------
page = st.session_state.page

if page in (1, 2):
    render_input_page(page)

else:
    set_colors("#c8c8c8")

    if not st.session_state.loading_started:
        loading = st.empty()
        loading.markdown(
            '<div class="loading-wrap">'
            '<div class="loading-spinner"></div>'
            '<div class="loading-text">Изчисляване на сходството...</div>'
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

    st.markdown(
        f'<div class="result-circle" style="--result-color: {ring_color};">{result:.1f}%</div>'
        f'<div class="result-message">{message}</div>',
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 1.5, 1])
    with mid:
        st.button("Ново изчисление", key="restart", use_container_width=True, on_click=restart)
