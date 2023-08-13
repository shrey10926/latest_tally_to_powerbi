'''
from xml files of purchase and sales vouchers,
scrap all vouchers data and put in excel/csv files
'''

from os.path import join as join_path
from os.path import isfile
from xml.etree import ElementTree as et
import xmltodict
import csv
import os
import pandas as pd

class ToCSV():
    def __init__():
        pass

    def make_required_folders_files():
        folder_name = "output_files"

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print(f"The '{folder_name}' folder was created.")
        else:
            print(f"The '{folder_name}' folder already exists.")

        folder_name = "xml_files"
        file_name = "get_vouchers.xml"

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print(f"The '{folder_name}' folder was created.")
        else:
            print(f"The '{folder_name}' folder already exists.")

        file_path = os.path.join(folder_name, file_name)

        if not os.path.exists(file_path):
            xml_content = """<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>Export</TALLYREQUEST>
    <TYPE>Data</TYPE>
    <ID>Sales Vouchers</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVFROMDATE>20230401</SVFROMDATE>
        <SVTODATE>20230812</SVTODATE>
      </STATICVARIABLES>
    </DESC>
  </BODY>
</ENVELOPE>
"""

            root = et.fromstring(xml_content)
            tree = et.ElementTree(root)
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            print(f"The '{file_name}' file was created in the '{folder_name}' folder.")
        else:
            print(f"The '{file_name}' file already exists in the '{folder_name}' folder.")


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
                            temp['PARTYLEDGERNAME'] = i['VOUCHER']['PARTYLEDGERNAME']
                            temp['PLACEOFSUPPLY'] = i['VOUCHER']['PLACEOFSUPPLY']
                            temp['STATE'] = i['VOUCHER']['STATENAME']
                            temp['TOTAL_BILLED_AMOUNT'] = i['VOUCHER']['LEDGERENTRIES.LIST']['AMOUNT']
                            temp['ITEM_NAME'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['STOCKITEMNAME']
                            temp['QUANTITY'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['BILLEDQTY']
                            temp['RATE'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['RATE']
                            temp['ITEM_AMOUNT'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST'][j]['AMOUNT']
                            temp['NARRATION'] = i['VOUCHER']['NARRATION']
                            
                            temp_data.append(temp)

                    elif isinstance(i['VOUCHER']['ALLINVENTORYENTRIES.LIST'], dict):
                        temp = dict()
                        temp['V_TYPE'] = data_type.split(' ')[0]
                        temp['V_No'] = i['VOUCHER']['VOUCHERNUMBER']
                        temp['DATE'] = i['VOUCHER']['DATE']
                        temp['PARTYLEDGERNAME'] = i['VOUCHER']['PARTYLEDGERNAME']
                        temp['PLACEOFSUPPLY'] = i['VOUCHER']['PLACEOFSUPPLY']
                        temp['STATE'] = i['VOUCHER']['STATENAME']
                        temp['TOTAL_BILLED_AMOUNT'] = i['VOUCHER']['LEDGERENTRIES.LIST']['AMOUNT']
                        temp['ITEM_NAME'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['STOCKITEMNAME']
                        temp['QUANTITY'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['BILLEDQTY']
                        temp['RATE'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['RATE']
                        temp['ITEM_AMOUNT'] = i['VOUCHER']['ALLINVENTORYENTRIES.LIST']['AMOUNT']
                        temp['NARRATION'] = i['VOUCHER']['NARRATION']

                        temp_data.append(temp)

            final_data[data_type] = temp_data

            # print('\n' + '-'*50)
            # print(data_type)
            # print('-'*50)

            # for i in final_data[data_type]:
            #     for k, v in i.items():
            #         print(f"{k} --> {v}")
            #     print()

        print("filtered and saved required data from xml")

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
                                'PARTYLEDGERNAME',
                                'PLACEOFSUPPLY',
                                'STATE',
                                'TOTAL_BILLED_AMOUNT',
                                'ITEM_NAME',
                                'QUANTITY',
                                'RATE',
                                'ITEM_AMOUNT',
                                'NARRATION',
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

                        print(f'{data_type} saved in csv file')

            except Exception as e:
                print("ERROR -->", e)


    def combined_data_to_csv(final_data):
        '''
        save purchase and sales vouchers data into two saperate csv files
        '''
        csv_file = "combined.csv"
        # csv_columns = ['V_TYPE',
        #                 'V_No',
        #                 'DATE',
        #                 'PARTYLEDGERNAME',
        #                 'PLACEOFSUPPLY',
        #                 'STATE',
        #                 'TOTAL_BILLED_AMOUNT',
        #                 'ITEM_NAME',
        #                 'QUANTITY',
        #                 'RATE',
        #                 'ITEM_AMOUNT',
        #                 'NARRATION',
        #                 ]

        # #check if csv file is exist or not, if not create and add headers
        # if not isfile(csv_file):
        #     with open(csv_file, 'w', newline='') as output_file:
        #         dict_writer = csv.DictWriter(output_file, csv_columns)
        #         dict_writer.writeheader()

        for data_type in ('Sales Vouchers', 'Purchase Vouchers'):
            try:
                if os.path.exists(csv_file):
                    existing_data = pd.read_csv(csv_file)
                    new_data = pd.DataFrame(final_data[data_type])
                    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

                else:
                    combined_data = pd.DataFrame(final_data[data_type])
                
                convert_dict = {
                    'V_TYPE': str,
                    'V_No': int,
                    'DATE': str,
                    'PARTYLEDGERNAME': str,
                    'PLACEOFSUPPLY': str,
                    'STATE': str,
                    'TOTAL_BILLED_AMOUNT': float,
                    'ITEM_NAME': str,
                    'QUANTITY': str,
                    'RATE': str,
                    'ITEM_AMOUNT': float,
                    'NARRATION': str,
                }

                combined_data = combined_data.astype(convert_dict)
                combined_data.replace('nan', None, inplace=True)
                combined_data.replace('None', None, inplace=True)
                
                deduplicated_data = combined_data.drop_duplicates(keep='first')

                deduplicated_data.to_csv(csv_file, index=False)

                print(f'{data_type} saved in csv file')

            except Exception as e:
                print("ERROR -->", e)