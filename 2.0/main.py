from utils.get_xml_from_tally import GetXML
from utils.xml_to_csv import ToCSV
import pandas as pd
# GetXML()

data = ToCSV.all_data_xml_to_df()

sales_data = data['Sales Vouchers']
purchase_data = data['Purchase Vouchers']

final_sales_data = []
for i in sales_data:
    temp = dict()
    if 'VOUCHER' in i.keys():
        temp['V_TYPE'] = "Sales"
        temp['V_No'] = i['VOUCHER']['VOUCHERNUMBER']
        temp['DATE'] = i['VOUCHER']['DATE']
        temp['STATE'] = i['VOUCHER']['STATENAME']
        temp['PLACEOFSUPPLY'] = i['VOUCHER']['PLACEOFSUPPLY']
        temp['PARTYLEDGERNAME'] = i['VOUCHER']['PARTYLEDGERNAME']
        temp['NARRATION'] = i['VOUCHER']['NARRATION']
        temp['ITEMS'] = []

        print(type(i['VOUCHER']['ALLINVENTORYENTRIES.LIST']))

        if isinstance(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'], list):
            for j in range(len(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'])):
                temp2 = dict()
                temp2['NAME'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['STOCKITEMNAME']
                temp2['AMOUNT'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['AMOUNT']

                temp['ITEMS'].append(temp2)

        elif isinstance(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'], dict):
            temp2 = dict()
            temp2['NAME'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['STOCKITEMNAME']
            temp2['AMOUNT'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['AMOUNT']

            temp['ITEMS'].append(temp2)

        final_sales_data.append(temp)

print(final_sales_data)
print()

for i in final_sales_data:
    for k, v in i.items():
        print(f"{k} --> {v}")
    print()


final_purchase_data = []
for i in purchase_data:
    temp = dict()
    if 'VOUCHER' in i.keys():
        temp['V_TYPE'] = "Purchase"
        temp['V_No'] = i['VOUCHER']['VOUCHERNUMBER']
        temp['DATE'] = i['VOUCHER']['DATE']
        temp['STATE'] = i['VOUCHER']['STATENAME']
        temp['PLACEOFSUPPLY'] = i['VOUCHER']['PLACEOFSUPPLY']
        temp['PARTYLEDGERNAME'] = i['VOUCHER']['PARTYLEDGERNAME']
        temp['NARRATION'] = i['VOUCHER']['NARRATION']
        temp['ITEMS'] = []

        print(type(i['VOUCHER']['ALLINVENTORYENTRIES.LIST']))

        if isinstance(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'], list):
            for j in range(len(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'])):
                temp2 = dict()
                temp2['NAME'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['STOCKITEMNAME']
                temp2['AMOUNT'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['AMOUNT']

                temp['ITEMS'].append(temp2)

        elif isinstance(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'], dict):
            temp2 = dict()
            temp2['NAME'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['STOCKITEMNAME']
            temp2['AMOUNT'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['AMOUNT']

            temp['ITEMS'].append(temp2)

        final_purchase_data.append(temp)

print(final_purchase_data)
print()

for i in final_purchase_data:
    for k, v in i.items():
        print(f"{k} --> {v}")
    print()


purchase_df = []
for entry in final_purchase_data:
    v_type = entry['V_TYPE']
    v_no = entry['V_No']
    date = entry['DATE']
    state = entry['STATE']
    place_of_supply = entry['PLACEOFSUPPLY']
    part_ledger_name = entry['PARTYLEDGERNAME']
    narration = entry['NARRATION']
    for item in entry['ITEMS']:
        item_name = item['NAME']
        amount = item['AMOUNT']
        purchase_df.append([v_type, v_no, date, state, place_of_supply, part_ledger_name, narration, item_name, amount])

p_df = pd.DataFrame(purchase_df, columns=['V_TYPE', 'V_NO', 'DATE', 'STATE', 'PLACE_OF_SUPPLY', 'PARTY_LEDGER_NAME', 'NARRATION', 'ITEMS', 'AMOUNT'])



sales_df = []
for entry in final_sales_data:
    v_type = entry['V_TYPE']
    v_no = entry['V_No']
    date = entry['DATE']
    state = entry['STATE']
    place_of_supply = entry['PLACEOFSUPPLY']
    part_ledger_name = entry['PARTYLEDGERNAME']
    narration = entry['NARRATION']
    for item in entry['ITEMS']:
        item_name = item['NAME']
        amount = item['AMOUNT']
        sales_df.append([v_type, v_no, date, state, place_of_supply, part_ledger_name, narration, item_name, amount])

s_df = pd.DataFrame(sales_df, columns=['V_TYPE', 'V_NO', 'DATE', 'STATE', 'PLACE_OF_SUPPLY', 'PARTY_LEDGER_NAME', 'NARRATION', 'ITEMS', 'AMOUNT'])
