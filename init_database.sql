CREATE TABLE IF NOT EXISTS article (
	id serial not null primary key,
	title varchar not null,
	image_url varchar,
	published_date timestamptz not null,
	parsed_date timestamptz not null DEFAULT CURRENT_TIMESTAMP,
	unique (title, published_date)
);
