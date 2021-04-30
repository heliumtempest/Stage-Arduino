CREATE TABLE IF NOT EXISTS cardio
(
    id serial NOT NULL,
    "Date" timestamp without time zone,
    "Session" character varying,
    "Pulsation" integer,
    PRIMARY KEY (id)
);

ALTER TABLE public.cardio
    OWNER to postgres;