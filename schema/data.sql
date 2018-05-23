INSERT INTO public.vpnserversmeta(id, version, state_version) VALUES (0, 0, 0);

INSERT INTO public.city(id, name, created_date) VALUES (1, 'New York', '2018-05-23 12:26:01.601516');
INSERT INTO public.city(id, name, created_date) VALUES (2, 'Moscow', '2018-05-23 12:26:26.319747');

-- geo position
INSERT INTO public.geo_position(id, latitude, longitude, country_code, state_code, city_id, region_common, region_dvd, region_xbox360, region_xboxone, region_playstation3, region_playstation4, region_nintendo, created_date) VALUES (1, 55.108, 54.039, 826, null, 1, 0, 0, 0, 0, 0, 0, 0, '2018-05-22 13:17:42.947280');

-- vpn server
INSERT INTO public.vpnserver (uuid, version, state_version, type_id, status_id, bandwidth, load, geo_position_id, created_date) VALUES ('c872e7f0-76d6-4a4e-826e-c56a7c05958a', 1, 1, 1, 1, 0, 0, 1, '2018-05-22 13:18:14.041628');
INSERT INTO public.vpnserver (uuid, version, state_version, type_id, status_id, bandwidth, load, geo_position_id, created_date) VALUES ('ef0bd460-a8ee-4cf4-9d8d-f8367ccaff34', 1, 1, 2, 2, 0, 0, 1, '2018-05-23 17:07:22.894000');

-- vpn server configuration
INSERT INTO public.vpnserver_configuration(uuid, user_uuid, server_uuid, file_path, created_date) VALUES ('8f525324-f752-4135-bab7-38e0f1ff96f9', 'c872e7f0-76d6-4a4e-826e-c56a7c05958a', 'c872e7f0-76d6-4a4e-826e-c56a7c05958a', '/file/path', '2018-05-22 13:25:29.392613');