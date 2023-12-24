import streamlit as st
from io import StringIO
from anti_plagiarism import predicting_functions, Model, give_pandas
from backend import model
from backend.metrics import *

st.set_page_config(page_title="Antiplagiarism checker", page_icon="👋", layout='wide')
st.write('## Evaluation of metrics for comparison of two (python) files from the point of plagiarism')

uploaded_file = st.sidebar.file_uploader('Put your files here', accept_multiple_files=True)
metrics = st.sidebar.multiselect('Choose metrics to use', predicting_functions.keys())

if uploaded_file and metrics:

    files = {file.name: StringIO(file.getvalue().decode("utf-8")).getvalue() for file in uploaded_file}

    parse_python: bool = all(file.endswith('.py') for file in files.keys())
    model = Model(parse_python, metrics)

    if not parse_python and any(file.endswith('.py') for file in files.keys()):
        st.write('Not all files in folder have extension .py, we compare them as pure strings')
    if parse_python:
        files_temp = {}
        for key, value in files.items():
            files_temp[key] = model.preprocessing_code(value)
        files = files_temp
        del files_temp

    results = model.compare(files)
    df = give_pandas(results, metrics)

    st.write(f'metrics increasing from plagiarism: '
                f'{[metric for metric in metrics if metric in increasing_from_plagiarism]}')

    st.write(f'metrics decreasing from plagiarism: '
                f'{[metric for metric in metrics if metric not in increasing_from_plagiarism]}')


    st.write("Results are: ")
    st.write(df)

    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        "Press to Download results",
        csv,
        "comparison.csv",
        "text/csv",
        key='download-csv'
    )