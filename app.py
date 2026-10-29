
import time

import streamlit as st

st.set_page_config(
    page_title="Сравнение на числа",
    page_icon="o",
    layout="centered",
    initial_sidebar_state="collapsed",
)

FIELDS = 6

# Полета 1–3: от 2 до 6
# Полета 4–6: от 1 до 10
FIELD_RANGES = [(2, 6)] * 3 + [(1, 10)] * 3

# Отделни имена за всяко поле на всяка страница
FIELD_NAMES = {
    1: [
        "Поле 1",
        "Поле 2",
        "Поле 3",
        "Поле 4",
        "Поле 5",
        "Поле 6",
    ],
    2: [
        "Поле 1",
        "Поле 2",
        "Поле 3",
        "Поле 4",
        "Поле 5",
        "Поле 6",
    ],
}

THEMES = {
    1: {
        "title": "Страница 1",
        "bg": "#7bd3f5",
        "panel": "#05a9e8",
    },
    2: {
        "title": "Страница 2",
        "bg": "#f8c9df",
        "panel": "#f2a5ca",
    },
}

st.markdown(
    """
<style>
#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}

.stApp {
    background: var(--page-bg, #7bd3f5);
}

.block-container {
    max-width: 720px;
    padding-top: 2.5rem;
    padding-bottom: 2.5rem;
}

.page-title {
    font-size: 2rem;
    font-weight: 800;
    text-align: center;
    color: #000000;
    margin-bottom: 1.2rem;
}

.st-key-panel {
    background: var(--panel-bg, #05a9e8);
    border: 10px solid #000000;
    border-radius: 30px;
    padding: 3rem 3.2rem 2.6rem;
}

.field-label {
    font-size: 1rem;
    font-weight: 700;
    color: #000000;
    margin-bottom: 0.3rem;
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

div[data-testid="stNumberInput"] button {
    display: none !important;
}

.stButton > button {
    border: 4px solid #000000 !important;

