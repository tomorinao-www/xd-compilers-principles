CREATE DATABASE db1;
USE db1;

CREATE TABLE users (
    id INT,
    name CHAR(50)
);
INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');
INSERT INTO users VALUES (3, 'Peter');
INSERT INTO users VALUES (4, 'Eve');

SELECT * FROM users;
SELECT name FROM users WHERE name = 'Alice';
SELECT id, name FROM users WHERE id <= 2 OR name = 'Eve';

UPDATE users SET name = 'Charlie' WHERE id = 1;

DELETE FROM users WHERE id = 4;
SELECT * FROM users;

DROP TABLE users;
DROP DATABASE db1;
