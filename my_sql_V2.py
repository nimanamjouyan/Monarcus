from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv('D:/SQL Test Capgemini/road-crash-data-2015/2015_DATA_SA_Casualty.csv')
# Optional, set your indexes to get Primary Keys
# df = df.set_index(['COL A', 'COL B'])

engine = create_engine('mysql+pymysql://root:nima@localhost:3306/sakila', echo=False)

df.to_sql('alpha_t', engine, index=False)