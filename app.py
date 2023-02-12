import csv
import openai
import pandas as pd
import base64 
import time
import streamlit as st


#variables
timestr = time.strftime("%Y%m%d-%H%M%S")


# Downaloaer function
def csv_downloader(data):
	csvfile = data.to_csv()
	b64 = base64.b64encode(csvfile.encode()).decode()
	new_filename = "completed_ai_file_{}_.csv".format(timestr)
	st.markdown("#### Download File ###")
	href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
	st.markdown(href,unsafe_allow_html=True)


#strealit frontend
st.title("Text Classifer")
st.markdown("""---""") 
st.subheader("1. Please Enter you OpenAI API key")
url = "https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key"
api = st.text_input("If you don't know your OpenAI API key click [here](%s)." % url, type="password", placeholder="Your API Key")
st.write("If you don't know your OpenAI API key click [here](%s" % url)
st.markdown("""---""")
st.subheader("2. Please input the required informaiton:")
classifiers =st.text_input("Please identify your classifers.👇")
csv_title = st.text_input("Select a lable for your classification:")
docx_file = st.text_area("Paste you input here.👇")

# Check Openai Key
if st.button("Classify!"):
    openai.api_key = api 
    try:
        # Send a test request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="What is the capital of France?",
            temperature=0.5
    )
        st.markdown("""---""")
        st.success("API key is valid!")
    
    except Exception as e:
        st.error("API key is invalid: {}".format(e))
    
    #AI computation backend
    if docx_file is not None:
        with st.spinner(text="Processing..."):
                lines = docx_file.split("\n")
                with open('output.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Content', csv_title])
                    for line in lines:
                        response = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt=(f"Is the following text related to or involve {classifiers}? {line}"),
                            max_tokens=70,
                            temperature=0.2,
                            top_p=1,
                            frequency_penalty=1,
                            presence_penalty=1
                        )

                        # parse the API response
                        output = response["choices"][0]["text"].strip()
                        
                        # write the data to the CSV file
                        writer.writerow([line.strip(), output])
                df = pd.read_csv("output.csv")
                csv_downloader(df)
                

                






