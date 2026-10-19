import csv, datetime, os
import streamlit as st

# Load the key from Streamlit Cloud's private Secrets (does nothing on your own computer)
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

from ask import ask

PER_SESSION_LIMIT = 10   # questions per visitor
DAILY_LIMIT = 100        # questions for the whole app per day

st.set_page_config(page_title="Olist SQL Assistant", page_icon="📊")
st.title("📊 Ask your data")
st.caption("Ask questions about the Olist Brazilian e-commerce dataset in plain English.")

if "history" not in st.session_state:
    st.session_state.history = []
if "n_asked" not in st.session_state:
    st.session_state.n_asked = 0


@st.cache_resource
def usage_counter():
    return {}


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

left = PER_SESSION_LIMIT - st.session_state.n_asked
st.caption(f"Questions left in this session: {max(left, 0)}")

q = st.chat_input("Ask a question, e.g. Which 5 states have the most customers?")
if q:
    usage = usage_counter()
    today = str(datetime.date.today())
    if st.session_state.n_asked >= PER_SESSION_LIMIT:
        st.session_state.history.append({"question": q, "sql": "", "df": None,
            "error": "you've reached the question limit for this session."})
    elif usage.get(today, 0) >= DAILY_LIMIT:
        st.session_state.history.append({"question": q, "sql": "", "df": None,
            "error": "the demo has reached its daily limit. Please try again tomorrow."})
    else:
        usage[today] = usage.get(today, 0) + 1
        st.session_state.n_asked += 1
        with st.spinner("Thinking..."):
            try:
                sql, df = ask(q)
                st.session_state.history.append({"question": q, "sql": sql, "df": df, "error": None})
            except Exception as e:
                st.session_state.history.append({"question": q, "sql": "", "df": None, "error": str(e)[:300]})
    st.rerun()