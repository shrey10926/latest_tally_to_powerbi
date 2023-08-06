from utils.get_xml_from_tally import GetXML
from utils.xml_to_csv import ToCSV

GetXML()

data = ToCSV.all_data_xml_to_df()

final_data = ToCSV.filter_data(data)

ToCSV.data_to_csv(final_data)