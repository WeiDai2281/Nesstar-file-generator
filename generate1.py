import xml.etree.ElementTree as ET
import copy
import pandas as pd
import numpy as np

# configure the input format:
excel_file_name = "Example data.csv"
template_file_name = "template.xml"
output_name = "result_1.xml"

# parse the xml
ET.register_namespace('', "http://www.icpsr.umich.edu/DDI")
xmlfile = ET.parse(template_file_name)
root = xmlfile.getroot()

# create the template element for section and variable
fileDscr_template = root.find("{http://www.icpsr.umich.edu/DDI}fileDscr")
root.remove(fileDscr_template)
var_template = root[2][0]
root[2].remove(var_template)


test = pd.read_csv(excel_file_name, encoding="utf-8")
data = np.array(test)

# define the function to create section


def create_section(section_name, count):
    print "Creating one section..."
    stringa = "Example_for_script.Nesstar?Index=" + str(count)
    stringb = "&amp;Name=" + section_name
    section = copy.deepcopy(fileDscr_template)
    id = "F" + str(count + 1)
    section.set("ID", id)
    section.set("URI", stringa + stringb)
    text = section_name + " name.NSDstat"
    section[0][0].text = text
    return section


# define the function to create the variable


def create_variable(name, text, section, count):
    print "Creating one variable"
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
    section_dic = {}
    section_set = set(data[:, 2])
    count = -1
    var_count = 0
    for i in section_set:
        count += 1
        section_dic[i] = "F" + str(count + 1)
        section = create_section(i, count)
        root.insert(2, section)
    print len(section_set), "section have been created in total"
    for i in range(data.shape[0]):
        var_count += 1
        newvar = create_variable(data[i][1], data[i][0], section_dic[data[i][2]], var_count)
        root[-1].append(copy.deepcopy(newvar))
    print data.shape[0], "variables have been created in total"
    xmlfile.write(output_name)




