#!/bin/bash
num_users=474
num_messages=100
num_stories=200
num_comments=400

D="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "generating tags..."
python $D/gen_tags.py &> tags.csv

echo "generating stories..."
python $D/gen_stories.py $num_users $num_stories &> stories.csv

echo "generating comments..."
python $D/gen_comments.py $num_users $num_stories $num_comments &> comments.csv

echo "generating messages..."
python $D/gen_messages.py $num_messages $num_users &> messages.csv

