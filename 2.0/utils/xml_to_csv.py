'''
from xml files of purchase and sales vouchers,
scrap all vouchers data and put in excel/csv files
'''

from os.path import join as join_path
from xml.etree import ElementTree as et
import xmltodict

class ToCSV():
    def __init__():
        final_data = []


    def all_data_xml_to_df():
        data = dict()

        for voucher_type in ['Sales Vouchers', 'Purchase Vouchers']:
            f = join_path('output_files', str(voucher_type)+'.xml')
            with open(f, 'r'):
                tree = et.parse(f)
                xml_data = tree.getroot()

                #here you can change the encoding type to be able to set it to the one you need
                xmlstr = et.tostring(xml_data, encoding='utf-8', method='xml')

                data_dict = dict(xmltodict.parse(xmlstr))
                data[voucher_type] = data_dict['ENVELOPE']['BODY']['DATA']['TALLYMESSAGE']
        
        print("Got all data from xml to dictionary")
        return data
    
    def filter_data(data):
        final_data = dict()

        for data_type in ('Sales Vouchers', 'Purchase Vouchers'):
            temp_data = []
            all_data = data[data_type]

            for i in all_data:
                temp = dict()
                if 'VOUCHER' in i.keys():
                    temp['V_TYPE'] = data_type.split(' ')[0]
                    temp['V_No'] = i['VOUCHER']['VOUCHERNUMBER']
                    temp['DATE'] = i['VOUCHER']['DATE']
                    temp['STATE'] = i['VOUCHER']['STATENAME']
                    temp['PLACEOFSUPPLY'] = i['VOUCHER']['PLACEOFSUPPLY']
                    temp['PARTYLEDGERNAME'] = i['VOUCHER']['PARTYLEDGERNAME']
                    temp['NARRATION'] = i['VOUCHER']['NARRATION']
                    temp['ITEMS'] = []

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

                    temp_data.append(temp)

            final_data[data_type] = temp_data

            # print(final_data)

            print('\n' + '-'*50)
            print(data_type)
            print('-'*50)

            for i in final_data[data_type]:
                for k, v in i.items():
                    print(f"{k} --> {v}")
                print()