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
    1: {"bg": "#dbeeff", "panel": "#ffffff", "accent": "#1d6fe8", "title": "Първа група числа"},
    2: {"bg": "#d3e4fb", "panel": "#ffffff", "accent": "#0b4fb3", "title": "Втора група числа"},
}

# ---------- ОБЩ ДИЗАЙН ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, .stApp, .stApp * { font-family: 'Inter', sans-serif; }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }

    .stApp { background: var(--page-bg, #dbeeff); }

    .block-container { max-width: 760px; padding-top: 2.5rem; padding-bottom: 2rem; }

    .page-title {
        font-size: 1.7rem; font-weight: 700; text-align: center;
        color: #0b2a5b; margin-bottom: 0.2rem;
    }
    .page-subtitle {
        text-align: center; color: #3b5b8c; margin-bottom: 1.4rem; font-size: 0.98rem;
    }

    /* Панел (контейнер с ключ "panel") */
    .st-key-panel {
        background: var(--panel-bg, #ffffff);
        border: 2px solid #1d6fe8;
        border-radius: 24px;
        padding: 1.8rem 2rem 1.4rem;
        box-shadow: 0 10px 30px rgba(29, 111, 232, 0.15);
    }

    .field-label {
        font-size: 0.95rem; font-weight: 600; color: #0b2a5b; margin-bottom: 0.2rem;
    }

    div[data-testid="stNumberInput"] input {
        background: #f4f9ff !important;
        color: #0b2a5b !important;
        border-radius: 12px !important;
        text-align: center;
        font-size: 1.1rem !important;
    }
    div[data-testid="stNumberInput"] button { display: none !important; }

    .stButton > button {
        border-radius: 14px !important;
        min-height: 2.7rem;
        font-weight: 600 !important;
        border: 2px solid #1d6fe8 !important;
        transition: transform 0.12s ease, filter 0.12s ease;
    }
    .stButton > button:hover:not(:disabled) { transform: translateY(-1px); filter: brightness(1.05); }

    /* Бутон „Изтрий" */
    [class*="st-key-clear_"] button {
        background: #ffffff !important; color: #d62839 !important; border-color: #d62839 !important;
    }
    /* Бутони „Продължи" / „Ново изчисление" */
    [class*="st-key-continue_"] button, .st-key-restart button {
        background: #1d6fe8 !important; color: #ffffff !important;
    }
    [class*="st-key-continue_"] button:disabled {
        background: #a9c8f5 !important; border-color: #a9c8f5 !important; color: #ffffff !important;
    }

    .result-circle {
        width: 230px; height: 230px; margin: 1.5rem auto 1.6rem;
        border-radius: 50%; background: #ffffff;
        border: 12px solid var(--result-color, #1d6fe8);
        display: flex; align-items: center; justify-content: center;
        font-size: 2.6rem; font-weight: 700; color: #0b2a5b;
        box-shadow: 0 10px 30px rgba(11, 42, 91, 0.18);
    }
    .result-message {
        max-width: 560px; margin: 0 auto; text-align: center;
        color: #0b2a5b; font-size: 1.1rem; font-weight: 500; line-height: 1.6;
    }

    .loading-wrap {
        min-height: 55vh; display: flex; flex-direction: column;
        justify-content: center; align-items: center; gap: 1.2rem;
    }
    .loading-spinner {
        width: 76px; height: 76px; border: 8px solid #ffffff;
        border-top-color: #1d6fe8; border-radius: 50%;
        animation: spin 0.9s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .loading-text { font-size: 1.15rem; font-weight: 600; color: #0b2a5b; }
    </style>
    """,
    unsafe_allow_html=True,
)


def set_theme(page_bg, panel_bg="#ffffff"):
    st.markdown(
        f"<style>.stApp {{ --page-bg: {page_bg}; --panel-bg: {panel_bg}; }}</style>",
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


# ---------- CALLBACK-ове (безопасно променят състоянието преди ново рисуване) ----------
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
    theme = PAGE_THEMES[page_number]
    set_theme(theme["bg"], theme["panel"])

    st.markdown(f'<div class="page-title">{theme["title"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-subtitle">Стъпка {page_number} от 2 · попълни всички полета</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="panel"):
        left, right = st.columns(2, gap="large")
        for col, indices in ((left, (0, 1, 2)), (right, (3, 4, 5))):
            with col:
                for i in indices:
                    if i < 3:
                        label, lo, hi = f"Поле {i + 1} (2–6)", 2, 6
                        placeholder = "Число от 2 до 6"
                    else:
                        label, lo, hi = f"Поле {i + 1} (1–10)", 1, 10
                        placeholder = "Число от 1 до 10"

                    st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
                    st.number_input(
                        label,
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
    delete_col, _, continue_col = st.columns([1.2, 2.2, 1.4])
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
        return "#e5383b", "Сходството е много ниско. Двете групи числа се различават значително."
    if percent < 40:
        return "#f77f00", "Сходството е ниско. Има известна прилика, но разликите са големи."
    if percent < 60:
        return "#e9c716", "Сходството е умерено. Двете групи числа имат частична прилика."
    if percent < 80:
        return "#5fbf5a", "Сходството е високо. Двете групи числа са сравнително близки."
    return "#1b8a3e", "Сходството е много високо. Двете групи числа са почти напълно сходни."


def compute_similarity(first, second):
    # По-малкото число се дели на по-голямото -> 0..100% за всяка двойка.
    pairs = [(min(a, b) / max(a, b)) * 100 for a, b in zip(first, second) if a and b]
    return sum(pairs) / len(pairs) if pairs else 0.0


# ---------- РОУТЕР ----------
page = st.session_state.page

if page in (1, 2):
    render_input_page(page)

else:
    set_theme("#e8edf3")

    if not st.session_state.loading_started:
        placeholder = st.empty()
        placeholder.markdown(
            """
            <div class="loading-wrap">
                <div class="loading-spinner"></div>
                <div class="loading-text">Изчисляване на сходството...</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(5)
        st.session_state.result = compute_similarity(
            st.session_state.values_page_1,
            st.session_state.values_page_2,
        )
        st.session_state.loading_started = True
        placeholder.empty()
        st.rerun()

    result = st.session_state.result
    ring_color, message = result_style_and_message(result)

    st.markdown(
        f"""
        <div class="result-circle" style="--result-color: {ring_color};">{result:.1f}%</div>
        <div class="result-message">{message}</div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.button("Ново изчисление", key="restart", use_container_width=True, on_click=restart)
