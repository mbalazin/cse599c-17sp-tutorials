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
taggings_file = open("taggings.csv", "w")
hidden_file = open("hidden.csv", "w")
short_ids = []
story_id = 0
hidden_id = 0

for i in range(0, num_stories):
	created_at = str(helper.get_time(num_stories-i))
	user_id = str(random.randint(1, num_users))
	url = get_random_url()
	title = get_random_string(10)
	description_length = random.randint(16, 1024)
	description = get_random_string(description_length)
	short_id = get_random_string(6)
	while short_id in short_ids:
		short_id = get_random_string(6)
	short_ids.append(short_id)
	story_id += 1
	is_expired = "0"
	upvotes = str(random.randint(0, 10))
	downvotes = str(random.randint(0, 10))
	is_moderated = "0"
	hotness = str(random.uniform(-100, 100))
	markeddown_description = "<p>%s</p>"%get_random_string(description_length)
	story_cache = ""
	comments_count = "0"
	merged_story_id = ""
	unavailable_at = ""
	twitter_id = ""
	user_is_author = "0"
	tag_id = str(random.randint(1, 70))
	
	hidden = random.randint(0, 10)
	
	
	print ",".join( [str(i+1), created_at, description, hotness, markeddown_description, short_id, title, upvotes, downvotes, url, user_id])
	
	taggings_file.write("%s\n"%(",".join([str(i+1), str(story_id), tag_id])))
	if hidden < 3:
		hidden_file.write("%s\n"%(",".join([str(hidden_id+1), user_id, str(story_id)])))
		hidden_id += 1
	 
