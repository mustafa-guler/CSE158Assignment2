import gzip
import pickle
import json
import datetime
from bs4 import BeautifulSoup

def clean_data(q):
    date_keys = ['ClosedDate', 'CreationDate', 'LastActivityDate', 'LastEditDate']
    for key in q:
        if key in date_keys:
            curr_date, curr_time = q[key].split('T')
            curr_date = list(map(int, curr_date.split('-')))
            curr_time = curr_time.split(":")
            curr_time[-1] = curr_time[-1].split(".")[0]
            curr_time = list(map(int, curr_time))
            q[key] = datetime.datetime(*(curr_date + curr_time))
        elif key == 'Tags':
            q[key] = q[key][1:-1].split("><")
        elif key == 'Body':
            soup = BeautifulSoup(q[key], 'html.parser')
            q[key] = {'code': list(map(lambda x: x.text, soup.find_all('code'))),
                    'links': list(map(lambda x:x.get('href'), soup.find_all('a'))),
                    'text': soup.get_text()}
        else:
            try:
                q[key] = int(q[key])
            except ValueError:
                continue
    return q

with gzip.open("PythonStackOverflow.json.gz", "rb") as f:
    dataset = [json.loads(line) for line in f]
print("read dataset")

questions = [clean_data(d) for d in dataset if d['PostTypeId'] == "1"]
print("read questions")
answers = [clean_data(d) for d in dataset if d['PostTypeId'] == "2"]
print("read answers")

with open("questions.pk1", "wb") as f:
    pickle.dump(questions, f)
print("pickled questions")

with open("answers.pk1", "wb") as f:
    pickle.dump(answers, f)
print("pickled answers")
