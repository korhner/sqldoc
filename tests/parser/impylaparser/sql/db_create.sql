CREATE DATABASE sql_doc_empty LOCATION '/tmp/sql_doc_empty';

CREATE DATABASE sql_doc_tables LOCATION '/tmp/sql_doc_tables';

CREATE TABLE sql_doc_tables.empty_not_partitioned_comments (
	id INTEGER COMMENT 'Id field.'
)
COMMENT 'A non partitioned table.'
STORED AS PARQUET;

CREATE TABLE sql_doc_tables.empty_not_partitioned_no_comments (
	id INTEGER
)
STORED AS PARQUET;

CREATE TABLE sql_doc_tables.empty_partitioned_comments (
	id INTEGER COMMENT 'Id field.'
)
PARTITIONED BY (p_id INTEGER COMMENT 'Id of the partition.')
COMMENT 'A partitioned table.'
STORED AS PARQUET;

CREATE TABLE sql_doc_tables.empty_partitioned_no_comments (
	id INTEGER
)
PARTITIONED BY (p_id INTEGER)
STORED AS PARQUET;
