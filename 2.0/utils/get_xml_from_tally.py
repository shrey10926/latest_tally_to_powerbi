'''
export sales and purchase vouchers as xml file and store in output_files folder

within for loop:
xml_files/get_vouchers.xml file will be edited for sales and purchase vouchers
also date can be modified in SVFROMDATE and SVTODATE
by default starting date: 1st April 2023
           end date: today's date
'''


import requests
from datetime import datetime
from xml.etree import ElementTree as et


class GetXML():
    def __init__(self):
        # tally ip and port
        url = "http://localhost:9000"

        print('2')
        for voucher_type in ['Purchase Vouchers', 'Sales Vouchers']:
            print('1')
            tree = et.parse('xml_files/get_vouchers.xml')
            root = tree.getroot()

            for elem in root.iter('ID'):
                elem.text = voucher_type

            for elem in root.iter('SVFROMDATE'):
                elem.text = '20230401'

            for elem in root.iter('SVTODATE'):
                elem.text = datetime.today().strftime('%Y%m%d')

            tree.write('xml_files/get_vouchers.xml')

            with open('xml_files/get_vouchers.xml', 'r') as f:
                sales_ledger_data = f.read()

            ledger_request = requests.post(url=url, data=sales_ledger_data)
            ledger_response = ledger_request.text.strip()

            xml_file = open(f"output_files/{voucher_type}.xml", "w", newline='')
            xml_file.write(ledger_response)

            print(f'{voucher_type} extracted in "output_files/{voucher_type}.xml"')