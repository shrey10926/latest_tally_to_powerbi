from utils.get_xml_from_tally import GetXML
from utils.xml_to_csv import ToCSV

ToCSV.make_required_folders_files()

GetXML()

data = ToCSV.all_data_xml_to_df()

final_data = ToCSV.filter_data(data)

# #for saving purchase and sales data into saperate csv files
# ToCSV.data_to_csv(final_data)

#for saving sames and purchase daata into one combined file
ToCSV.combined_data_to_csv(final_data)