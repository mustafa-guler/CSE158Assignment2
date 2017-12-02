import re
import xml.etree.ElementTree as ET
import json
from os.path import splitext

def get_ids(xml_file):
    result = set()
    with open(xml_file) as f:
        f.readline() #read the xml doc info
        f.readline() #read opening <post>

        for line in f:
            if "&lt;python&gt;" in line:
                matches = re.match("<row Id=\"(\d+)", line.strip())
                if matches:
                    result.add(matches.group(1))
    return result

def write_python_entries(xml_file, out_file, ids):
    out = open(out_file, "w+")
    with open(xml_file) as f:
        out.write(f.readline()) #xml doc info
        out.write(f.readline()) #opening <post>

        for line in f:
            rowID = re.search("<row Id=\"(\d+)", line)
            if rowID:
                rowID = rowID.group(1)
            parentID = re.search("ParentId=\"(\d+)", line)
            if parentID:
                parentID = parentID.group(1)

            if rowID in ids or parentID in ids:
                out.write(line)
    out.write("</posts>\n")
    out.close()

def to_json(xml_file):
    root = ET.parse(xml_file).getroot()
    json_file = splitext(xml_file)[0] + ".json"
    json_fh = open(json_file, "w+")

    for child in root:
        json_fh.write(json.dumps(child.attrib) + "\n")
    json_fh.close()


#if __name__ == "__main__":
#    import sys
#    in_file, out_file = sys.argv[1:3]
#    ids = get_ids(in_file)
#    write_python_entries(in_file, out_file, ids)
