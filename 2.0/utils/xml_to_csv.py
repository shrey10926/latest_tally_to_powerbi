'''
from xml files of purchase and sales vouchers,
scrap all vouchers data and put in excel/csv files
'''

from os.path import join as join_path
from os.path import isfile
from xml.etree import ElementTree as et
import xmltodict
import csv

class ToCSV():
    def __init__():
        pass


    def all_data_xml_to_df():
        '''
        extract all data from xml files to dictionary
        '''
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
        '''
        return only required data as final_data
        '''
        final_data = dict()

        for data_type in ('Sales Vouchers', 'Purchase Vouchers'):
            temp_data = []
            all_data = data[data_type]

            for i in all_data:
                if 'VOUCHER' in i.keys():

                    if isinstance(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'], list):
                        for j in range(len(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'])):
                            temp = dict()
                            temp['V_TYPE'] = data_type.split(' ')[0]
                            temp['V_No'] = i['VOUCHER']['VOUCHERNUMBER']
                            temp['DATE'] = i['VOUCHER']['DATE']
                            temp['STATE'] = i['VOUCHER']['STATENAME']
                            temp['PLACEOFSUPPLY'] = i['VOUCHER']['PLACEOFSUPPLY']
                            temp['PARTYLEDGERNAME'] = i['VOUCHER']['PARTYLEDGERNAME']
                            temp['TOTAL_BILLED_AMOUNT'] = i['VOUCHER']['LEDGERENTRIES.LIST']['AMOUNT']
                            temp['NARRATION'] = i['VOUCHER']['NARRATION']
                            temp['ITEM_NAME'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['STOCKITEMNAME']
                            temp['ITEM_AMOUNT'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['AMOUNT']

                            temp_data.append(temp)

                    elif isinstance(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'], dict):
                        temp = dict()
                        temp['V_TYPE'] = data_type.split(' ')[0]
                        temp['V_No'] = i['VOUCHER']['VOUCHERNUMBER']
                        temp['DATE'] = i['VOUCHER']['DATE']
                        temp['STATE'] = i['VOUCHER']['STATENAME']
                        temp['PLACEOFSUPPLY'] = i['VOUCHER']['PLACEOFSUPPLY']
                        temp['PARTYLEDGERNAME'] = i['VOUCHER']['PARTYLEDGERNAME']
                        temp['TOTAL_BILLED_AMOUNT'] = i['VOUCHER']['LEDGERENTRIES.LIST']['AMOUNT']
                        temp['NARRATION'] = i['VOUCHER']['NARRATION']
                        temp['ITEM_NAME'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['STOCKITEMNAME']
                        temp['ITEM_AMOUNT'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['AMOUNT']

                        temp_data.append(temp)

            final_data[data_type] = temp_data

            print('\n' + '-'*50)
            print(data_type)
            print('-'*50)

            for i in final_data[data_type]:
                for k, v in i.items():
                    print(f"{k} --> {v}")
                print()

        return final_data


    def data_to_csv(final_data):
        '''
        save purchase and sales vouchers data into two saperate csv files
        '''
        for data_type in ('Sales Vouchers', 'Purchase Vouchers'):
            try:
                csv_file = f"{data_type}.csv"
                csv_columns = ['V_TYPE',
                                'V_No',
                                'DATE',
                                'STATE',
                                'PLACEOFSUPPLY',
                                'PARTYLEDGERNAME',
                                'TOTAL_BILLED_AMOUNT',
                                'NARRATION',
                                'ITEM_NAME',
                                'ITEM_AMOUNT'
                                ]

                #check if csv file is exist or not, if not create and add headers
                if not isfile(csv_file):
                    with open(csv_file, 'w', newline='') as output_file:
                        dict_writer = csv.DictWriter(output_file, csv_columns)
                        dict_writer.writeheader()
                        dict_writer.writerows(final_data[data_type])
                    
                else:
                    with open(csv_file, 'a', newline='') as output_file:
                        dict_writer = csv.DictWriter(output_file, csv_columns)
                        dict_writer.writerows(final_data[data_type])

            except Exception as e:
                print("ERROR -->", e)