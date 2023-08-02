import xml.etree.ElementTree as ET
import xmltodict
import json
import pandas as pd
import os
import csv


# tree = ET.parse('output_files\Sales Vouchers.xml')
# xml_data = tree.getroot()

# #here you can change the encoding type to be able to set it to the one you need
# xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

# data_dict = dict(xmltodict.parse(xmlstr))
# data = data_dict['ENVELOPE']['BODY']['IMPORTDATA']['REQUESTDATA']['TALLYMESSAGE']

# # out_file = open("myfile.json", "w")
# # op = json.dump(data, out_file, )
# # out_file.close()


#convert xml to dictionary
#WHEN I RUN THIS SCRIPT ON My PERSONAL XML FILE, THIS FINAL_DATA LIST COMES OUT AS EMPTY AND HENCE THE CSV FILE IS EMPTY!!!!

def df_to_csv(data):
  final_data = []
  try:
      for i in range(len(data)):
          voucher = data[i]['VOUCHER']

          #if there is only one stock item in voucher, we'll get dict intead of list in output from tally
          #So we are checking is it's dict, we convert into list
          if voucher['ALLINVENTORYENTRIES.LIST']:
              if not isinstance(voucher['ALLINVENTORYENTRIES.LIST'], list):
                  voucher['ALLINVENTORYENTRIES.LIST'] = [voucher['ALLINVENTORYENTRIES.LIST']]

              # print(voucher['ALLINVENTORYENTRIES.LIST'])

              for j in range(len(voucher['ALLINVENTORYENTRIES.LIST'])):
                  final_data.append(
                      {
                      "date": voucher['DATE'],
                      "voucher_type": voucher['VOUCHERTYPENAME'],
                      "party_ledger": voucher['PARTYLEDGERNAME'],
                      # "reference_number": voucher['REFERENCE'],
                      "voucher_number": voucher['VOUCHERNUMBER'],
                      "item_name": voucher['ALLINVENTORYENTRIES.LIST'][j]['STOCKITEMNAME'],
                      "rate": voucher['ALLINVENTORYENTRIES.LIST'][j]['RATE'],
                      "amount": voucher['ALLINVENTORYENTRIES.LIST'][j]['AMOUNT'],
                      "actual_quantity": voucher['ALLINVENTORYENTRIES.LIST'][j]['ACTUALQTY'],
                      "billed_quantity": voucher['ALLINVENTORYENTRIES.LIST'][j]['BILLEDQTY']
                      }
                  )
  except Exception as e:
      print("pass:", e)

  try:
      #convert dictionary to csv file
      csv_file = "first_draft.csv"
      csv_columns = ['date',
                      'voucher_type',
                      'party_ledger',
                  #   'reference_number',
                      'voucher_number',
                      'item_name',
                      'rate',
                      'amount',
                      'actual_quantity',
                      'billed_quantity'
                      ]

      csv_file = 'second_draft.csv'

      #check if csv file is exist or not, if not create and add headers
      if not os.path.isfile(csv_file):
          with open(csv_file, 'w', newline='') as output_file:
              dict_writer = csv.DictWriter(output_file, csv_columns)
              dict_writer.writeheader()
              dict_writer.writerows(final_data)
          
      else:
          with open(csv_file, 'a', newline='') as output_file:
              dict_writer = csv.DictWriter(output_file, csv_columns)
              dict_writer.writerows(final_data)

  except Exception as e:
      print(e)

  return final_data

try:
  combined = dict()
  for voucher_type in ['Purchase Vouchers', 'Sales Vouchers']:
    #open xml file which you get as output from tally
    with open(f'output_files/{voucher_type}.xml', 'r') as f:
      # data = xmltodict.parse(f.read())['ENVELOPE']['BODY']['IMPORTDATA']['REQUESTDATA']['TALLYMESSAGE']
      tree = ET.parse('output_files\Sales Vouchers.xml')
      xml_data = tree.getroot()

      #here you can change the encoding type to be able to set it to the one you need
      xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

      data_dict = dict(xmltodict.parse(xmlstr))
      data = data_dict['ENVELOPE']['BODY']['IMPORTDATA']['REQUESTDATA']['TALLYMESSAGE']

      combined[voucher_type] = df_to_csv(data)

except Exception as e:
  print(e)


sales_dff = []
purchase_dff = []

for k, v in combined.items():
   for i in v:
      if i['voucher_type'] == 'Sales':
         sales_dff.append(i)

      elif i['voucher_type'] == 'Purchase':
         purchase_dff.append(i)

      else:
         pass

sales_df = pd.DataFrame.from_dict(sales_dff)
purchase_df = pd.DataFrame.from_dict(purchase_dff)

convert_dict = {"voucher_number" : int, "voucher_type" : str, "party_ledger" : str, "item_name" : str, "amount" : float, "actual_quantity" : int}#, "rate" : float

purchase_df.drop(['rate', 'billed_quantity'], inplace = True, axis = 1)
purchase_df.drop_duplicates(keep = 'first', inplace = True)

purchase_df['amount'] = purchase_df['amount'].str.replace('-', '')
purchase_df['actual_quantity'] = purchase_df['actual_quantity'].str.replace(' QTY', '')
# purchase_df['rate'] = purchase_df['rate'].str.replace('/QTY', '')

purchase_df = purchase_df.astype(convert_dict)

purchase_df1 = purchase_df.groupby(['party_ledger', 'item_name']).agg({
                                          'date' : 'first', 'voucher_type' : 'first', 'party_ledger' : 'first', 'item_name' : 'first',
                                          'amount' : 'sum', 'actual_quantity' : 'sum'})



