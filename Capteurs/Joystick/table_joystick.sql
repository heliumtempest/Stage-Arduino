CREATE TABLE IF NOT EXISTS "Joystick"
(
    id serial NOT NULL,
    "Session" character varying,
    "X" integer,
    "Y" integer,
    "Date" timestamp without time zone,
    PRIMARY KEY (id)
);

ALTER TABLE "Joystick"
    OWNER to postgres;