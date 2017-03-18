import pandas as pd




data = pd.read_excel('todb.xlsx')
data = data.astype(pd.np.object)

print(data.info())

syns = pd.read_excel('syns.xlsx')
syns = syns.astype(pd.np.object)


print(syns.info())

def extract_species(x):
    ns = x.replace('together with', '').strip().lower()
    alist = map(str.strip, ns.split('@'))
    return list(filter(lambda x: len(x)>0, alist))


res=[]
for ind, row in data.iterrows():
    #if not pd.isnull(row['comment']):
    #    res = extract_species(row['comment'])
    #    print(ind, res)
    res.append(len(str(row['ecology'])))



print(pd.np.argsort(res))
print(pd.np.array(res)[pd.np.argsort(res)])    
