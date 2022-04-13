import streamlit as st
import pandas as pd
import altair as alt

DATA_URL = 'claims.csv'
data = pd.read_csv(DATA_URL)
st.header("Claims Analysis")



option = st.sidebar.selectbox("What do you want to do with the data?", ("Investigate", "Data Preparation", "Data Analysis"))
st.sidebar.write("As data analysts and data scientists our roles don't just involve doing some excel analysis on data we have - there are several steps needed to understand and prepare the data before we can do any analysis. This app will walk you through the process of preparing data and analysing it!")
if option =="Investigate":
    st.write(data)
    lob = list(data["Line of Business"].unique())
    not_type = list(data["Notification Type"].unique())
    clm_sta = list(data["Claim Status"].unique())
    lob_select = st.selectbox(label = "Filter the data by Line of Business", options = lob)
    lob_df = data.loc[data["Line of Business"] == lob_select]
    st.write(lob_df)
    not_select = st.selectbox(label = "Filter by Notification Type", options = not_type)
    not_df = data.loc[data["Notification Type"] == not_select]
    st.write(not_df)
    claim_select = st.selectbox(label = "Filter by claim status", options = clm_sta)
    claim_df = data.loc[data["Claim Status"] == claim_select]
    st.write(claim_df)
 

    
if option =="Data Preparation":
    st.write(data)
    if st.checkbox("Find Duplicated Claims"):
        duplicates = data[data["Claim reference"].duplicated()]
        st.write(duplicates)
        st.write("It is really important to ensure duplicate data is removed from any data set (known as 'deduping') to preserve data quality and make sure analysis isn't skewed")


    if st.checkbox("Find incomplete claim references"):
        incomplete = data[data['Claim reference'].apply(lambda x: len(x) < 8)]
        st.write(incomplete)
        st.write("Identifying & removing or correcting invalid data is important as we often join data from multiple different sources so it is important records match - we have advanced tools to correct some invalid data but it can also be excluded")

    if st.checkbox("Remove duplicated or incomplete data"):
        duplicatedf = data.drop_duplicates(subset = "Claim reference")
        incompdup = duplicatedf[duplicatedf['Claim reference'].map(len) > 7]
        st.write(incompdup)
        st.write("We are now ready to do some data analysis")


if option =="Data Analysis":
    duplicatedf = data.drop_duplicates(subset = "Claim reference")
    incompdup = duplicatedf[duplicatedf['Claim reference'].map(len) > 7]
    st.write(incompdup)
    

    if st.checkbox("Make a bar chart"):
        st.write("Number of Claims by Line of Business")
        lob_bar_chart = alt.Chart(incompdup).mark_bar().encode(alt.X("Line of Business"),y="count()")
        st.altair_chart(lob_bar_chart,use_container_width=True)
    
        st.write("Number of Claims by Notification Type") 
        not_bar_chart = alt.Chart(incompdup).mark_bar().encode(alt.X("Notification Type"),y="count()")
        st.altair_chart(not_bar_chart, use_container_width=True)

        st.write("Number of claims by Status")
        sta_bar_chart = alt.Chart(incompdup).mark_bar().encode(alt.X("Claim Status"),y="count()")
        st.altair_chart(sta_bar_chart, use_container_width=True)

    

    if st.checkbox("Make a line chart"):
        incompdup =incompdup.replace('£', '', regex=True)
        incompdu = incompdup.replace(',', '', regex=True)
        incompdu["Notification date"] = pd.to_datetime(incompdu["Notification date"])
        incompdu["Amount Incurred"] = incompdu["Amount incurred"].astype(int)
        incompdu["Amount Paid"] = incompdu["Amount paid"].astype(int)
        month = incompdu.groupby(incompdu['Notification date'].dt.strftime('%B'))["Amount Incurred", "Amount Paid"].sum()
        months = ["4", "8", "12", "1", "7", "6", "3", "5", "11", "10", "9"]
        month["Months"]= months
        month.Months = month.Months.astype(int)
        Months = month.sort_values(by=['Months'])
        line_chart = pd.DataFrame(Months, columns = ["Amount Incurred", "Amount Paid"])
        st.line_chart(line_chart)

       