sales_df.drop(['rate', 'billed_quantity'], inplace = True, axis = 1)
sales_df.drop_duplicates(keep = 'first', inplace = True)

sales_df['amount'] = sales_df['amount'].str.replace('-', '')
sales_df['actual_quantity'] = sales_df['actual_quantity'].str.replace(' QTY', '')
# sales_df['rate'] = sales_df['rate'].str.replace('/unit', '')

sales_df = sales_df.astype(convert_dict)

sales_df1 = sales_df.groupby(['party_ledger', 'item_name']).agg({
                                          'date' : 'first', 'voucher_type' : 'first', 'party_ledger' : 'first', 'item_name' : 'first',
                                          'amount' : 'sum', 'actual_quantity' : 'sum'})


purchase_df1.reset_index(drop = True, inplace = True)
sales_df1.reset_index(drop = True, inplace = True)

try:
  tmp = purchase_df1.set_index(['party_ledger', 'item_name'])
  out = (tmp
        .sub(sales_df1.set_index(['party_ledger', 'item_name'])[['amount', 'actual_quantity']])
        .combine_first(tmp).assign(voucher_type='Remaining')
        .reset_index()[purchase_df1.columns]
        )
  
except Exception as e:
  print(e)

out['Quantity'] = abs(out['actual_quantity'])
out['Party_Name'] = out['party_ledger']
out['Script_Name'] = out['item_name']
out.drop(['actual_quantity', 'party_ledger', 'item_name'], inplace = True, axis = 1)

purchase_df1.to_csv('purchse_final.csv', index = False)
sales_df1.to_csv('sales_final.csv', index = False)
out.to_csv('op.csv', index = False)


# s = pd.read_csv('sales_final.csv')
# p = pd.read_csv('purchse_final.csv')

# def df_to_csv(data, voucher_type):
#   #convert xml to dictionary
#   final_data = []

#   for i in range(len(data)):
#     try:
#       voucher = data[i]['VOUCHER']

#       #if there is only one stock item in voucher, we'll get dict intead of list in output from tally
#       #So we are checking is it's dict, we convert into list
#       if not isinstance(voucher['ALLINVENTORYENTRIES.LIST'], list):
#         voucher['ALLINVENTORYENTRIES.LIST'] = [voucher['ALLINVENTORYENTRIES.LIST']]

#       for j in range(len(voucher['ALLINVENTORYENTRIES.LIST'])):
#           final_data.append(
#               {
#                 "date": voucher['DATE'],
#                 "voucher_type": voucher['VOUCHERTYPENAME'],
#                 "party_ledger": voucher['PARTYLEDGERNAME'],
#                 "reference_number": voucher['REFERENCE'],
#                 "voucher_number": voucher['VOUCHERNUMBER'],
#                 "item_name": voucher['ALLINVENTORYENTRIES.LIST'][j]['STOCKITEMNAME'],
#                 "rate": voucher['ALLINVENTORYENTRIES.LIST'][j]['RATE'],
#                 "amount": voucher['ALLINVENTORYENTRIES.LIST'][j]['AMOUNT'],
#                 "actual_quantity": voucher['ALLINVENTORYENTRIES.LIST'][j]['ACTUALQTY'],
#                 "billed_quantity": voucher['ALLINVENTORYENTRIES.LIST'][j]['BILLEDQTY']
#               }
#           )
    
#     except Exception as e:
#       print("pass:", e)

#   try:
#     #convert dictionary to csv file
#     csv_file = "first_draft.csv"
#     csv_columns = ['date',
#                   'voucher_type',
#                   'party_ledger',
#                   'reference_number',
#                   'voucher_number',
#                   'item_name',
#                   'rate',
#                   'amount',
#                   'actual_quantity',
#                   'billed_quantity'
#                   ]

#     csv_file = 'first_draft.csv'

#     #check if csv file is exist or not, if not create and add headers
#     if not os.path.isfile(csv_file):
#       with open(csv_file, 'w', newline='') as output_file:
#         dict_writer = csv.DictWriter(output_file, csv_columns)
#         dict_writer.writeheader()
#         dict_writer.writerows(final_data)
      
#     else:
#       with open(csv_file, 'a', newline='') as output_file:
#           dict_writer = csv.DictWriter(output_file, csv_columns)
#           dict_writer.writerows(final_data)

#   except Exception as e:
#     print(e)

#   try:
#     csv_file = voucher_type + '.csv'
#     #For Purchase check if csv file is exist or not, if not create and add headers
#     if not os.path.isfile(csv_file):
#       with open(csv_file, 'w', newline='') as output_file:
#         dict_writer = csv.DictWriter(output_file, csv_columns)
#         dict_writer.writeheader()
#         dict_writer.writerows(final_data)
      
#     else:
#       with open(csv_file, 'a', newline='') as output_file:
#           dict_writer = csv.DictWriter(output_file, csv_columns)
#           dict_writer.writerows(final_data)
#   except Exception as e:
#     print(e)

#   return final_data



# try:
#   combined = dict()
#   for voucher_type in ['Sales Vouchers']:
#     #open xml file which you get as output from tally
#     with open(f'output_files/{voucher_type}.xml', 'r') as f:
#       data = xmltodict.parse(f.read())['ENVELOPE']['BODY']['IMPORTDATA']['REQUESTDATA']['TALLYMESSAGE']
#       combined[voucher_type] = df_to_csv(data, voucher_type)

# except Exception as e:
#   print(e)


