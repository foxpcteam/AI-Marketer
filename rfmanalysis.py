import datetime as dt
import pandas as pd
import plotly.express as px
from rfm import *
import streamlit as st
from util import p_title
from io import StringIO

def rfmanalysis(nav):
    if nav == '👑RFM Model':
        st.text('')
        p_title('👑RFM Model')
        st.text('')
        st.markdown(":white_check_mark:Identify customers who are most engaged with your products or services")
        st.write('Suggested Data : Customer ID (Identifier of Customer, Invoice Date (The date of each transaction),Amount($ amount of the each order)')
        if st.button('Get Demo Data'):
            df = pd.read_csv('./dataset/rfm.csv',encoding= 'unicode_escape')
            st.write(df.head(10))
            with st.spinner('Training model...'):
            #Setup 
                r = RFM(df, customer_id='CustomerID', transaction_date= 'InvoiceDate', amount='Amount')

            #Visualization 
                st.title('Visualization')
                #Output dataframe with "segment" column
                st.dataframe(r.customer_df)
                #Output barchart
                segment_df = r.segment_df
                #segment_df['segment'][::-1]
                #segment_df['no of customers'][::-1]
                st.title('Distribution of user group')
                fig = px.bar(segment_df,x="segment",y="no of customers")
                st.plotly_chart(fig)
                #['Champions', 'Loyal Accounts', 'Low Spenders', 'Potential Loyalist', 'Promising', 'New Active Accounts', 'Need Attention', 'About to Sleep', 'At Risk', 'Lost']
                
        else:
            uploaded_file = st.file_uploader("Choose a file",key=rfm)
            if uploaded_file is not None:
                # To read file as bytes:
                bytes_data = uploaded_file.getvalue()
                #st.write(bytes_data)

                # To convert to a string based IO:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                #st.write(stringio)

                # To read file as string:
                string_data = stringio.read()

                # Can be used wherever a "file-like" object is accepted:
                df = pd.read_csv(uploaded_file,encoding= 'unicode_escape')
                st.write(df.head(10))
                example_customer = 'CustomerID'
                customer = st.text_input('Input the customer ID column name',example_customer)
                example_transcation = 'InvoiceDate'
                transcation = st.text_input('Input the Invoice Date column name',example_transcation)
                example_amount = 'Amount'
                amount = st.text_input('Input the invoice amount column name',example_amount)            
                #User input
                if st.button('Submit') :
                    with st.spinner('Training model...'):
                #Setup 
                        r = RFM(df, customer_id=customer, transaction_date= transcation, amount=amount)

                    #Visualization 
                        st.title('Visualization')
                        #Output dataframe with "segment" column
                        st.dataframe(r.customer_df)
                        #Output barchart
                        segment_df = r.segment_df
                        #segment_df['segment'][::-1]
                        #segment_df['no of customers'][::-1]
                        st.title('Distribution of user group')
                        fig = px.bar(segment_df,x="segment",y="no of customers")
                        st.plotly_chart(fig)
                        #['Champions', 'Loyal Accounts', 'Low Spenders', 'Potential Loyalist', 'Promising', 'New Active Accounts', 'Need Attention', 'About to Sleep', 'At Risk', 'Lost']
                        
                        
                        @st.cache
                        def convert_df(df):
                            # IMPORTANT: Cache the conversion to prevent computation on every rerun
                            return df.to_csv().encode('utf-8')

                        csv = convert_df(r.customer_df)

                        st.download_button(
                            label="Download data as CSV",
                            data=csv,
                            file_name='rfm_analysis.csv',
                            mime='text/csv',
                        )
