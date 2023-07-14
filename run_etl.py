import os
import pandas as pd
from dotenv import load_dotenv
from etl.etl_pipeline import  RentasETL

load_dotenv()

#db_name = os.getenv("BTC_DB")
#table_btc_price_history = os.getenv("BTC_PRICE_TABLE")
#table_rolling_price_history = os.getenv("ROLLING_PRICE_TABLE")
#bitcoin_name = os.getenv("COIN_BTC_NAME")
#vs_currency= os.getenv("VS_CURRENCY")
#from_timestamp = os.getenv("FROM_DATE")
#to_timestamp = os.getenv("TO_DATE")
#precision =os.getenv("PRECISION")


def main():
    etl = RentasETL('vehiculos.csv', 'puntos_renta.csv', 'clientes.csv', 'rentas.csv')
    etl.run()


if __name__ == "__main__":
    main()