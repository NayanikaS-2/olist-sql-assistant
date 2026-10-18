import csv, datetime
import streamlit as st
from ask import ask

st.set_page_config(page_title="Olist SQL Assistant", page_icon="📊")
st.title("📊 Ask your data")
st.caption("Ask questions about the Olist Brazilian e-commerce dataset in plain English.")

if "history" not in st.session_state:
    st.session_state.history = []


def save_feedback(question, sql, vote):
    with open("feedback.csv", "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.datetime.now().isoformat(), question, sql, vote])


def show_chart(df):
    nums = list(df.select_dtypes("number").columns)
    others = [c for c in df.columns if c not in nums]
    if len(df) > 1 and nums and others:
        st.bar_chart(df.set_index(others[0])[nums[0]])


for i, item in enumerate(st.session_state.history):
    with st.chat_message("user"):
        st.write(item["question"])
    with st.chat_message("assistant"):
        if item["error"]:
            st.error("Sorry, I couldn't answer that: " + item["error"])
            continue
        st.dataframe(item["df"], use_container_width=True)
        show_chart(item["df"])
        with st.expander("SQL used"):
            st.code(item["sql"], language="sql")
        c1, c2, _ = st.columns([1, 1, 6])
        if c1.button("👍", key=f"up{i}"):
            save_feedback(item["question"], item["sql"], "up")
            st.toast("Thanks for the feedback!")
        if c2.button("👎", key=f"down{i}"):
            save_feedback(item["question"], item["sql"], "down")
            st.toast("Thanks, noted.")

q = st.chat_input("Ask a question, e.g. Which 5 states have the most customers?")
if q:
    with st.spinner("Thinking..."):
        try:
            sql, df = ask(q)
            st.session_state.history.append({"question": q, "sql": sql, "df": df, "error": None})
        except Exception as e:
            st.session_state.history.append({"question": q, "sql": "", "df": None, "error": str(e)[:300]})
    st.rerun()