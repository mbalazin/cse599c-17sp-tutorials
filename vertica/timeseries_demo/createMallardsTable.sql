create table if not exists mallards (
	eventId varchar(20) PRIMARY KEY,
	ts timestamp,
	locationLong float,
	locationLat float);

