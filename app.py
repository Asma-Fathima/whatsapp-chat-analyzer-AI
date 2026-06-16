streamlit_code = """
import streamlit as st
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google import genai

st.set_page_config(layout="wide")
st.title(" WhatsApp Chat Analyzer + AI")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header(" AI Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password", help="Get a free key from Google AI Studio")

# 1. File Upload Component
uploaded_file = st.file_uploader("Upload your WhatsApp Chat (.txt) file", type=["txt"])

if uploaded_file is not None:
    raw_data = uploaded_file.getvalue().decode("utf-8")
    
    # 2. Parse using our custom Regex rule
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[ApAP][Mm])\s-\s'
    messages = re.split(pattern, raw_data, flags=re.MULTILINE)
    dates = re.findall(pattern, raw_data, flags=re.MULTILINE)
    
    if len(messages) > len(dates):
        messages = messages[1:]
    message_contents = messages[1::2]
    
    df = pd.DataFrame({'user_message': message_contents, 'message_date': dates})
    df['message_date'] = df['message_date'].str.replace('\\u202f', ' ', regex=False)
    
    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')
    except ValueError:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%Y, %I:%M %p', errors='coerce')
        
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    users = []
    actual_messages = []
    for message in df['user_message']:
        entry = re.split(r'([\\w\\W]+?):\s', message)
        if entry[1:]:  
            users.append(entry[1])
            actual_messages.append(entry[2])
        else:          
            users.append('group_notification')
            actual_messages.append(entry[0])
            
    df['user'] = users
    df['message'] = actual_messages
    df = df.drop(columns=['user_message'])
    
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    
    # --- 3. Layout Dashboard Cards ---
    total_messages = df.shape[0]
    total_words = sum(len(str(msg).split()) for msg in df['message'])
    media_omitted = df[df['message'].str.contains('<Media omitted>', na=False)].shape[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(" Total Messages", total_messages)
    with col2:
        st.metric(" Total Words Spoken", total_words)
    with col3:
        st.metric(" Media Hidden", media_omitted)
        
    st.markdown("---")
    
    # --- 4. Generate and Display Charts Side-by-Side ---
    sns.set_theme(style="darkgrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    real_users = df[df['user'] != 'group_notification']
    top_senders = real_users['user'].value_counts().head(5)
    sns.barplot(x=top_senders.values, y=top_senders.index, ax=ax1, palette="viridis", hue=top_senders.index, legend=False)
    ax1.set_title("Top 5 Most Active Members", fontsize=14, fontweight='bold')
    
    timeline = df.groupby(['year', 'month']).size().reset_index(name='message_count')
    timeline['time_label'] = timeline['month'] + "-" + timeline['year'].astype(str)
    sns.lineplot(data=timeline, x='time_label', y='message_count', ax=ax2, marker="o", color="dodgerblue", linewidth=2.5)
    ax2.set_title("Chat Activity Timeline", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    st.markdown("---")
    
    # --- 5. THE AI SMART SUMMARIZER COMPONENT ---
    st.header(" AI Chat Smart Digest")
    
    if not api_key:
        st.info(" To unlock the AI Executive Summary, please enter your free Gemini API Key in the left sidebar configuration panel.")
    else:
        if st.button(" Generate AI Executive Summary", type="primary"):
            with st.spinner("AI is analyzing the tone, topics, and discussions across your chat log history..."):
                try:
                    # Initialize the official GenAI Client with user key
                    client = genai.Client(api_key=api_key)
                    
                    # Clean and compile only human chat data to save token size
                    human_logs = df[df['user'] != 'group_notification'][['user', 'message']].dropna()
                    compiled_text = "\\n".join([f"{row['user']}: {row['message']}" for _, row in human_logs.tail(1500).iterrows()])
                    
                    # Design a strict analytical prompt template
                    ai_prompt = (
                        "You are an expert chat data analyst. Below is a raw log export of a WhatsApp group chat. "
                        "Analyze the conversation data deeply and provide a structured Executive Summary. "
                        "Format your response with the following headers: "
                        "###  Main Discussion Topics (What are they talking about?)\\n"
                        "###  Group Vibe & Tone Analysis (What is the general mood?)\\n"
                        "###  Key Decisions, Links, or Highlights (Bulleted wrap-up)\\n\\n"
                        f"Here is the raw conversation history data:\\n{compiled_text}"
                    )
                    
                    # Generate the summary response string
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=ai_prompt
                    )
                    
                    # Render the beautiful Markdown text directly to the UI panel
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred while calling the AI Engine: {e}")
                    
    st.markdown("---")
    st.dataframe(df.head(10), use_container_width=True)
"""

destination_path = r"C:\Users\HP\Downloads\WhatsApp Chat \app.py"
with open(destination_path, "w", encoding="utf-8") as f:
    f.write(streamlit_code)

print(" app.py successfully upgraded with AI Summarization structures!")
