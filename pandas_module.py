import pandas as pd
import numpy as np
import traceback

def format_registry_data(df:pd.DataFrame) -> pd.DataFrame:
    #used for Excel export

    #--DATA CLEANING--
    df['subnrinreg'] = df['subnrinreg'].fillna(0)
    df['termen_data'] = df['termen_data'].fillna('')
    df['dtinregemit'] = df['dtinregemit'].fillna('')
    df['dtrepar'] = df['dtrepar'].fillna('')
    df['dtinregdest'] = df['dtinregdest'].fillna('')
    df['dtinreg_cnx'] = df['dtinreg_cnx'].fillna('')

    df['nrinreg'] = df.apply(ceck_for_subreg, axis=1)
    df['Conținut'] = df.apply(parse_description, axis=1)

    df['dtinreg'] = pd.to_datetime(df['dtinreg'], errors='coerce').dt.strftime('%d-%m-%Y').fillna('')
    df['termen_data'] = pd.to_datetime(df['termen_data'], errors='coerce').dt.strftime('%d-%m-%Y').fillna('')
    df['dtinregemit'] = pd.to_datetime(df['dtinregemit'], errors='coerce').dt.strftime('%d-%m-%Y').fillna('')
    df['dtrepar'] = pd.to_datetime(df['dtrepar'], errors='coerce').dt.strftime('%d-%m-%Y').fillna('')
    df['dtinregdest'] = pd.to_datetime(df['dtinregdest'], errors='coerce').dt.strftime('%d-%m-%Y').fillna('')
    df['dtinreg_cnx'] = pd.to_datetime(df['dtinreg_cnx'], errors='coerce').dt.strftime('%d-%m-%Y').fillna('')

    #axis=0(index), 1(column)
    df.drop(columns=['iddoc','utilizator','last_update'], inplace=True)
    df.rename(columns={
        'nrinreg': 'Număr',
        'dtinreg': 'din data',
        'emitent': 'Emitent',
        'destinatar': 'Destinatar',
        'repartizat': 'Compartimentul căruia i s-a repartizat documentul',
        'solras_data': 'Data expedierii',
        'inddos': 'Indicator nomenelator',
    }, inplace=True, errors='raise')

    #reorder reassigning the dataframe
    df = df[['Număr','din data','Emitent','Conținut','Compartimentul căruia i s-a repartizat documentul',
            'Data expedierii','Destinatar','Indicator nomenelator']]
    return df

def ceck_for_subreg(row: pd.Series) -> str:
    #used to modify nrinreg based of subnrinreg (if exists)
    if row['subnrinreg']>0:
        row['nrinreg'] = f"{row['nrinreg']}/{row['subnrinreg']}"
    return row['nrinreg']

def parse_description(row: pd.Series) -> str:
    #used to build the right description based on inties (I/E)
    description:str = ''
    if row['inties'] == 'I':
        description = row['continut_int']
    else:
        description = row['continut_ies']
    return description

def get_registry_data(records:list[dict])->pd.DataFrame:
    #convert data into data frame for clean/export
    #axis 0 = columns, axis 1 = rows

    df = pd.DataFrame(records, columns=["iddoc","nrinreg","dtinreg","subnrinreg","subdtinreg","inties","modintrare","tipintrare","termen_zile","termen_data","emitent","emailemitent","nrinregemit","dtinregemit","destinatar","emaildestinatar","compartiment_ies","continut_int",
            "continut_ies","repartdanu","repartizat","dtrepar","tipiesire","modexp","solras_danu","solras_data","nrinregdest","dtinregdest","nrinreg_cnx","dtinreg_cnx","inddos","mot_anul","stare","utilizator","last_update"
    ])
    return df
