#Function1:
def return_stop_wards():
    stop_words = ['kuba','cyangwa','ariko','hari','iza','aba', 'abo', 'aha', 'aho', 'ari', 'ati', 'aya', 'ayo', 'ba', 'baba', 'babo', 'bari', 'be', 'bo', 'bose',
            'bw', 'bwa', 'bwo', 'by', 'bya', 'byo', 'cy', 'cya', 'cyo', 'hafi', 'ibi', 'ibyo', 'icyo', 'iki',
            'imwe', 'iri', 'iyi', 'iyo', 'izi', 'izo', 'ka', 'ko', 'ku', 'kuri', 'kuva', 'kwa', 'maze', 'mu', 'muri',
            'na', 'naho','nawe', 'ngo', 'ni', 'niba', 'nk', 'nka', 'no', 'nta', 'nuko', 'rero', 'rw', 'rwa', 'rwo', 'ry',
            'rya','ubu', 'ubwo', 'uko', 'undi', 'uri', 'uwo', 'uyu', 'wa', 'wari', 'we', 'wo', 'ya', 'yabo', 'yari', 'ye',
            'yo', 'yose', 'za', 'zo','kandi','cyane','kw','kugirango','ubwo','ibyo',' ','abayobozi','abanyamuryango','inteko rusange','intekorusange','urubyiruko','gahunda','akagari','akagali','umudugudu','inzego',
                'inzego zumuryango',"inzego z'umuryango",'hagati',"hagati y'inzego",'umuryango',"gahunda z'umuryango",'uruhare','kutagira','abaturage',
                'gihe','inshingano','bamwe','nshingano','inzego','nzego','hari','ubuyobozi','ababyeyi','uruhare','bwite','abantu','ahantu','kuba',
                'inama','leta','neza','rusange','igihe','gushaka','kubera',"nzego z'umuryango",'igihugu','kugira','inteko','ibibazo',
                'uburyo','bikorwa','nama','akenshi','ntabwo','ikigo','bitewe','zabo','bigatuma','imbere','umwanya','kudaha','budahagije','imbaraga','kongera',
                'ndetse','imbaraga','gukomeza','buri','gushyiraho','gukomeza','gushyira','gukora','guha','kunoza','guha','gutanga','kuzamura','inkotanyi','gukunda']
    return stop_words
def gen_keywords(df,col,stop_words):
    kwds1=[]
    import yake
    for text in df[col].values:
        kw_extractor = yake.KeywordExtractor()
        keywords = kw_extractor.extract_keywords(text)
        arr=[]
        for k in keywords:
            arr.append(k[0])
        kwds1.append(set(arr))
    keywords=[]
    for d in kwds1:
        output_strings = []
        for input_string in d:
            words = input_string.split()  # Split the string into words
             
            if words and "’" in words[0]:
                words[0]=words[0].split("’")[1]
            if words and "'" in words[0]:
                words[0]=words[0].split("'")[1]
            if words and words[0] in stop_words:
                words=[' ']
            if words:
                t=0
                for x in words[-1]:
                    if x in 'aeiou':
                        t+=1
                if t<=1:
                    words=[' ']
            if words:
                t=0
                for x in words[0]:
                    if x in 'aeiou':
                        t+=1
                if t<=1:
                    words=[' '] 
            output_strings.append(" ".join(words))
        keywords.append([x for x in output_strings])
    return keywords

#Function 2:
def gen_data_fields2(X, keywords, stop_words):
    df = X.dropna()
    data_fields = [df[col].values for col in df.columns]
    num_fields = len(data_fields)
    field_lists = [[] for _ in range(num_fields + 1)]
    for values in zip(*data_fields, keywords):
        for input_string in values[-1]:
            if input_string.lower() in stop_words:
                continue
            else:
                field_lists[-1].append(input_string)
                for field_list, value in zip(field_lists[:-1], values[:-1]):
                    field_list.append(value)
    
    return field_lists
def gen_data_fields1(X,keywords,stop_words):
    df=X.dropna()
    d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12=[df[col].values for col in df.columns]
    f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13=[],[],[],[],[],[],[],[],[],[],[],[],[]
    for d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13 in zip(d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,keywords):
        for input_string in d13:
            if input_string.lower() in stop_words:
                continue  
            else:
                f13.append(input_string)
                for key,value in zip([f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12],[d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]):
                    key.append(value)
    return [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13]
#Function 3
def update_DF(fields,list_fields,empty_df):
    import pandas as pd
    da=empty_df
    i=0
    for col in fields:
        da[col]=list_fields[i]
        i+=1
    return da

