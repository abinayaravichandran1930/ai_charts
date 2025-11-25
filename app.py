# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import openai

# ---------------------------
# CONFIGURE OPENAI API
# ---------------------------
openai.api_key = "YOUR_OPENAI_API_KEY"

# ---------------------------
# APP LAYOUT
# ---------------------------
st.title("AI-Powered Data Visualization")

st.markdown("""
Upload your CSV/Excel or connect Google Sheet and get instant charts + AI insights.
""")

# ---------------------------
# DATA UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Data uploaded successfully!")
    st.write("Preview of your data:", df.head())

    # ---------------------------
    # AUTOMATIC CHART SUGGESTION
    # ---------------------------
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    chart_type = st.selectbox("Choose chart type", ["Bar", "Line", "Scatter", "Pie"])

    if chart_type == "Bar":
        x = st.selectbox("X-axis", categorical_cols + numeric_cols)
        y = st.selectbox("Y-axis", numeric_cols)
        fig = px.bar(df, x=x, y=y)
    elif chart_type == "Line":
        x = st.selectbox("X-axis", numeric_cols + categorical_cols)
        y = st.selectbox("Y-axis", numeric_cols)
        fig = px.line(df, x=x, y=y)
    elif chart_type == "Scatter":
        x = st.selectbox("X-axis", numeric_cols)
        y = st.selectbox("Y-axis", numeric_cols)
        fig = px.scatter(df, x=x, y=y)
    elif chart_type == "Pie":
        names = st.selectbox("Category", categorical_cols)
        values = st.selectbox("Values", numeric_cols)
        fig = px.pie(df, names=names, values=values)

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # AI INSIGHTS
    # ---------------------------
    if st.button("Generate AI Insights"):
        data_sample = df.head(20).to_dict()
        prompt = f"Analyze this dataset and give 2-3 short actionable insights:\n{data_sample}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        insights = response['choices'][0]['message']['content']
        st.markdown("### AI Insights")
        st.write(insights)

    # ---------------------------
    # DOWNLOAD OPTION
    # ---------------------------
    st.download_button(
        label="Download Chart as HTML",
        data=fig.to_html(),
        file_name="chart.html",
        mime="text/html"
    )
