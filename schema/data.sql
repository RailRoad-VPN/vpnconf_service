TRUNCATE public.vpnserversmeta CASCADE;
TRUNCATE public.vpnserver CASCADE;
TRUNCATE public.vpnserver_connection CASCADE;
TRUNCATE public.geo_position CASCADE;

INSERT INTO public.vpnserversmeta(id, version, condition_version) VALUES (0, 0, 0);

-- geo position
INSERT INTO public.geo_position(id, latitude, longitude, country_code, state_code, city_id, region_common, region_dvd, region_xbox360, region_xboxone, region_playstation3, region_playstation4, region_nintendo) VALUES (1, 55.108, 54.039, 826, '1', 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO public.geo_position(id, latitude, longitude, country_code, state_code, city_id, region_common, region_dvd, region_xbox360, region_xboxone, region_playstation3, region_playstation4, region_nintendo) VALUES (2, 55.108, 54.039, 36, '3', 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO public.geo_position(id, latitude, longitude, country_code, state_code, city_id, region_common, region_dvd, region_xbox360, region_xboxone, region_playstation3, region_playstation4, region_nintendo) VALUES (3, 55.108, 54.039, 533, '4', 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO public.geo_position(id, latitude, longitude, country_code, state_code, city_id, region_common, region_dvd, region_xbox360, region_xboxone, region_playstation3, region_playstation4, region_nintendo) VALUES (4, 55.108, 54.039, 248, '5', 1, 0, 0, 0, 0, 0, 0, 0);

--
-- vpn server
--

-- openvpn server
INSERT INTO public.vpnserver (uuid, ip, hostname, port, version, condition_version, type_id, status_id, bandwidth, load, geo_position_id) VALUES ('c872e7f0-76d6-4a4e-826e-c56a7c05958a', '91.121.50.14', 'rrnovpn2', '51241', 1, 1, 1, 1, 0, 0, 1);