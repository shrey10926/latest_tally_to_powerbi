'''
Prepare the combined csv (both sales and purchase data combined into one csv)
for PBI Dash format. We are aggregating all the sales and purchase data and
then subtracting the sales from purchase to get inventory of all the clients.
'''

import pandas as pd
import os

def pbi_csv():

  main_df = pd.read_csv('2.0\csv_files\combined.csv')

  sales_df = main_df[main_df['V_TYPE'] == 'Sales'].reset_index(drop = True)
  purchase_df = main_df[main_df['V_TYPE'] == 'Purchase'].reset_index(drop = True)

  purchase_df['QUANTITY'] = purchase_df['QUANTITY'].str.replace(' unit', '')
  sales_df['QUANTITY'] = sales_df['QUANTITY'].str.replace(' unit', '')

  purchase_df['ITEM_AMOUNT'] = purchase_df['ITEM_AMOUNT'].abs()
  sales_df['ITEM_AMOUNT'] = sales_df['ITEM_AMOUNT'].abs()

  convert_dict = {"V_No" : int, "V_TYPE" : str, "PARTYLEDGERNAME" : str, "ITEM_NAME" : str, "ITEM_AMOUNT" : float, "QUANTITY" : int}#, "rate" : float

  purchase_df.drop(['RATE', 'TOTAL_BILLED_AMOUNT', 'PLACEOFSUPPLY', 'STATE', 'RATE', 'NARRATION'], inplace = True, axis = 1)
  purchase_df = purchase_df.astype(convert_dict)

  sales_df.drop(['RATE', 'TOTAL_BILLED_AMOUNT', 'PLACEOFSUPPLY', 'STATE', 'RATE', 'NARRATION'], inplace = True, axis = 1)
  sales_df = sales_df.astype(convert_dict)

  purchase_df1 = purchase_df.groupby(['PARTYLEDGERNAME', 'ITEM_NAME']).agg({
                                            'DATE' : 'first', 'V_TYPE' : 'first', 'V_No' : 'first',
                                            'PARTYLEDGERNAME' : 'first', 
                                            'ITEM_NAME' : 'first', 'QUANTITY' : 'sum', 'ITEM_AMOUNT' : 'sum'})

  sales_df1 = sales_df.groupby(['PARTYLEDGERNAME', 'ITEM_NAME']).agg({
                                            'DATE' : 'first', 'V_TYPE' : 'first', 'V_No' : 'first',
                                            'PARTYLEDGERNAME' : 'first', 
                                            'ITEM_NAME' : 'first', 'QUANTITY' : 'sum', 'ITEM_AMOUNT' : 'sum'})

  purchase_df1.reset_index(drop = True, inplace = True)
  sales_df1.reset_index(drop = True, inplace = True)

  try:
    tmp = purchase_df1.set_index(['PARTYLEDGERNAME', 'ITEM_NAME'])
    out = (tmp
          .sub(sales_df1.set_index(['PARTYLEDGERNAME', 'ITEM_NAME'])[['ITEM_AMOUNT', 'QUANTITY']])
          .combine_first(tmp).assign(voucher_type='Remaining')
          .reset_index()[purchase_df1.columns]
          )
    
  except Exception as e:
    print(e)


  out['V_TYPE'] = out['V_TYPE'].replace('Purchase', 'Remaining')
  out.drop(['V_No', 'DATE'], axis = 1, inplace = True)
  out['QUANTITY'] = out['QUANTITY'].abs()

  out.to_excel(os.path.join('2.0', 'csv_files', 'final_dataframe.xlsx'), index=None)

  return 'Done!'

