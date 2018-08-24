INSERT INTO public.vpnserversmeta(id, version, condition_version) VALUES (0, 0, 0);

-- geo position
INSERT INTO public.geo_position(id, latitude, longitude, country_code, state_code, city_id, region_common, region_dvd, region_xbox360, region_xboxone, region_playstation3, region_playstation4, region_nintendo) VALUES (1, 55.108, 54.039, 826, '1', 1, 0, 0, 0, 0, 0, 0, 0);

--
-- vpn server
--

-- openvpn server
INSERT INTO public.vpnserver (uuid, ip, hostname, port, version, condition_version, type_id, status_id, bandwidth, load, geo_position_id) VALUES ('c872e7f0-76d6-4a4e-826e-c56a7c05958a', '192.168.0.1', 'rroad.net', '1194', 1, 1, 1, 1, 0, 0, 1);

--
-- vpn server connection
--

-- windows and openvpn
INSERT INTO public.vpnserver_connection (uuid, server_uuid, user_uuid, user_device_uuid, device_ip, virtual_ip, bytes_i, bytes_o, is_connected, connected_since) VALUES ('d10e7099-1f18-496f-ba6b-6fe3352d565a', 'c872e7f0-76d6-4a4e-826e-c56a7c05958a', 'cf402144-0c02-4b97-98f2-73f7b56160cf', '4c23dffb-2cf2-4173-9d0c-e38caad6e12b', '185.89.8.146', '10.10.0.6', 900, 800, TRUE, now());