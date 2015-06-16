import email
import os
import os.path
import sys
import numpy
import re
from collections import Counter
import pandas
from pandasql import *

person = 'taylor-m'
directory = "/home/mallend1/Downloads/enron_mail/maildir/"+ person
regex = re.compile(r'[ \n\r\t\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]')
regex_1 = re.compile(r'[\n\r\t\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]')
class Email(object):
    def __init__(self,_from, to_list, _subject, _body, date):
        self._from = _from
        self.to_list = to_list
        self._subject = _subject
        self._body = _body
        self.date = date

		
emails = []
text = []
for root, dirs, file_names in os.walk(directory):
	for file_name in file_names:
		file_path = os.path.join(root, file_name)
		message_file = file(file_path, "r")
		message_text = message_file.read()
		message_file.close()
		msg = email.message_from_string(message_text)
		#writeToFile(outfile, str(msg['From']), str(msg['To']),str(msg['Subject']), msg.get_payload())
		_to = str(msg['To'])
		to_list = _to.split(',')
		te = msg.get_payload()
		text.append(regex_1.sub('',te))
		emails.append(Email(str(msg['From']), to_list,str(msg['Subject']),regex_1.sub(' ',te),str(msg['Date'])))
print len(emails)
emails_list = []
i=0
people = []
for email in emails:
	for _to in email.to_list:
		e = []
		e.append(i)
		f= regex.sub('',email._from)
		e.append(f)
		t = regex.sub('',_to)
		people.append(t)
		e.append(t)
		e.append(email._subject)
		e.append(email._body)
		e.append(email.date)
		emails_list.append(e)
	i=i+1
em = Counter(people).most_common(1)[0][0]
unique_peeps = OrderedDict.fromkeys(people).keys()
unique_peeps.remove(em)
df = pandas.DataFrame(emails_list, columns=['idd','_From', '_To', 'Subject', 'Body','Date'])		
person = 'mark.elliott@enron.com'
#q = "SELECT idd,_From,_To,Subject FROM df where (_From='%s' OR _TO = '%s') AND (_From='%s' OR _TO = '%s');"%(person,person,em,em)
q = "SELECT Distinct Subject FROM df where (_From='%s' OR _TO = '%s') AND (_From='%s' OR _TO = '%s');"%(person,person,em,em)
#q = "SELECT idd,_From,_To,Subject FROM df where _From='%s' OR _TO = '%s';"%(person,person)
p = sqldf(q, globals())
print sqldf(q, globals())
sub = p.ix[1].Subject
q_1  = "SELECT idd FROM df where (_From='%s' OR _TO = '%s') AND (_From='%s' OR _TO = '%s') AND Subject = '%s';"%(person,person,em,em,sub)
print sqldf(q_1, globals())
