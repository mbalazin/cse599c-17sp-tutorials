CREATE SCHEMA lobsters;

CREATE TABLE lobsters.tags ( id integer NOT NULL, tag varchar(64));

CREATE TABLE lobsters.taggings (id integer NOT NULL, story_id integer NOT NULL, tag_id integer NOT NULL);

CREATE TABLE lobsters.hiddens (id integer NOT NULL, user_id integer NOT NULL, story_id integer NOT NULL);

CREATE TABLE lobsters.stories (id integer NOT NULL, created_at TIMESTAMP, description varchar(4095), hotness float, markeddown_description varchar(4095), short_id varchar(255), title varchar(1023), upvotes integer, downvotes integer, url varchar(255), user_id integer);


