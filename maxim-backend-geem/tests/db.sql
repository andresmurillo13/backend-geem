\set db_name `echo "$DB_NAME_POSTGRES"`
\set db_user `echo $DB_USER_POSTGRES`
DROP DATABASE IF EXISTS :db_name;
CREATE DATABASE :db_name WITH OWNER :db_user;
\connect :db_name :db_user;
