import re
import pandas as pd

def preprocess(data):
    # Preprocess the data
    pattern = r'\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s?[apAP][mM]\s-\s'

    messages=re.split(pattern, data)[1:]
    dates=re.findall(pattern, data)
    

    df=pd.DataFrame({ 'user_message':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={'message_date':'date'}, inplace=True)


    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1: ]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df['month_num']=df['date'].dt.month
    df.drop(columns=['user_message'], inplace=True)
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['only_date']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period = []

# Ensure the DataFrame contains 'hour' as an integer column
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")


    df['period']=period

    return df


