from urlextract import URLExtract
import matplotlib.pyplot as plt
extract=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
        
    num_messages= df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())

    num_media_msg=df[df['message']=="<Media omitted>\n"].shape[0]

    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return num_messages, len(words), num_media_msg,len(links)

def most_busy_users(df):
    x=df['user'].value_counts().head()
    name=x.index
    count=x.values
    plt.bar(name,count)
    plt.xticks(rotation="vertical" )
    
        