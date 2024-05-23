import pandas as pd
from pymongo import MongoClient

def extracting_data(source_file, brand):
    client = MongoClient(
        'mongodb+srv://Example:12345@casa.lvwjpfm.mongodb.net/?retryWrites=true&w=majority&appName=Casa')

    db = client["Casa"]

    collection = db["Usuarios2"]
    columns=["Fecha", "Referencia", "Valor neto", "Vendedor","Nombre vendedor", "MARCA" ]
    df=source_file
    temporal=df.copy()
    temporal['Fecha']=pd.to_datetime(df['Fecha'], errors='coerce')
    temporal=temporal.dropna(subset=["Fecha"])
    oldest_date=temporal['Fecha'].min()
    newest_date = temporal['Fecha'].max()
    print(oldest_date, newest_date)
    workers_df=collection.find()
    workers_df=list(workers_df)
    workers_df=pd.DataFrame(workers_df)
    workers_df=workers_df.drop('_id',axis=1)
    workers_df = workers_df.drop('cedula', axis=1)
    workers_df=workers_df.rename(columns={'Nombre':'Nombre vendedor'})
    extracted_df=df[columns].copy()
    new_file=extracted_df.merge(workers_df, how='left', on='Nombre vendedor')
    new_file=new_file[1:]
    new_file=new_file.drop(columns=['Nombre vendedor'])
    collection2=db['Statistics2']
    bonus_file=collection2.find({'end_time':{'$gt':oldest_date}, 'Marca': brand})
    new_file=new_file.groupby(['Area'])['Valor neto'].sum().reset_index()
    ids=[doc['_id'] for doc in bonus_file]
    extracted_df=extracted_df.groupby(['Nombre vendedor'])['Valor neto'].sum().reset_index()
    print(bonus_file)
    for id in ids :

        #print(new_file['AREA'])
        #print(new_file['AREA'].str.contains(bonus_1))
        instance=collection2.find_one({'_id':id})
        parametro=0
        try:
            filtered_df=extracted_df[extracted_df['Nombre vendedor'].str.contains(instance['Nombre'], case=False)]
            print(instance['Nombre'])
            total=filtered_df['Valor neto'].sum()
        except:
            filtered_df = new_file[new_file['Area'].str.contains(instance['Area'],case=False)]
            print(instance['Area'])
            total=filtered_df['Valor neto'].sum()
        meta=instance['Meta']
        if total>=meta:
            parametro=1
        num=total*100/meta
        query={'_id':id}
        new_values={'$set':{'last_date':newest_date, 'Porcentaje':round(num)}}
        
        collection2.update_one(query, new_values)
        try:
            new_file.loc[new_file['Area']==instance['Area'], 'Condicion']=parametro
            new_file.loc[new_file['Area'] == instance['Area'], 'Porcentaje'] = num
            new_file.loc[new_file['Area'] == instance['Area'], 'Meta'] = meta
        except:
            data={'Area': instance['Nombre'], 'Valor neto': meta, 'Condicion':parametro, 'Porcentaje':round(num), 'Meta':meta}
            new_file=new_file.append(data, ignore_index=True)
            
    print()
    new_file=new_file.dropna(subset=['Condicion'])
    print(new_file[new_file['Area'].str.contains('GONZALEZ TORRES LUIS CRISTOFER',case=False)])
    
    #with pd.ExcelWriter(destination_file, engine='openpyxl') as writer:
        #   new_file.to_excel(writer, index=False)
    return new_file, oldest_date, newest_date
    #new_file=new_file[new_file["AREA"]=="PTO. VENTA PALACE"]
    #print(new_file)

