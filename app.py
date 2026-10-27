
import time
import streamlit as st

st.set_page_config(
    page_title="Сравнение на числа",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- ДИЗАЙН ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"],
    [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    .stApp {
        background: var(--page-bg, #7bd3f5);
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stAppViewContainer"] > .main .block-container {
        max-width: 1180px;
    }

    .page-title {
        font-size: 1.65rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.4rem;
        color: #111111;
    }

    .panel {
        max-width: 820px;
        margin: 0 auto;
        padding: 2.2rem 2.6rem 2rem;
        border: 4px solid #050505;
        border-radius: 34px;
        background: var(--panel-bg, #05a9e8);
        color: #111111;
        box-sizing: border-box;
    }

    .field-label {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
        color: #111111;
    }

    div[data-testid="stNumberInput"] input {
        background: #ffffff !important;
        color: #111111 !important;
        border: 3px solid #050505 !important;
        border-radius: 18px !important;
        min-height: 2.8rem;
        font-size: 1.15rem !important;
        text-align: center;
        box-shadow: none !important;
    }

    div[data-testid="stNumberInput"] button {
        display: none !important;
    }

    div[data-testid="stNumberInput"] > div {
        border: none !important;
        background: transparent !important;
    }

    .stButton > button {
        border: 3px solid #050505 !important;
        border-radius: 18px !important;
        min-height: 2.7rem;
        font-weight: 600 !important;
        color: #111111 !important;
        transition: transform 0.12s ease, filter 0.12s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        filter: brightness(1.03);
    }

    .delete-button .stButton > button {
        background: #ff3d48 !important;
    }

    .continue-button .stButton > button {
        background: #16d45b !important;
    }

    .result-circle {
        width: 220px;
        height: 220px;
        margin: 1.4rem auto 1.6rem;
        border: 7px solid #050505;
        border-radius: 50%;
        background: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 0 7px var(--result-color, #16d45b);
        font-size: 2.55rem;
        font-weight: 500;
        color: #111111;
    }

    .result-message {
        max-width: 720px;
        margin: 0 auto;
        text-align: center;
        color: #222222;
        font-size: 1.12rem;
        font-weight: 500;
        line-height: 1.6;
    }

    .loading-wrap {
        min-height: 55vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 1.2rem;
    }

    .loading-spinner {
        width: 78px;
        height: 78px;
        border: 9px solid #ffffff;
        border-top: 9px solid #111111;
        border-right: 9px solid #16d45b;
        border-radius: 50%;
        animation: spin 0.9s linear infinite;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    .loading-text {
        font-size: 1.15rem;
        font-weight: 600;
        color: #111111;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- СЪСТОЯНИЕ НА САЙТА ----------
if "page" not in st.session_state:
    st.session_state.page = 1

if "values_page_1" not in st.session_state:
    st.session_state.values_page_1 = [None] * 6

if "values_page_2" not in st.session_state:
    st.session_state.values_page_2 = [None] * 6

if "loading_started" not in st.session_state:
    st.session_state.loading_started = False

if "result" not in st.session_state:
    st.session_state.result = None


# ---------- ИЗТРИВАНЕ НА ПОЛЕТАТА ----------
def clear_current_page(page_number):
    for i in range(6):
        st.session_state[f"p{page_number}_field_{i}"] = None

    if page_number == 1:
        st.session_state.values_page_1 = [None] * 6
    else:
        st.session_state.values_page_2 = [None] * 6


# ---------- ПРОЧИТАНЕ НА ВЪВЕДЕНИТЕ ЧИСЛА ----------
def read_current_values(page_number):
    return [
        st.session_state.get(f"p{page_number}_field_{i}")
        for i in range(6)
    ]


# ---------- СТРАНИЦИ 1 И 2 ----------
def render_input_page(page_number, background, panel_color, title):

    st.markdown(
        f"""
        <style>
        .stApp {{
            --page-bg: {background};
            --panel-bg: {panel_color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="page-title">{title}</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="large")

    for col, indices in (
        (left, (0, 1, 2)),
        (right, (3, 4, 5)),
    ):
        with col:

            for i in indices:

                field_number = i + 1

                if i < 3:
                    label = f"Поле {field_number} (2–6)"
                    min_value = 2
                    max_value = 6
                    placeholder = "Число от 2 до 6"
                else:
                    label = f"Поле {field_number} (1–10)"
                    min_value = 1
                    max_value = 10
                    placeholder = "Число от 1 до 10"

                st.markdown(
                    f'<div class="field-label">{label}</div>',
                    unsafe_allow_html=True,
                )

                st.number_input(
                    label,
                    min_value=min_value,
                    max_value=max_value,
                    value=None,
                    step=1,
                    key=f"p{page_number}_field_{i}",
                    label_visibility="collapsed",
                    placeholder=placeholder,
                )

    values = read_current_values(page_number)

    all_filled = all(
        value is not None
        for value in values
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    delete_col, spacer_col, continue_col = st.columns(
        [1.2, 2.5, 1.4]
    )

    with delete_col:

        st.markdown(
            '<div class="delete-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Изтрий",
            key=f"clear_{page_number}",
            use_container_width=True,
        ):
            clear_current_page(page_number)
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with continue_col:

        st.markdown(
            '<div class="continue-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Продължи",
            key=f"continue_{page_number}",
            use_container_width=True,
            disabled=not all_filled,
        ):

            if page_number == 1:
                st.session_state.values_page_1 = values
                st.session_state.page = 2

            else:
                st.session_state.values_page_2 = values
                st.session_state.page = 3
                st.session_state.loading_started = False
                st.session_state.result = None

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if not all_filled:
        st.caption(
            "Попълни всички 6 полета, за да продължиш."
        )


# ---------- ЦВЯТ И СЪОБЩЕНИЕ СПОРЕД РЕЗУЛТАТА ----------
def result_style_and_message(percent):

    if percent < 20:
        return (
            "#ef3038",
            "Сходството е много ниско. "
            "Двете групи числа се различават значително."
        )

    if percent < 40:
        return (
            "#ff8c24",
            "Сходството е ниско. "
            "Има известна прилика, но разликите са големи."
        )

    if percent < 60:
        return (
            "#f2d629",
            "Сходството е умерено. "
            "Двете групи числа имат частична прилика."
        )

    if percent < 80:
        return (
            "#8bdc65",
            "Сходството е високо. "
            "Двете групи числа са сравнително близки."
        )

    return (
        "#087d35",
        "Сходството е много високо. "
        "Двете групи числа са почти напълно сходни."
    )


# ---------- СТРАНИЦА 1 ----------
if st.session_state.page == 1:

    render_input_page(
        page_number=1,
        background="#7bd3f5",
        panel_color="#05a9e8",
        title="Страница 1",
    )


# ---------- СТРАНИЦА 2 ----------
elif st.session_state.page == 2:

    render_input_page(
        page_number=2,
        background="#f8c9df",
        panel_color="#f2a5ca",
        title="Страница 2",
    )


# ---------- СТРАНИЦА 3 ----------
elif st.session_state.page == 3:

    if not st.session_state.loading_started:

        st.session_state.loading_started = True

        st.markdown(
            """
            <style>
            .stApp {
                --page-bg: #c8c8c8;
            }
            </style>

            <div class="loading-wrap">
                <div class="loading-spinner"></div>
                <div class="loading-text">
                    Изчисляване на сходството...
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(5)

        first = st.session_state.values_page_1
        second = st.session_state.values_page_2

        # Винаги делим по-малкото число на по-голямото.
        # Така резултатът за всяка двойка е между 0% и 100%.
        pair_percentages = [
            (min(a, b) / max(a, b)) * 100
            for a, b in zip(first, second)
        ]

        # Средноаритметична стойност на шестте процента.
        st.session_state.result = (
            sum(pair_percentages) / len(pair_percentages)
        )

        st.rerun()

    st.markdown(
        """
        <style>
        .stApp {
            --page-bg: #c8c8c8;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.result

    ring_color, message = result_style_and_message(result)

    st.markdown(
        f"""
        <div
            class="result-circle"
            style="--result-color: {ring_color};"
        >
            {result:.1f}%
        </div>

        <div class="result-message">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    _, _, restart_col = st.columns([3, 1, 1.5])

    with restart_col:

        st.markdown(
            '<div class="continue-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Ново изчисление",
            key="restart",
            use_container_width=True,
        ):

            for page_number in (1, 2):
                for i in range(6):
                    st.session_state.pop(
                        f"p{page_number}_field_{i}",
                        None,
                    )

            st.session_state.page = 1
            st.session_state.values_page_1 = [None] * 6
            st.session_state.values_page_2 = [None] * 6
            st.session_state.loading_started = False
            st.session_state.result = None

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
```
