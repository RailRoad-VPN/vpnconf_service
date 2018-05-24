-- increment VPN Server version when any field was changed
CREATE TRIGGER check_vpnserver_update
  AFTER UPDATE ON public.vpnserver
  FOR EACH ROW
  WHEN (OLD.* IS DISTINCT FROM NEW.* AND pg_trigger_depth() = 0)
  EXECUTE PROCEDURE update_vpnserver_version();

-- increment VPN Server state version when vpn server fields (on of) load or bandwidth or geo_pos_id were changed
CREATE TRIGGER check_vpnserver_state_update
  AFTER UPDATE ON public.vpnserver
  FOR EACH ROW
  WHEN ((OLD.load IS DISTINCT FROM NEW.load
        OR OLD.bandwidth IS DISTINCT FROM NEW.bandwidth
        OR OLD.geo_position_id IS DISTINCT FROM NEW.geo_position_id) AND pg_trigger_depth() = 0)
  EXECUTE PROCEDURE update_vpnserver_state_version();

-- increment version when VPN Server configuration changed
CREATE TRIGGER check_vpnserver_configuration_update
  AFTER UPDATE ON public.vpnserver_configuration
  FOR EACH ROW
  WHEN (OLD.* IS DISTINCT FROM NEW.* AND pg_trigger_depth() = 0)
  EXECUTE PROCEDURE update_vpnserver_version();