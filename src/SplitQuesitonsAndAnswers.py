import gzip
import json

qs = open("questions.json", "w+")
ans = open("answers.json", "w+")

with gzip.open("PythonStackOverflow.json.gz") as f:
    for line in f:
        line = json.loads(line)
        if line["PostTypeId"] == 1:
            qs.write(json.dumps(line) + "\n")
        else:
            ans.write(json.dumps(line) + "\n")

qs.close()
ans.close()
