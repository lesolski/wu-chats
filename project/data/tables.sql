CREATE TABLE IF NOT EXISTS group_fav (
				id int primary key,
				user_id int,
				group_id int,
				foreign key(user_id) references users(id),
				foreign key(group_id) references groups(id)
				);

CREATE TABLE IF NOT EXISTS users (
				id integer primary key,
				username varchar(50),
				password varchar(60),
				confirmed integer,
				confirmed_on datetime
				);

CREATE TABLE IF NOT EXISTS groups(
				id integer primary key,
				semester varchar(4),
				group_name text,
				course_id text,
				professors text,
				platform text,
				group_link text,
				show_admin int,
				author text,
				qr_code text,
				foreign key(author) references users(username)
				);

CREATE TABLE IF NOT EXISTS news(
			id integer primary key,
			title varchar(200),
			descr text,
			link text,
			date(published_at) datetime);


CREATE TABLE IF NOT EXISTS  faqs(
			id integer primary key,
			question text,
			answer text);