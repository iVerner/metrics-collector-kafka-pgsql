-- Table: public.metrics_table

-- DROP TABLE public.metrics_table;

CREATE TABLE public.metrics_table
(
    record_timestamp timestamp with time zone NOT NULL,
    metrics_json json NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE public.metrics_table
    OWNER to pguser;