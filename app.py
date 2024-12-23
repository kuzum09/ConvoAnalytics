import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns



# Custom CSS for centering the heading
st.markdown(
    """
    <style>
    .centered-heading {
        text-align: center;
        font-size: 100px; /* Increased font size for a larger heading */
        color: #indigo; /* Indigo color matching theme */
        font-weight: bold;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Adding the centered heading using a <div> tag
st.markdown('<div class="centered-heading">ConvAnalytics</div>', unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data =bytes_data.decode("utf-8")
    # st.text(data)

    df=preprocessor.preprocess(data)


    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user= st.sidebar.selectbox('Show analyst wrt',user_list)

    if st.sidebar.button("Analysis"):
        st.title('Top Statstics')

        num_messages, words, num_media_messages, num_links= helper.fetch_stats(selected_user,df)
        col1, col2, col3 ,col4 = st.columns(4)
        
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
    

        
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="#0083B8") # Set the line color here
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



        st.title('Daily Timeline')
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='#0083B8')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)




        st.title('Activity Map')
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Active Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color= "#0083B8") # Set the bar color here
            st.pyplot(fig)




        with col2:
            st.header("Most Active Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color= "#0083B8")  # Set the bar color here
            st.pyplot(fig)

        st.title('Weekly Activity Heatmap')
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap,cmap='coolwarm')
        st.pyplot(fig)

        if selected_user=='Overall':
            st.title ('Most Busy User ')
            x,new_df=helper.most_busy_users(df)

            fig,ax=plt.subplots()
           
            col1, col2 = st.columns(2)

            with col1:
                  ax.bar(x.index,x.values,color='#0083B8') # Set the bar color here
                  plt.xticks(rotation='vertical')
                  st.pyplot(fig)
            with col2:
                  st.dataframe(new_df)
        st.title('Word Cloud')
        df_wc=helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        st.pyplot(fig)

        most_common_df=helper.most_common_words(selected_user,df)

        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most Common Words')
        st.pyplot(fig)




        emoji_df=helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')
        col1, col22 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)  
        with col22:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%.2f')        
            st.pyplot(fig)



