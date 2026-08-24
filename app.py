import streamlit as st
from google import genai

# Էջի կարգավորումներ
st.set_page_config(page_title="Հովհաննես AI", page_icon="🤖")
st.title("🤖 Հովհաննես AI")

# Ստուգում ենք Secrets-ում GEMINI_API_KEY-ի առկայությունը
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Խնդրում ենք ավելացնել GEMINI_API_KEY-ը Streamlit Secrets-ում:")
    st.stop()

# Ինիցիալիզացնում ենք Google GenAI Client-ը
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Նամակագրության պատմության պահպանում
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ցուցադրում ենք նախորդ հաղորդագրությունները
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Օգտատիրոջ մուտքագրում
if prompt := st.chat_input("Գրեք ձեր հարցը..."):
    # Ավելացնում ենք օգտատիրոջ հարցը պատմության մեջ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ստանում ենք AI-ի պատասխանը
    with st.chat_message("assistant"):
        with st.spinner("Մտածում եմ..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                st.markdown(response.text)
                # Ավելացնում ենք AI-ի պատասխանը պատմության մեջ
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Սխալ տեղի ունեցավ: {e}")
