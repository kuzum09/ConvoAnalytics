import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.sidebar.title('ConvoAnalytics')

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
    

        

        if selected_user=='Overall':
            st.title ('Most Busy User ')
            x,new_df=helper.most_busy_users(df)

            fig,ax=plt.subplots()
           
            col1, col2 = st.columns(2)

            with col1:
                  ax.bar(x.index,x.values)
                  plt.xticks(rotation='vertical')
                  st.pyplot(fig)
            with col2:
                  st.dataframe(new_df)
        st.title('Word Cloud')
        df_wc=helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
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



        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



