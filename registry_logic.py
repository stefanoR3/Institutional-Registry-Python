import pymysql #used to send MySql network requests using python commands
import pandas as pd
import numpy as np
#import openpyxl
import datetime

def get_connection() -> pymysql.Connection:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='regtest',
        port = 3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor #convert tuples into dictionaries
    )
    return connection

def fetch_registry_records(start_date:datetime.date, end_date:datetime.date) -> None:
    #fetch rows trough a data range
    connection = get_connection()
    with connection.cursor() as cursor: #study cursors!
        #we prevent sql injection by not letting further instruction append
        # ''' or """ used for multi-line strings
        stmt = """SELECT iddoc, nrinreg, dtinreg, emitent, continut_int FROM registru WHERE dtinreg BETWEEN %s AND %s"""
        cursor.execute(stmt, (start_date,end_date))
        records = cursor.fetchall()
        #for record in records:
            #print(f"ID:{record['iddoc']} | Nr:{record['nrinreg']} | Date:{record['dtinreg']} |  Emitent:{record['emitent']} | continut_int:{record['continut_int']}")
            #print(type('dtinreg'))
        return records

def ceck_for_subreg(row: pd.Series) -> str:
    #used to modify nrinreg based of subnrinreg (if exists)
    #iterates trough each row, takes all the returned vales and snitches them together in a single row(pd.Series)
    #if value is returned, apply = series, else if series is returned, apply = dataframe
    if pd.notna(row['subnrinreg']) and row['subnrinreg']>0:
        row['nrinreg'] = f"{row['nrinreg']}/{row['subnrinreg']}"
    return row['nrinreg']

def convert_date_model(row: pd.Series, column_name:str) -> datetime.date:
    date:datetime.date = row[column_name]
    date.strftime("%d-%m-%Y") #you can convert from string to date too!
    return date

def format_registry_data(records:list[dict])->pd.DataFrame:
    #convert data into data frame for clean/export
    #axis 0 = columns, axis 1 = rows

    #--DATA RETRIEVE--
    df = pd.DataFrame(records, columns=["iddoc","nrinreg","dtinreg","subnrinreg","inties","modintrare",
        "dtinregemit","nrinregemit","emitent","continut_int","continut_ies","destinatar","repartizat",
        "termen","solras_data","solras_rezumat","solras_nr","solras_danu","mot_anul","dt_anul","user_anul",
        "user_inreg","dt_modific","user_modific","stare","anulat","obs","dosar","nr_file",
        ])

    #notna transform a column into a True or False mask
    #any() ceck if there is at least one True value

    #--DATA CLEANING--
    df['subnrinreg'] = df['subnrinreg'].fillna(0)
    print(df['subnrinreg'])
    df['nrinreg'] = df.apply(ceck_for_subreg, axis=1)
    df['dtinreg'] = df.apply(convert_date_model, axis=1)
    if df['termen_data'].notna().any():
        df['termen_data'] = df.apply(convert_date_model, axis=1)
    if df['dtinregemit'].notna().any():
        df['dtinregemit'] = df.apply(convert_date_model, axis=1)
    if df['dtrepar'].notna().any():
        df['dtrepar'] = df.apply(convert_date_model, axis=1)
    if df['dtinregdest'].notna().any():
        df['dtinregdest'] = df.apply(convert_date_model, axis=1)
    if df['dtinregcnx'].notna().any():
        df['dtinregcnx'] = df.apply(convert_date_model, axis=1)

    df['termen_data'] = df['termem_data'].fillna('-')
    df['dtinregemit'] = df['dtinregemit'].fillna('-')
    df['dtrepar'] = df['dtrepar'].fillna('-')
    df['dtinregdest'] = df['dtinregdest'].fillna('-')
    df['dtinregcnx'] = df['dtinregcnx'].fillna('-')

    


    
    
    

