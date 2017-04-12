#!/bin/bash
num_users=474
num_messages=100
num_stories=4000
num_comments=400

echo "generating tags..."
python gen_tags.py &> tags.csv

echo "generating stories..."
python gen_stories.py $num_users $num_stories &> stories.csv

echo "generating comments..."
python gen_comments.py $num_users $num_stories $num_comments &> comments.csv

echo "generating messages..."
python gen_messages.py $num_messages $num_users &> messages.csv

