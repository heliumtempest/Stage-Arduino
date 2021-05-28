CREATE TABLE IF NOT EXISTS "Micro"
(
    id serial NOT NULL,
    "Session" character varying,
    "Date" timestamp without time zone,
    "Tension" integer,
    PRIMARY KEY (id)
);

ALTER TABLE public."Micro"
    OWNER to postgres;