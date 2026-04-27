"""Streamlit chat UI for the RAG injection demo.

Run:
    streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

from llm import ask_with_context
from retriever import search

st.set_page_config(page_title="ACME HR Assistant", page_icon=":speech_balloon:")

st.title("ACME Pte Ltd — Internal HR Assistant")
st.caption("Ask any question about company policy. Backed by internal policy documents.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for src in msg["sources"]:
                    st.markdown(f"- **{src['source']}**")
                    st.code(src["text"][:400] + ("..." if len(src["text"]) > 400 else ""))

if prompt := st.chat_input("Ask about a policy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Looking up policy..."):
            chunks = search(prompt, k=3)
            answer = ask_with_context(prompt, chunks)
        st.markdown(answer)
        with st.expander("Sources"):
            for src in chunks:
                st.markdown(f"- **{src['source']}**")
                st.code(src["text"][:400] + ("..." if len(src["text"]) > 400 else ""))

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": chunks}
    )
