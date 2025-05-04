import streamlit as st
from sql_query_graph import answer_question  # Custom graph you built


# --- Custom CSS ---
# --- Custom CSS ---
st.title("📊 SQL Assistant")

# Sidebar: Data source context
st.sidebar.title("🗂️ Data Sources")

st.sidebar.markdown("""
**已连接到 sqlite 数据库:**

Northwind 是一个经典零售数据集
                    
包含客户、订单、产品、员工信息

💡 *尝试提问：*
- 列出所有来自德国的客户。
- 所有德国客户的订单总数是多少？
- 最早的德国客户订单是什么时候的？
""")


# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Each item is a dict: {"question", "sql", "answer"}

# --- Chat UI rendering (top to bottom) ---
for item in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(f"**🧠 问题:** {item['question']}")
    with st.chat_message("assistant"):
        st.markdown(f"**🛠️ SQL 查询:**\n```sql\n{item['sql']}\n```")
        st.markdown(f"**🤖 回答:** {item['answer']}")

# --- User input at the bottom ---
user_question = st.chat_input("Ask your data question:")

# --- Run graph and update memory ---
if user_question:
    with st.spinner("思考中..."):
        result = {}
        for update in answer_question(user_question):  # your streaming graph
            result.update(update)

        sql_query = result.get("write_query", {}).get("query", "未生成 SQL 查询")
        answer = result.get("generate_answer", {}).get("answer", "没有可用的回答")

        # Save to memory
        st.session_state.chat_history.append(
            {"question": user_question, "sql": sql_query, "answer": answer}
        )
    # st.experimental_rerun()
    for item in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(f"**🧠 问题:** {item['question']}")
        with st.chat_message("assistant"):
            st.markdown(f"**🛠️ SQL 查询:**\n```sql\n{item['sql']}\n```")
            st.markdown(f"**🤖 回答:** {item['answer']}")
