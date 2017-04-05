import datetime, random
import string
import sys
import helper

def get_random_string(length):
	chars = "".join( [random.choice(string.letters) for i in xrange(length)] )
	return chars


num_messages = int(sys.argv[1])
num_users = int(sys.argv[2])
short_ids = []

for i in range(0, num_messages):
	#created_at = str(datetime.datetime.now())[0:-7]
	created_at = str(helper.get_time(num_messages-i))[0:-7]
	author_user_id = str(random.randint(1, num_users))
	recipient_user_id = str(random.randint(1, num_users))
	subject = get_random_string(10)
	body_length = random.randint(128, 1024)
	body = get_random_string(body_length)
	short_id = get_random_string(6)
	while short_id in short_ids:
		short_id = get_random_string(6)
	short_ids.append(short_id)
	
	print ",".join( [str(i+1), author_user_id, body, created_at, recipient_user_id, short_id, subject] )
