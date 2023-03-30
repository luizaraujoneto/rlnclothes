-- Database: rlnclothesdb_hmg

DROP DATABASE IF EXISTS rlnclothesdb_hmg;

CREATE DATABASE rlnclothesdb_hmg
    WITH
    OWNER = rlnclothesuser
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT TEMPORARY, CONNECT ON DATABASE rlnclothesdb_hmg TO PUBLIC;

GRANT ALL ON DATABASE rlnclothesdb_hmg TO rlnclothesuser;