import datetime, random
import string
import sys
import helper

def get_random_string(length):
	chars = "".join( [random.choice(string.letters) for i in xrange(length)] )
	return chars

def get_random_url():
	return "http://www." + get_random_string(6) + ".com"


num_users = int(sys.argv[1])
num_stories = int(sys.argv[2])
num_comments = int(sys.argv[3])
thread_cnt = 0

comment_thread_hash = {}
short_ids = []
comment_id = 0
comment_id_start = 1

for i in range(0, num_comments):
	created_at = str(helper.get_time(num_comments-i))[0:-7]
	updated_at = created_at 

	short_id = get_random_string(6)
	while short_id in short_ids:
		short_id = get_random_string(6)
	short_ids.append(short_id)
	story_id = str(random.randint(1, num_stories))
	user_id = str(random.randint(1, num_users))
	comment_id += 1
	
	parent_comment_id = ""
	thread_id = thread_cnt
	if i > 10 and random.randint(1, 10) < 8 and comment_id > comment_id_start + 10:
		parent_comment_id = random.randint(comment_id_start+1, comment_id-1)
		thread_id = comment_thread_hash[parent_comment_id] 
	else:
		thread_cnt += 1
		thread_id = thread_cnt
	comment_thread_hash[comment_id] = thread_id
	comment_length = random.randint(16, 128)
	comment = get_random_string(comment_length)
	
	upvotes = "0"
	downvotes = "0"
	confidence = str(random.uniform(-100, 100))
	m_comment_length = random.randint(16, 1024)
	markeddown_comment = "<p>%s</p>"%get_random_string(m_comment_length)
	
	is_deleted = "0"
	is_moderated = "0"
	is_from_email = "0"
	hat_id = ""
	vote = "1"	
	
	print ",".join([str(i+1), comment, confidence, created_at, markeddown_comment, short_id, story_id, str(thread_id), str(parent_comment_id), updated_at, upvotes, user_id])


