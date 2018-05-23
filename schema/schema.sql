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

DROP TRIGGER IF EXISTS check_vpnserver_update ON vpnserver CASCADE;
DROP TRIGGER IF EXISTS check_vpnserver_state_update ON vpnserver CASCADE;
DROP TRIGGER IF EXISTS check_vpnserver_configuration_update ON vpnserver_configuration  CASCADE; ;

DROP TABLE IF EXISTS public.vpnserver CASCADE;
DROP TABLE IF EXISTS public.vpnserver_configuration CASCADE;
DROP TABLE IF EXISTS public.country CASCADE;
DROP TABLE IF EXISTS public.state CASCADE;
DROP TABLE IF EXISTS public.city CASCADE;
DROP TABLE IF EXISTS public.geo_position CASCADE;
DROP TABLE IF EXISTS public.vpnserver_status CASCADE;
DROP TABLE IF EXISTS public.vpn_type CASCADE;

CREATE TABLE public.country
(
    code INT PRIMARY KEY
  , str_code CHAR(3) NOT NULL
  , name VARCHAR(500) NOT NULL
  , created_date timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.state
(
    code VARCHAR(3) PRIMARY KEY
  , country_code INT REFERENCES public.country(code)
  , name VARCHAR(500) NOT NULL
  , created_date timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.city
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(200) NOT NULL
  , created_date timestamptz NOT NULL DEFAULT now()
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
  , created_date timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.vpnserver_status
(
    id SERIAL PRIMARY KEY
  , code VARCHAR(50) NOT NULL
  , description VARCHAR(255) NOT NULL
  , created_date timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.vpn_type
(
    id SERIAL PRIMARY KEY
  , code VARCHAR(50) NOT NULL
  , description VARCHAR(255) NOT NULL
  , created_date timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.vpnserver
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , version INT DEFAULT 1 NOT NULL
  , state_version INT DEFAULT 1 NOT NULL
  , type_id INT REFERENCES public.vpn_type(id) NOT NULL
  , status_id INT REFERENCES public.vpnserver_status(id) NOT NULL
  , bandwidth BIGINT DEFAULT 0
  , load INT DEFAULT 0
  , geo_position_id INT REFERENCES public.geo_position(id) NOT NULL
  , created_date timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.vpnserver_configuration
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , user_uuid UUID NOT NULL
  , server_uuid UUID REFERENCES public.vpnserver(uuid) NOT NULL
  , file_path VARCHAR(1024) NOT NULL
  , created_date timestamptz NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION update_vpnserver_version()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.vpnserver
  SET "version" = "version" + 1
  WHERE uuid = NEW.uuid;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_vpnserver_state_version()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.vpnserver
  SET state_version = state_version + 1
  WHERE uuid = NEW.uuid;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_vpnserver_update
  AFTER UPDATE ON public.vpnserver
  FOR EACH ROW
  WHEN (OLD.* IS DISTINCT FROM NEW.* AND pg_trigger_depth() = 0)
  EXECUTE PROCEDURE update_vpnserver_version();

CREATE TRIGGER check_vpnserver_state_update
  AFTER UPDATE ON public.vpnserver
  FOR EACH ROW
  WHEN ((OLD.load IS DISTINCT FROM NEW.load
        OR OLD.bandwidth IS DISTINCT FROM NEW.bandwidth
        OR OLD.geo_position_id IS DISTINCT FROM NEW.geo_position_id) AND pg_trigger_depth() = 0)
  EXECUTE PROCEDURE update_vpnserver_state_version();

CREATE TRIGGER check_vpnserver_configuration_update
  AFTER UPDATE ON public.vpnserver_configuration
  FOR EACH ROW
  WHEN (OLD.* IS DISTINCT FROM NEW.* AND pg_trigger_depth() = 0)
  EXECUTE PROCEDURE update_vpnserver_version();