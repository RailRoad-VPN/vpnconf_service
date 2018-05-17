SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = ON;
SET check_function_bodies = FALSE;
SET client_min_messages = WARNING;
SET search_path = PUBLIC, extensions;
SET default_tablespace = '';
SET default_with_oids = FALSE;

-- this extension allow to generate uuid as default field, gen_random_uuid - function from this extension
-- https://stackoverflow.com/questions/11584749/how-to-create-a-new-database-with-the-hstore-extension-already-installed

-- CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS public.servers CASCADE;
DROP TABLE IF EXISTS public.server_geo_position CASCADE;
DROP TABLE IF EXISTS public.server_status CASCADE;
DROP TABLE IF EXISTS public.server_type CASCADE;

CREATE TABLE public.server_geo_position
(
    id INT PRIMARY KEY
  , latitude INT
  , longtitude INT
  , country VARCHAR(5)
  , state VARCHAR(100)
  , city VARCHAR(100)
  , region_common INT
  , region_dvd INT
  , region_xbox360 INT
  , region_xboxone INT
  , region_playstation3 INT
  , region_playstation4 INT
  , region_nintendo INT
);

CREATE TABLE public.server_status
(
    id INT PRIMARY KEY
  , name VARCHAR(100) NOT NULL
  , code BYTEA NOT NULL
  , description VARCHAR(255) NOT NULL
);

CREATE TABLE public.server_type
(
    id INT PRIMARY KEY
  , name VARCHAR(100) NOT NULL
  , code BYTEA NOT NULL
  , description VARCHAR(255) NOT NULL
);

CREATE TABLE public.server_configuration
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  ,
);

CREATE TABLE public.server
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , version INT NOT NULL
  , type_id INT REFERENCES public.server_type(id) NOT NULL
  , status_id INT REFERENCES public.server_status(id) NOT NULL
  , bandwidth BIGINT DEFAULT 0
  , load INT DEFAULT 0
  , geo_position_id INT REFERENCES public.server_geo_position(id) NOT NULL
  , created_date BIGINT
);

