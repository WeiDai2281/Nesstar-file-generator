import xml.etree.ElementTree as ET
import copy
import pandas as pd
import json, ast

# configure the input format:
excel_file_name = "Example data.xls"
template_file_name = "template.xml"
output_name = "result.xml"

# parse the xml
ET.register_namespace('', "http://www.icpsr.umich.edu/DDI")
xmlfile = ET.parse(template_file_name)
root = xmlfile.getroot()

# create the template element for section and variable
fileDscr_template = root.find("{http://www.icpsr.umich.edu/DDI}fileDscr")
root.remove(fileDscr_template)
var_template = root[2][0]
root[2].remove(var_template)

# open the excel file
sheet_names = pd.ExcelFile(excel_file_name).sheet_names

# define the function to transform one section data into dictionary


def parse_excel(sheet):
    data = pd.read_excel(excel_file_name, header=None, sheetname=sheet)
    data.columns = ["1", "2"]
    dic = data.set_index("1").to_dict()["2"]
    dictionary = ast.literal_eval(json.dumps(dic))

    return dictionary

# define the function to create section
def create_section(sheet, count):
    stringa = "Example_for_script.Nesstar?Index=" + str(count)
    stringb = "&amp;Name=" + sheet
    section = copy.deepcopy(fileDscr_template)
    id = "F" + str(count + 1)
    section.set("ID", id)
    section.set("URI", stringa + stringb)
    return section, id

# define the function to create the variable

def create_variable(name, text, section, count):
    var = copy.deepcopy(var_template)
    id = "V" + str(count)
    var.set("ID", id)
    var.set("files", section)
    var.set("name", name)
    var.text = text
    var[1].text = text
    var[3][0].text = text

    return var

if __name__ == "__main__":
    count = -1
    var_count = 0
    for sheet in sheet_names:
        count += 1
        dic = parse_excel(sheet)
        section, id = create_section(sheet, count)
        root.insert(2, section)
        for var_name in dic:
            var_count += 1
            newvar = create_variable(var_name, dic[var_name], id, var_count)
            root[-1].append(newvar)

    xmlfile.write(output_name)



#define the function to create the section
# def create_section(sec_name):
#     root


