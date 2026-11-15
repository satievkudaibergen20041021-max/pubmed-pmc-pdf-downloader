import xml.etree.ElementTree as ET


with open('xml_ids/exeption.txt13751970', 'r', encoding='utf-8') as f:
    xml_data = f.read()
    
root = ET.fromstring(xml_data)
namespace = root.tag.split('}')[0].strip('{')
ns = {'s3': namespace}
variable = root.find('.//s3:CommonPrefixes/s3:Prefix', ns).text
if variable is not None:
    pass