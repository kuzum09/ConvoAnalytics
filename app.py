import streamlit as st
import preprocessor 

st.sidebar.title('ConvoAnalytics')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data =bytes_data.decode("utf-8")
    # st.text(data)

    df=preprocessor.preprocess(data)
    st.dataframe(df)
