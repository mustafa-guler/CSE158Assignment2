from ExtractData import *
import sys

xml_file = sys.argv[1]
out_file = sys.argv[2]

ids = get_ids(xml_file)
write_python_entries(xml_file, out_file, ids)
to_json(out_file)
