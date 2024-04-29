def extracting_data(source_file, store_at, workers_direction):
    destination_file=store_at+r"\destination.xlsx"
    columns=["Fecha", "Referencia", "Valor neto", "Vendedor","Nombre vendedor", "MARCA" ]
    df=pd.read_excel(source_file)
    workers_df=pd.read_excel(workers_direction)
    workers_df=workers_df[["Nombre vendedor", "AREA"]]
    extracted_df=df[columns].copy()
    new_file=extracted_df.merge(workers_df, how='left', on='Nombre vendedor')
    new_file=new_file[1:]
    print(new_file)
    with pd.ExcelWriter(destination_file, engine='openpyxl') as writer:
        new_file.to_excel(writer, index=False)
    return destination_file