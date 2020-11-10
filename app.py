
#region imports

import streamlit as st
from streamlit import _beta_warning
import waybackpy
import pandas as pd
import csv
import base64

import requests
from requests.exceptions import ConnectionError

#endregion imports

#region Top area

def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

#endregion Top area ############################################################

#region headers

c30, c31, c32 = st.beta_columns(3)

#with c30:
#    st.image('StreamSuggestLogo.png', width = 325 )

with c32:
  st.header('')
  st.header('')
  st.markdown('###### Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/)&nbsp, with :heart: by [@DataChaz](https://twitter.com/DataChaz) &nbsp [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/cwar05)')


with st.beta_expander("ℹ️ - About this app ", expanded=False):
  st.write("""  

- StreamSuggest retrieves auto-complete suggestions from Google and
   Bing at scale! 🔥
-   The tool is in Beta. Feedback & bug spotting are welcome. [DMs are open!](https://twitter.com/DataChaz)
-   This app is free. If it's useful to you, you can [buy me a coffee](https://www.buymeacoffee.com/cwar05) to support my work! 🙏

-   'Add try with ConnectionError, means theres at least one incorrect URL')
-   'dupe + URLs missing https are removed')
-   'non 200 are removed')
-   "Return the closest Wayback Machine archive to the time supplied. Supported params are year, month, day, hour and minute. Any non-supplied parameters default to the current time.") """)

with st.beta_expander("🛠️ - URLs", expanded=False):
	    st.write("""
-   https://www.ranksense.com/
-   https://www.tatielou.co.uk/
-   https://www.google.com/
-   https://www.charlywargnier.com/
-   https://www.searchengineland.com/
-   https://searchengineland.com/
-   https://www.searchenginejournal.com/
   	    """)

#endregion headers

#region text area

st.markdown('## **① Paste some URLs **')

MAX_LINES = 5

c29, c30, c31 = st.beta_columns([1,4,1])

with c30:

    text = st.text_area("one URL per line (5 max)", height=175)
    
    if not text:
        st.stop()
    
    lines = text.split("\n")  # A list of lines

    if len(lines) > MAX_LINES:
        st.warning(f"you've exceeded the allowed number of URLs (max 5)")
        lines = lines[:MAX_LINES]
        st.stop()

    identifier_list = ('https://', 'http://')  # tuple, not list
    notHTTP = [elem for elem in lines if not elem.startswith(identifier_list)]

    if '' in lines:
        st.warning('⚠️ Remove empty line')
        st.stop()

    c = st.beta_container()     
        
    if notHTTP:

        if len(notHTTP) < 2:           
            st.warning("⚠️ The following URL -> " + str(notHTTP) + " is invalid and needs a protocol (https:// or http://) to work.")
            st.stop()
        else:
            st.warning("⚠️ The following URLs -> " + str(notHTTP) + " are invalid and need a protocol (https:// or http://) to work.")
            st.stop()

    for line in lines:
        data = pd.DataFrame({'url':lines})
        data = data.drop_duplicates(subset ="url")   

#endregion text area

#region selector

@st.cache(suppress_st_warning=True, show_spinner=False)
def get_code(row):
  name = row['url']
  return requests.get(name).status_code

try:
    data['code'] = data.apply(get_code, axis = 1)
    CodeList = [404, 500]
    
    df2 = data[~data['code'].isin(CodeList)]

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0"

    st.markdown('## **② Tick what you&#39d like to see **')
    
    c29, c30, c31, c32, c33, c34 = st.beta_columns(6)

    with c30:
        st.header("")
        check_Old = st.checkbox("Oldest cached date")

    with c31:
        st.header("")
        check_New = st.checkbox("Newest cached date")
    
    with c32:
        st.header("")
        check_Custom = st.checkbox("📅 Custom date ► ", value=True)
    
    with c33:
        d = st.date_input("")
        year =  d.strftime('%Y')
        month =  d.strftime('%m')
        day =  d.strftime('%d')

    if not text:
        c.success('Add some URLs')
        st.stop()

#endregion selector