#function 4: 
def rename_keywords(df,col,dfmapa,col_map):
    dfmapa[col_map]=dfmapa[col_map].str.lower()
    d={}
    for k,x in zip(dfmapa[col_map].values,dfmapa[col_map].values):
        d[k]=x
    df[col]=df[col].str.lower()
    df['mapped_keywords']=df[col].apply(lambda x: d[x] if x in d.keys() else np.NaN)
    return df
#Function 3:
def clean_keywords(df,dfmapa):
    dfmapa=dfmapa.dropna()
    dfmapa['keywords']=dfmapa['keywords'].str.lower()
    df['keywords']=df['keywords'].str.lower() 
    for x in df['keywords'].values:
        for key in dfmapa['keywords'].values:
            if key in x.split():
                df.loc[df['keywords'] == x, 'keywords'] = key
    df=df.drop_duplicates()
    return df
#Function 4: 
def remove_special_character(df,columns):
    import re
    def remove_special_chars(text):
        pattern = r'[^a-zA-Z0-9(),\';.\s]'  # This pattern keeps letters, numbers, and spaces
        clean_text = re.sub(pattern, '', text)
        return clean_text
    for col in columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].apply(remove_special_chars)

    return df
    
#Function 5:
def remove_extra_spaces(df,columns):
    for col in columns:
        df[col] = df[col].str.strip()
    return df

#Function 6:
def map_keywords(df,dat,questions):
    dat['keywords']=dat['keywords'].str.lower()
    df['keywords']=df['keywords'].str.lower() 
    
    d1,d2,d3,d4={},{},{},{}
    i=0
    for x,d in zip([dat[dat.columns[1]].values,dat[dat.columns[2]].values,dat[dat.columns[3]].values,dat[dat.columns[4]].values],(d1,d2,d3,d4)):
        for k,m in zip(dat['keywords'].values,x):
            d[k]=m
        i=i+1
    i=0
    for qs in list(set(df['icyabajijwe'].values)):
        if qs==questions[0]:
            df1=df[df['icyabajijwe']==qs]
            for x in df1['keywords'].values:
                for key,value in zip(d1.keys(),d1.values()):
                    if key in str(x).split():
                        df1.loc[df1['keywords'] == x, 'keywords'] = value
        elif qs==questions[1]:
            df2=df[df['icyabajijwe']==qs]
            for x in df2['keywords'].values:
                for key,value in zip(d2.keys(),d2.values()):
                    if key in str(x).split():
                        df2.loc[df2['keywords'] == x, 'keywords'] = value
        elif qs==questions[2]:
            df3=df[df['icyabajijwe']==qs]
            for x in df3['keywords'].values:
                for key,value in zip(d3.keys(),d3.values()):
                    if key in str(x).split():
                        df3.loc[df3['keywords'] == x, 'keywords'] = value
        elif qs==questions[3]:
            df4=df[df['icyabajijwe']==qs]
            for x in df4['keywords'].values:
                for key,value in zip(d4.keys(),d4.values()):
                    if key in str(x).split():
                        df4.loc[df4['keywords'] == x, 'keywords'] = value
        else:
            continue
        i=i+1
    df=pd.concat([df1,df2,df3,df4],axis=0)
    df=df.drop_duplicates()
    return df

    #Function 7: 
def keywords_counts(df,col):
    keyword_counts = df[col].value_counts()
    return keyword_counts

#Function 8:

def return_df_with_seled_kwds(df,data):
    keywords=[]
    for x in [data[data.columns[1]].values,data[data.columns[2]].values,data[data.columns[3]].values,data[data.columns[4]].values]:
        for x2 in x:
            keywords.append(x2)  
    df2=df[df['keywords'].isin(keywords)]
    return df2

# Function 9: 
def counts_20_top_kwds_frequency(keywords_counts,df7,questions):
    i=1
    for y in questions:
        print('Questions{}:\n{}'.format(i,y))
        i=i+1
        print()
        print(keywords_counts(df7[df7['icyabajijwe']==y],'keywords')[:20])
        print()
#Function 10:
def return_df_with_unkown_kwds(df,data):
    keywords=[]
    for x in [data[data.columns[1]].values,data[data.columns[2]].values,data[data.columns[3]].values,data[data.columns[4]].values]:
        for x2 in x:
            keywords.append(x2)  
    df2=df[~df['keywords'].isin(keywords)]
    return df2