CREATE OR REPLACE FUNCTION update_vpnserver_version()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.vpnserver
  SET "version" = "version" + 1
  WHERE uuid = NEW.uuid;

  UPDATE public.vpnserversmeta
  SET state_version = state_version + 1;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_vpnserver_state_version()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.vpnserver
  SET state_version = state_version + 1
  WHERE uuid = NEW.uuid;

  UPDATE public.vpnserversmeta
  SET state_version = state_version + 1;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;