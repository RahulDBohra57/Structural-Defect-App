import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import google.generativeai as genai
from PIL import Image
import datetime as dt

# configure the model
gemini_api_key = os.getenv('GOOGLE_API_KEY1')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Lets create a sidebar for image upload
st.sidebar.title(':red[UPLOAD THE IMAGE HERE:]')
uploaded_image = st.sidebar.file_uploader('Image',type=['jpeg','jpg','png','jfif'],accept_multiple_files=True)

uploaded_image = [Image.open(img) for img in uploaded_image]
if uploaded_image:
    st.sidebar.success('Image has been uploaded successfully')
    st.sidebar.subheader(':blue[Uploaded Image]')
    st.sidebar.image(uploaded_image)
    
# Lets create the main page
st.title(':orange[STRUCTURAL DEFECT:] :blue[AI Assisted Structural Defects Identifier]')
st.markdown('#### :green[This application takes the images of the structural defects from the construction site and prepares the AI assisted report.]')
title = st.text_input('Enter the title of the report:')
name = st.text_input('Enter the name of the person who is preparing the report:')
desig = st.text_input('Enter the designation of the person who is preparing the report:')
org = st.text_input('Enter the name of the organization:')

if st.button('SUBMIT'):
    with st.spinner('Processing...'):
        prompt = f'''
        <Role> You are and expert structural engineer with 20+ years experience in construction industry
        <Goal> You need to prepare a detailed report on the structural defect shown in the images provided by the user.
        
        <Context> The images shared by the user has been attached.
        
        <Format> 
        * Add title at the top of the report. The title provided by the user is {title}
        * Next add name, designation, organization ọf the person who has prepared the report. Also include the date when the report is prepared. 
        Following are the details provided by the user:
        - name: {name}
        - designation: {desig}
        - organization: {org}
        - date: {dt.datetime.now().date()}
        * Identify and classify the defect. For eg: crack, spalling, corossion, honeycombing, etc.
        * There could be more than one defects in images. Identify all defects seperately.
        * For each defect identified, provide a short description of the defect and its potential impact on the structure.
        * For each defect measure the sevearity as low, medium or high. Also mention if the defect is inevitable or not.
        * Provide the short-term and long-term solution for the repair along with an estimated cost in INR and estimated time.
        * What precautionary measures can be taken to avoid these defects in future.
        
        <Instructions>
        * The report generated should be in word format.
        * Use bullet points and table wherever possible.
        * Make sure the report does not exceeds 3 pages.
        '''
        
        response = model.generate_content([prompt,*uploaded_image],
                                          generation_config={'temperature':0.9})
        
        st.markdown(response.text)
        
    if st.download_button(label='Download Report',
                        data=response.text,
                        file_name='structural_defect_report.text',
                        mime='text/plain'):
        st.success('Your file is downloaded')