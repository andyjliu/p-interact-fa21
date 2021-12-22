import streamlit as st

from game import *

OPENAI_API_KEY= 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

header = st.container()

dataset = st.container()
features = st.container()
modelTraining = st.container()

with header:
    st.title("Welcome to our PAI project")
st.button("Begin Game", key=None, help=None, on_click=None, args=None, kwargs=None)