#region Functions

    @st.cache(suppress_st_warning=True,show_spinner=False)
    def oldestCache(row):
        name = row['url']
        return waybackpy.Url(name, user_agent).oldest()

    @st.cache(suppress_st_warning=True,show_spinner=False)
    def newestCache(row):
        name = row['url']
        return waybackpy.Url(name, user_agent).newest()

    @st.cache(suppress_st_warning=True,show_spinner=False, allow_output_mutation=True)
    def near(row):
        name = row['url']
        return waybackpy.Url(name, user_agent).near(year=year,month=month,day=day)
    
    @st.cache(suppress_st_warning=True,show_spinner=False, allow_output_mutation=True)
    def Alljson(row):
        name = row['url']
        return waybackpy.Url(name, user_agent).JSON

    @st.cache(suppress_st_warning=True,show_spinner=False)
    def totalArchivesCount(row):
        name = row['url']
        return waybackpy.Url(name, user_agent).total_archives()

#endregion Functions

    df2['Archive count'] = df2.apply(totalArchivesCount, axis = 1)

    if check_New == True:
        df2['Newest cache'] = df2.apply(newestCache, axis = 1)

    if check_New == False and check_Old == False and check_Custom == False:
        st.warning('at least 1 option needed!')

    if check_Old == True:
        df2['Oldest cache'] = df2.apply(oldestCache, axis = 1)

    if check_Custom == True:
        df2['NearestCustom'] = df2.apply(near, axis = 1)

    df2.to_csv('Export.csv')

    df2 = pd.read_csv('Export.csv')

    if 'NearestCustom' in df2.columns:
        df2['NearestCopy'] = df2['NearestCustom'] 
        df2[['dateNearest','NearestCopy']] = df2["NearestCopy"].str.split("/http", 1, expand=True)
        df2['dateNearest'] = df2['dateNearest'].replace(to_replace=r'https://web.archive.org/web/', value='', regex=True)       
        df2['dateNearest']= pd.to_datetime(df2['dateNearest'])
        del df2['NearestCopy']
    else:
        pass

    if 'Oldest cache' in df2.columns:
        df2['OldestCopy'] = df2['Oldest cache'] 
        df2[['dateOldest','OldestCopy']] = df2['OldestCopy'].str.split("/http", 1, expand=True)
        df2['dateOldest'] = df2['dateOldest'].replace(to_replace=r'https://web.archive.org/web/', value='', regex=True)       
        df2['dateOldest']= pd.to_datetime(df2['dateOldest'])
        del df2['OldestCopy']
    else:
        pass
    
    if 'Newest cache' in df2.columns:

        df2['NewestCopy'] = df2['Newest cache'] 
        df2[['dateNewest','NewestCopy']] = df2['NewestCopy'].str.split("/http", 1, expand=True)
        df2['dateNewest'] = df2['dateNewest'].replace(to_replace=r'https://web.archive.org/web/', value='', regex=True)       
        df2['dateNewest']= pd.to_datetime(df2['dateNewest'])
        del df2['NewestCopy']
    else:
        pass
    
    cols = list(df2.columns.values)
    
    column_names = [
    "url",
    "code",
    "Archive count",
    "NearestCustom",
    "dateNearest",
    "Newest cache",
    "dateNewest",
    "Oldest cache",
    "dateOldest",
    ]

    df2 = df2.reindex(columns=column_names)

    try:
        csv = df2.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown('## **③ Check results or download CSV **')
        st.subheader("")
        href = f'<a href="data:file/csv;base64,{b64}" download="filtered_table.csv">** ⯈ Download link 🎁 **</a>'
        st.markdown(href, unsafe_allow_html=True)

    except NameError:
        print ('wait')

    dfOldest = df2.copy()
    dfNewest = df2.copy()
    dfNearest = df2.copy()   

    if check_Old == True: 

        try:

            column_names_01 = [
            "url",
            "code",
            "Archive count",
            "Oldest cache",
            "dateOldest",
            ]

            dfOldest = dfOldest.reindex(columns=column_names_01)

            st.subheader("dfOldest")
            st.table(dfOldest)
        except KeyError:
            pass

    if check_New == True: 
        try:
            column_names_02 = [
            "url",
            "code",
            "Archive count",
            "Newest cache",
            "dateNewest",
            ]

            dfNewest = dfNewest.reindex(columns=column_names_02)

            st.subheader("dfNewest")
            st.table(dfNewest)
        except KeyError:
            pass

    if check_Custom == True: 

        try:

            column_names_03 = [
            "url",
            "code",
            "Archive count",
            "NearestCustom",
            "dateNearest",
            ]

            dfNearest = dfNearest.reindex(columns=column_names_03)

            st.subheader("dfNearest")
            st.table(dfNearest)
        except KeyError:
            pass

except ConnectionError:
    c.warning('⚠️ At least one URL is incorrectly formed, please check your URLs.')


