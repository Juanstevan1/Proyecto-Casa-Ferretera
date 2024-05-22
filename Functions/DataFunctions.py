import pandas as pd

def extracting_data(source_file, workers_direction, incentivos):
    columns=["Fecha", "Referencia", "Valor neto", "Vendedor","Nombre vendedor", "MARCA" ]
    df=source_file
    temporal=df.copy()
    temporal['Fecha']=pd.to_datetime(df['Fecha'], errors='coerce').dt.normalize()
    temporal=temporal.dropna(subset=["Fecha"])
    oldest_date=temporal['Fecha'].min()
    newest_date = temporal['Fecha'].max()
    workers_df=workers_direction
    workers_df=workers_df[["Nombre vendedor", "AREA"]]
    extracted_df=df[columns].copy()
    new_file=extracted_df.merge(workers_df, how='left', on='Nombre vendedor')
    new_file=new_file[1:]
    new_file=new_file.drop(columns=['Nombre vendedor'])
    bonus_file=incentivos
    new_file=new_file.groupby(['AREA'])['Valor neto'].sum().reset_index()
    for i in bonus_file.index:
        bonus_1=bonus_file.iloc[i,0]
        #print(new_file['AREA'])
        #print(new_file['AREA'].str.contains(bonus_1))
        filtered_df = new_file[new_file['AREA'].str.contains(bonus_1,case=False)]
        parametro=0
        total=filtered_df['Valor neto'].sum()
        meta=bonus_file.loc[i,'Meta']
        if total>=meta:
            parametro=1
        num=total*100/meta
        new_file.loc[new_file['AREA']==bonus_1, 'Condicion']=parametro
        new_file.loc[new_file['AREA'] == bonus_1, 'Porcentaje'] = int(round(num))
    #new_file=new_file[new_file["AREA"]=="PTO. VENTA PALACE"]
    #print(new_file)
    new_file=new_file.dropna(subset=['Condicion'])
    new_file=new_file.merge(bonus_file,how='left', on='AREA')
    new_file['initial_time']=oldest_date
    new_file['end_time'] = newest_date
    #with pd.ExcelWriter(destination_file, engine='openpyxl') as writer:
     #   new_file.to_excel(writer, index=False)
    return new_file, oldest_date, newest_date