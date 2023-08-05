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

        for voucher_type in ['Sales Vouchers', 'Purchase Vouchers']:
            f = join_path('output_files', str(voucher_type)+'.xml')
            with open(f, 'r'):
                tree = et.parse(f)
                xml_data = tree.getroot()

                #here you can change the encoding type to be able to set it to the one you need
                xmlstr = et.tostring(xml_data, encoding='utf-8', method='xml')

                data_dict = dict(xmltodict.parse(xmlstr))
                data = data_dict['ENVELOPE']['BODY']['DATA']['TALLYMESSAGE']

                print(data)