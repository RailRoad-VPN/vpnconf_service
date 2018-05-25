CREATE OR REPLACE FUNCTION update_vpnserver_version()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.vpnserver
  SET "version" = "version" + 1
  WHERE uuid = NEW.uuid;

  UPDATE public.vpnserversmeta
  SET "version" = "version" + 1;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_vpnserver_condition_version()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.vpnserver
  SET condition_version = condition_version + 1
  WHERE uuid = NEW.uuid;

  UPDATE public.vpnserversmeta
  SET condition_version = condition_version + 1;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;