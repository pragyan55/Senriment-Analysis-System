import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px


st.title("AMAZ0N ANALYSIS SYSTEM")

choice=st.sidebar.selectbox("My Menu", ("HOME", "ANALYSIS","RESULTS"))
if (choice == "HOME"):
    st.image("https://miro.medium.com/v2/1*_JW1JaMpK_fVGld8pd1_JQ.gif")
    st.write("1.It is a Natural Language Processing Application which can analyze the sentiment on a text data.")
    st.write("2. This application predicts the sentiment into 3 categories Positive, Negative and Neutral.")
    st.write("3.This Application then visualizes the results based on different factors such as name,description,rating star and manymore.")
elif (choice == "ANALYSIS"):
    sid=st.text_input("Enter your Google Sheet ID")
    r=st.text_input("Enter Range between first column and last columns")
    c=st.text_input("Enter column name that is to be analyzed")
    btn=st.button("Analyze")
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file("key.json", ["https://www.googleapis.com/auth/spreadsheets"])
            st.session_state['cred']=f.run_local_server (port=0)
        mymodel=SentimentIntensityAnalyzer()
        service=build("Sheets", "v4", credentials=st.session_state['cred']).spreadsheets().values()
        k=service.get(spreadsheetId=sid, range=r).execute()
        d=k['values']
        df=pd.DataFrame(data=d[1:], columns=d[0])
        l=[]
        for i in range(0,len(df)):
            t=df._get_value(i,c)
            pred=mymodel.polarity_scores(t)
            if(pred['compound' ]>0.5):
                l.append("Positive")
            elif (pred['compound' ]<-0.5):
                l.append("Negative")
            else:
                l.append("Neutral")
        df['Sentiment']=l
        df.to_csv("results.csv",index=False)
        st.subheader("The Analysis results are saved by the name of a results.csv file")
elif(choice=="RESULTS"):
    df=pd.read_csv("results.csv")
    choice2=st.selectbox("Choose Visualization", ("NONE", "PIE CHART", "HISTOGRAM", "SCATTER PLOT"))
    st.dataframe (df)
    if (choice2=="PIE CHART"):
        posper=(len (df [df[ 'Sentiment'] == 'Positive'])/len (df))*100
        negper=(len(df [df[ 'Sentiment']=='Negative'])/len (df))*100
        neuper=(len(df [df['Sentiment']=='Neutral'])/len (df))*100
        fig=px.pie(values = [posper, negper, neuper], names=['Positive', 'Negative', 'Neutral'])
        st.plotly_chart(fig)
    elif (choice2=="HISTOGRAM"):
        k=st.selectbox("Choose column", df.columns)
        if k:
            fig=px.histogram (x=df[k], color=df[ 'Sentiment'])
            st.plotly_chart(fig)
    elif (choice2=="SCATTER PLOT"):
        k=st.text_input("Enter the continous column name")
        if k:
            fig=px.scatter (x=df[k],y=df[ 'Sentiment'])
            st.plotly_chart(fig)
