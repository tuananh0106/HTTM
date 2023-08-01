CREATE TABLE user(
	id int8 NOT NULL AUTO_INCREMENT,
    username text(255),
    password text(255),
    email text(255),
    primary key(id)
);

CREATE TABLE label(
	id int8 NOT NULL AUTO_INCREMENT,
    name text(255),
     primary key(id)
);

CREATE TABLE label_of_user(
	id int8 NOT NULL AUTO_INCREMENT,
    user int8,
    label int8,
    PRIMARY KEY(id),
    FOREIGN KEY (user) REFERENCES user(id),
    FOREIGN KEY (label) REFERENCES label(id)
);

CREATE TABLE email(
	id int8 NOT NULL AUTO_INCREMENT,
    subject text(4294967295),
    context text(4294967295),
    sentTime text(255),
    sender text(255),
    receive int8,
    label int8,
    PRIMARY KEY(id),
    FOREIGN KEY (receive) REFERENCES user(id),
    FOREIGN KEY (label) REFERENCES label(id)
);

CREATE TABLE sample(
	id int8 NOT NULL AUTO_INCREMENT,
    context text(4294967295),
    label int8,
    is_trained int2,
    PRIMARY KEY(id),
    FOREIGN KEY (label) REFERENCES label(id)
);
    