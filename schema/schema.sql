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

DROP TABLE IF EXISTS public.vpnserversmeta CASCADE;
DROP TABLE IF EXISTS public.vpnserver CASCADE;
DROP TABLE IF EXISTS public.vpnserver_configuration CASCADE;
DROP TABLE IF EXISTS public.country CASCADE;
DROP TABLE IF EXISTS public.state CASCADE;
DROP TABLE IF EXISTS public.city CASCADE;
DROP TABLE IF EXISTS public.geo_position CASCADE;
DROP TABLE IF EXISTS public.vpnserver_status CASCADE;
DROP TABLE IF EXISTS public.configuration_platform CASCADE;
DROP TABLE IF EXISTS public.vpn_type CASCADE;
DROP TABLE IF EXISTS public.vpnserver_connection CASCADE;

CREATE TABLE public.vpnserversmeta
(
    id SERIAL PRIMARY KEY
  , version INT DEFAULT 1 NOT NULL
  , condition_version INT DEFAULT 1 NOT NULL
);

CREATE TABLE public.country
(
    code INT PRIMARY KEY
  , str_code CHAR(3) NOT NULL
  , name VARCHAR(500) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.state
(
    code VARCHAR(3) PRIMARY KEY
  , country_code INT REFERENCES public.country(code)
  , name VARCHAR(500) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.city
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(200) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.geo_position
(
    id SERIAL PRIMARY KEY
  , latitude NUMERIC
  , longitude NUMERIC
  , country_code INT REFERENCES public.country(code) NOT NULL
  , state_code VARCHAR(5) REFERENCES public.state(code)
  , city_id INT REFERENCES public.city(id) NOT NULL
  , region_common INT DEFAULT 0
  , region_dvd INT DEFAULT 0
  , region_xbox360 INT DEFAULT 0
  , region_xboxone INT DEFAULT 0
  , region_playstation3 INT DEFAULT 0
  , region_playstation4 INT DEFAULT 0
  , region_nintendo INT DEFAULT 0
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.vpnserver_status
(
    id SERIAL PRIMARY KEY
  , code VARCHAR(50) NOT NULL
  , description VARCHAR(255) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.vpn_type
(
    id SERIAL PRIMARY KEY
  , code VARCHAR(50) NOT NULL
  , description VARCHAR(255) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.vpnserver
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , ip INET NOT NULL
  , hostname VARCHAR(200)
  , num SERIAL NOT NULL
  , version INT DEFAULT 1 NOT NULL
  , condition_version INT DEFAULT 1 NOT NULL
  , type_id INT REFERENCES public.vpn_type(id) NOT NULL
  , status_id INT REFERENCES public.vpnserver_status(id) NOT NULL
  , bandwidth BIGINT DEFAULT 0
  , load INT DEFAULT 0
  , geo_position_id INT REFERENCES public.geo_position(id) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.configuration_platform
(
    id SERIAL PRIMARY KEY
  , code VARCHAR(50) NOT NULL
  , description VARCHAR(255) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.vpnserver_configuration
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , user_uuid UUID NOT NULL
  , server_uuid UUID REFERENCES public.vpnserver(uuid) UNIQUE NOT NULL
  , file_path VARCHAR(1024) NOT NULL
  , configuration TEXT NOT NULL
  , version INT DEFAULT 1 NOT NULL
  , platform_id INT REFERENCES public.configuration_platform(id) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.vpnserver_connection
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , server_uuid UUID REFERENCES public.vpnserver(uuid) NOT NULL
  , user_email VARCHAR(256)
  , ip_device INET
  , virtual_ip INET
  , bytes_i BIGINT
  , bytes_o BIGINT
  , last_ref TIMESTAMP
  , connected_since TIMESTAMP
);
