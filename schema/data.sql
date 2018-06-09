INSERT INTO public.vpnserversmeta(id, version, condition_version) VALUES (0, 0, 0);

INSERT INTO public.city(id, name, created_date) VALUES (1, 'New York', '2018-05-23 12:26:01.601516');
INSERT INTO public.city(id, name, created_date) VALUES (2, 'Moscow', '2018-05-23 12:26:26.319747');

INSERT INTO public.state (code, country_code, name, created_date) VALUES ('1', 826, 'SY', '2018-05-31 16:58:48.984279');
INSERT INTO public.state (code, country_code, name, created_date) VALUES ('2', 643, 'NY', '2018-05-31 16:58:55.672343');

-- geo position
INSERT INTO public.geo_position(id, latitude, longitude, country_code, state_code, city_id, region_common, region_dvd, region_xbox360, region_xboxone, region_playstation3, region_playstation4, region_nintendo, created_date) VALUES (1, 55.108, 54.039, 826, '1', 1, 0, 0, 0, 0, 0, 0, 0, '2018-05-22 13:17:42.947280');

--
-- vpn server
--

-- openvpn
INSERT INTO public.vpnserver (uuid, version, condition_version, type_id, status_id, bandwidth, load, geo_position_id, created_date) VALUES ('c872e7f0-76d6-4a4e-826e-c56a7c05958a', 1, 1, 1, 1, 0, 0, 1, '2018-05-22 13:18:14.041628');

-- ikev2
INSERT INTO public.vpnserver (uuid, version, condition_version, type_id, status_id, bandwidth, load, geo_position_id, created_date) VALUES ('699bba8d-7a50-4838-8c6e-ceed49d0f820', 1, 1, 1, 1, 0, 0, 1, '2018-06-04 17:17:34.824795');

--
-- vpn server configuration
--

-- openvpn
INSERT INTO public.vpnserver_configuration(uuid, user_uuid, server_uuid, configuration, file_path, created_date) VALUES ('8f525324-f752-4135-bab7-38e0f1ff96f9', 'cf402144-0c02-4b97-98f2-73f7b56160cf', 'c872e7f0-76d6-4a4e-826e-c56a7c05958a', 'Y2xpZW50CmRldiB0dW4KcHJvdG8gdWRwCnNuZGJ1ZiAwCnJjdmJ1ZiAwCnJlbW90ZSAxOTMuNzAuNzMuMjQyIDUxMjQxCnJlc29sdi1yZXRyeSBpbmZpbml0ZQpub2JpbmQKcGVyc2lzdC1rZXkKcGVyc2lzdC10dW4KcmVtb3RlLWNlcnQtdGxzIHNlcnZlcgphdXRoIFNIQTUxMgpjaXBoZXIgQUVTLTI1Ni1DQkMKY29tcC1sem8Kc2V0ZW52IG9wdCBibG9jay1vdXRzaWRlLWRucwprZXktZGlyZWN0aW9uIDEKdmVyYiAzCjxjYT4KLS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLekNDQWhPZ0F3SUJBZ0lKQU9aOFl3b0NQQUd5TUEwR0NTcUdTSWIzRFFFQkN3VUFNQk14RVRBUEJnTlYKQkFNTUNFTm9ZVzVuWlUxbE1CNFhEVEUzTURreU9ERXpNRFF4TWxvWERUSTNNRGt5TmpFek1EUXhNbG93RXpFUgpNQThHQTFVRUF3d0lRMmhoYm1kbFRXVXdnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCRHdBd2dnRUtBb0lCCkFRRGwrdzBFZ3ZnVzVtNG9SNFZOOFhiTkdIczVGNkMyaTVVMWxRaU5IcXR1MWI1cFNrRHRTNEpkcU40OEFKd3UKbDVPa2hLODFkYXkwbThCbmpzNFAveElvcmt6NTE5NVJXNGI4anFodGtrK0ZrZlI0M3F0WldJMHVMUVhicGxlZwpqdXdlLzR5MzRwdSs4VXF2cmQzenJPMDZZMXZSMXpQZ1NxM2t4Z2NELzhpTHlmNU5yTTA1U2RLNVhaWk1kbWxrCmZKd0ZsOTV5S1ZmWjJ0K3cwZ3oxWHJkcUwrRWJOUWR5SFdVYUFBM0NtY2JQSlRJWFoyaW9MQVJPVVlDbEtVaCsKemhEWEROUzFvOVI3bzdpaUlpay8wRGdnNWtaVmxuaXZuS2ZUTk8xM1R5NlpxYlhBQWxxczlhZjZaeThXZEVkTgpra2FoZXZXYlNtaVhyQ1A2K3dJd0V3T3JBZ01CQUFHamdZRXdmekFkQmdOVkhRNEVGZ1FVY3lnRU1DSmdzN3lkClNnZ0thUDdCN1dVaXcxZ3dRd1lEVlIwakJEd3dPb0FVY3lnRU1DSmdzN3lkU2dnS2FQN0I3V1VpdzFpaEY2UVYKTUJNeEVUQVBCZ05WQkFNTUNFTm9ZVzVuWlUxbGdna0E1bnhqQ2dJOEFiSXdEQVlEVlIwVEJBVXdBd0VCL3pBTApCZ05WSFE4RUJBTUNBUVl3RFFZSktvWklodmNOQVFFTEJRQURnZ0VCQU45c1NCTTRPdlZCeFFxVDFOWmJneGs1ClZmSnA0WnIrR1VkYXllWDNMUCtxTXFhZGhNWitIZ2xjTTduc2NxaloyM2ZQMUpyMzBvbmxLSDg4ZTAzR09UU0cKQUU5YzVJMnVhWjd2eWxGMS83TDV0a3pMd1ZEWlpzTEtMT2s1aTlqUmtUckNsZFpadGE2V3NXR1lScXQyTFV5RQp6K3pDRjUzcEttWkNuWjZxanNKUCtmbzdSRDVXcDhiU2VhRGIzR3lIT3dvSU5VN1ppNE12OE5HdkFoSDlyWTJ1CitJWGlIa3R3NWpHc1lnTjlvUm1qV1IwR2lUNEwydlYyL2NaVzFVWjdLZ2dsOHRqc1hFT0pWcG5IMWtTMW12ZkIKR0hHNGw3UmtoNnhuSjR4TmxlVnE4amtGYUx2VGRUQUxYUXByREtJdGFiTTNMWVFrb0FHbGZxUnhwWjY2T2J3PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCjwvY2E+CjxjZXJ0PgpDZXJ0aWZpY2F0ZToKICAgIERhdGE6CiAgICAgICAgVmVyc2lvbjogMyAoMHgyKQogICAgICAgIFNlcmlhbCBOdW1iZXI6CiAgICAgICAgICAgIDc1OjE2OjY4OmE2OjU0OmZhOmFhOjg0OmEzOmZhOmJlOjdhOjYwOjY2OjJkCiAgICBTaWduYXR1cmUgQWxnb3JpdGhtOiBzaGEyNTZXaXRoUlNBRW5jcnlwdGlvbgogICAgICAgIElzc3VlcjogQ049Q2hhbmdlTWUKICAgICAgICBWYWxpZGl0eQogICAgICAgICAgICBOb3QgQmVmb3JlOiBNYXkgMzEgMTM6NDU6MjggMjAxOCBHTVQKICAgICAgICAgICAgTm90IEFmdGVyIDogTWF5IDI4IDEzOjQ1OjI4IDIwMjggR01UCiAgICAgICAgU3ViamVjdDogQ049dGVzdF9hcGkKICAgICAgICBTdWJqZWN0IFB1YmxpYyBLZXkgSW5mbzoKICAgICAgICAgICAgUHVibGljIEtleSBBbGdvcml0aG06IHJzYUVuY3J5cHRpb24KICAgICAgICAgICAgICAgIFB1YmxpYy1LZXk6ICgyMDQ4IGJpdCkKICAgICAgICAgICAgICAgIE1vZHVsdXM6CiAgICAgICAgICAgICAgICAgICAgMDA6YWY6YzU6ZDc6MmM6NGQ6ZWU6NWU6YWQ6OTg6YTM6MzY6ODU6NjU6OTU6CiAgICAgICAgICAgICAgICAgICAgOGM6ZDM6MzI6NGQ6Mjg6NjA6ZGE6YTc6OWI6ZGM6NjY6YzU6NDc6Nzk6OGU6CiAgICAgICAgICAgICAgICAgICAgYWM6MTE6NWI6MTg6Y2M6MDY6OGI6Nzk6ZGI6MTg6MjU6ZDE6NTg6ZTE6NmI6CiAgICAgICAgICAgICAgICAgICAgYjM6MWU6YzU6Mjc6N2U6MzM6MDM6OWI6NGY6ZDU6YmM6YWQ6NTk6MTM6OWY6CiAgICAgICAgICAgICAgICAgICAgODM6NzQ6Mzc6MGY6YjU6YzM6MTc6NWM6YjQ6ODU6NGM6Y2E6Njg6NDc6YWY6CiAgICAgICAgICAgICAgICAgICAgMzU6ZDU6YWQ6ZjY6NzE6N2M6MTA6MmQ6YmU6OTY6NzE6MDQ6MmI6MjY6MzQ6CiAgICAgICAgICAgICAgICAgICAgYTI6ZDY6MmU6NjQ6N2Q6ZmM6OWM6NjY6MDk6YjU6NmI6OWY6MjU6ODU6OTQ6CiAgICAgICAgICAgICAgICAgICAgYjg6M2M6MzU6N2E6NDY6NTc6M2Y6MGY6OTU6ZWY6NTM6ZDY6ZTE6ZmY6NDE6CiAgICAgICAgICAgICAgICAgICAgZWI6ZmU6MjA6NTU6MDk6MTY6NGU6NTQ6NDM6MjM6ZmE6YjU6MmQ6OGU6Y2Y6CiAgICAgICAgICAgICAgICAgICAgYWU6MWY6M2U6MDA6MjU6OTM6MzI6MWQ6Yjg6MmQ6MDQ6YWM6MmU6M2I6NTg6CiAgICAgICAgICAgICAgICAgICAgM2I6OGE6NWU6Zjk6M2I6Zjc6NjQ6MDY6M2U6ODY6ZTA6ODA6Nzk6MDc6MDQ6CiAgICAgICAgICAgICAgICAgICAgYTI6Y2U6ZDQ6NjA6OWY6ODQ6MGU6OWM6YTA6NjY6OTg6YzI6ZmY6YmE6ZDc6CiAgICAgICAgICAgICAgICAgICAgNDM6NzY6ZTI6NzM6ZGM6YzY6ZTY6Nzk6ODg6ZDI6YTE6NDc6MTk6NWY6YTE6CiAgICAgICAgICAgICAgICAgICAgZDE6NDM6Y2M6ZDU6MGE6YWI6ZmQ6NDE6MTc6N2M6MTc6NTY6YzE6YjA6ZTQ6CiAgICAgICAgICAgICAgICAgICAgOWY6NmU6NGI6MDQ6ZDI6NGU6NjQ6OTE6ZWE6Mzg6OWY6ZmE6NGM6NGQ6MTE6CiAgICAgICAgICAgICAgICAgICAgYTk6ODM6ZmI6NGU6OGY6MmI6NDQ6ZDc6OTk6YmE6MjE6Mzg6MGQ6NjQ6Y2E6CiAgICAgICAgICAgICAgICAgICAgNGI6ZDc6M2U6NTM6Njc6ZDk6MDY6Zjk6Yzg6ZDc6YTA6ODc6YmM6YzQ6NDk6CiAgICAgICAgICAgICAgICAgICAgNDM6MmIKICAgICAgICAgICAgICAgIEV4cG9uZW50OiA2NTUzNyAoMHgxMDAwMSkKICAgICAgICBYNTA5djMgZXh0ZW5zaW9uczoKICAgICAgICAgICAgWDUwOXYzIEJhc2ljIENvbnN0cmFpbnRzOiAKICAgICAgICAgICAgICAgIENBOkZBTFNFCiAgICAgICAgICAgIFg1MDl2MyBTdWJqZWN0IEtleSBJZGVudGlmaWVyOiAKICAgICAgICAgICAgICAgIEZFOkUwOjFEOjdDOkRFOjBDOjI3OjFFOjI3OkRCOkFFOjQzOkRDOkEyOjQ2OjVBOkJBOjg3OjY0OjVDCiAgICAgICAgICAgIFg1MDl2MyBBdXRob3JpdHkgS2V5IElkZW50aWZpZXI6IAogICAgICAgICAgICAgICAga2V5aWQ6NzM6Mjg6MDQ6MzA6MjI6NjA6QjM6QkM6OUQ6NEE6MDg6MEE6Njg6RkU6QzE6RUQ6NjU6MjI6QzM6NTgKICAgICAgICAgICAgICAgIERpck5hbWU6L0NOPUNoYW5nZU1lCiAgICAgICAgICAgICAgICBzZXJpYWw6RTY6N0M6NjM6MEE6MDI6M0M6MDE6QjIKCiAgICAgICAgICAgIFg1MDl2MyBFeHRlbmRlZCBLZXkgVXNhZ2U6IAogICAgICAgICAgICAgICAgVExTIFdlYiBDbGllbnQgQXV0aGVudGljYXRpb24KICAgICAgICAgICAgWDUwOXYzIEtleSBVc2FnZTogCiAgICAgICAgICAgICAgICBEaWdpdGFsIFNpZ25hdHVyZQogICAgU2lnbmF0dXJlIEFsZ29yaXRobTogc2hhMjU2V2l0aFJTQUVuY3J5cHRpb24KICAgICAgICAgMWM6YzU6MWE6Nzc6YjY6OTM6NDE6ZTk6MmM6NzI6YmI6ODk6ZmU6YjA6ODc6NGY6ODM6Y2E6CiAgICAgICAgIDg2OmVjOmRkOjQxOmQyOmQ4OjEyOjg2OmU0OmVkOjc1OjRkOjIwOjg4OjRiOjg5OjU0OjFiOgogICAgICAgICBiOTphYTplNTo4MzpjMTowYTo0Njo3Nzo2NzpkNTpjMToyNzphYjpmNjplODo3YjphMDoxZjoKICAgICAgICAgZjk6YjA6YWU6NDM6MDc6ZTk6NDQ6ZTA6YTc6NjI6NDE6NjE6MjE6ZWM6ZTk6ZGY6ODQ6OWY6CiAgICAgICAgIDExOjc5Ojg2OmY2OjcwOjQ0OmQ1OjJhOjM3OmJhOjdmOjUzOmZhOjk1OjE5OmUyOjA1OjQ5OgogICAgICAgICAxNzoxYzphMDpjNzo1MjoyYzphNzo4ZDo2NTpiYToxZDo1ODozMzo4ZjpkNzo4YTpjNDo3ODoKICAgICAgICAgNDY6NDc6NTI6NjM6ZTA6NjI6NGQ6OWE6NzE6MTA6YTA6NzA6MGE6N2E6YjM6ZTU6OWU6OGM6CiAgICAgICAgIGJiOmJlOjdjOjFkOjA0OmJjOmUxOjcwOjYxOjk3OmY0OjI3OmY5OjNlOjk4OjAyOjkyOjA1OgogICAgICAgICBkNDoxNjpmYjowNjo0MjplODo2MDphNTpmNjphNTpmODozOTo1NTpkOTpjYjo1ZDo2Zjo0YzoKICAgICAgICAgNDY6YjE6YzI6MTE6MGY6OTg6MTU6ZTE6NTY6MmI6ZTQ6YjU6ZjQ6ZGU6MGU6ZDM6ZDU6Yzg6CiAgICAgICAgIDdiOjQxOjY2OmRmOmUwOmNmOjExOjVhOjZjOjBiOmRmOmZkOjkzOmZkOjVhOmQzOmRhOjIyOgogICAgICAgICAxYTo4Yzo5MTplMzpjYTo2ZjoyZjplNjoyNzpkNDo1MTphYzphNjo0ZDphYTphNzphMTpiNDoKICAgICAgICAgMjU6Mzg6NDQ6ZDQ6NmY6ODE6YWM6YTQ6Yjk6NmI6YjY6YTM6MGM6YTA6M2Y6ZWI6MjA6NzY6CiAgICAgICAgIGI0OjY0OmE2OjU5OmFlOjRiOjdkOmI1OmM1OmJmOjE1OjI1Ojc2OjNhOjI3OjI2OmFlOmE2OgogICAgICAgICBlZDo5ODo2YTpjNQotLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS0KTUlJRFJEQ0NBaXlnQXdJQkFnSVBkUlpvcGxUNnFvU2orcjU2WUdZdE1BMEdDU3FHU0liM0RRRUJDd1VBTUJNeApFVEFQQmdOVkJBTU1DRU5vWVc1blpVMWxNQjRYRFRFNE1EVXpNVEV6TkRVeU9Gb1hEVEk0TURVeU9ERXpORFV5Ck9Gb3dFekVSTUE4R0ExVUVBd3dJZEdWemRGOWhjR2t3Z2dFaU1BMEdDU3FHU0liM0RRRUJBUVVBQTRJQkR3QXcKZ2dFS0FvSUJBUUN2eGRjc1RlNWVyWmlqTm9WbGxZelRNazBvWU5xbm05eG14VWQ1anF3Uld4ak1Cb3Q1MnhnbAowVmpoYTdNZXhTZCtNd09iVDlXOHJWa1RuNE4wTncrMXd4ZGN0SVZNeW1oSHJ6WFZyZlp4ZkJBdHZwWnhCQ3NtCk5LTFdMbVI5L0p4bUNiVnJueVdGbExnOE5YcEdWejhQbGU5VDF1SC9RZXYrSUZVSkZrNVVReVA2dFMyT3o2NGYKUGdBbGt6SWR1QzBFckM0N1dEdUtYdms3OTJRR1BvYmdnSGtIQktMTzFHQ2ZoQTZjb0dhWXd2KzYxME4yNG5QYwp4dVo1aU5LaFJ4bGZvZEZEek5VS3EvMUJGM3dYVnNHdzVKOXVTd1RTVG1TUjZqaWYra3hORWFtRCswNlBLMFRYCm1ib2hPQTFreWt2WFBsTm4yUWI1eU5lZ2g3ekVTVU1yQWdNQkFBR2pnWlF3Z1pFd0NRWURWUjBUQkFJd0FEQWQKQmdOVkhRNEVGZ1FVL3VBZGZONE1KeDRuMjY1RDNLSkdXcnFIWkZ3d1F3WURWUjBqQkR3d09vQVVjeWdFTUNKZwpzN3lkU2dnS2FQN0I3V1VpdzFpaEY2UVZNQk14RVRBUEJnTlZCQU1NQ0VOb1lXNW5aVTFsZ2drQTVueGpDZ0k4CkFiSXdFd1lEVlIwbEJBd3dDZ1lJS3dZQkJRVUhBd0l3Q3dZRFZSMFBCQVFEQWdlQU1BMEdDU3FHU0liM0RRRUIKQ3dVQUE0SUJBUUFjeFJwM3RwTkI2U3h5dTRuK3NJZFBnOHFHN04xQjB0Z1NodVR0ZFUwZ2lFdUpWQnU1cXVXRAp3UXBHZDJmVndTZXI5dWg3b0IvNXNLNURCK2xFNEtkaVFXRWg3T25maEo4UmVZYjJjRVRWS2plNmYxUDZsUm5pCkJVa1hIS0RIVWl5bmpXVzZIVmd6ajllS3hIaEdSMUpqNEdKTm1uRVFvSEFLZXJQbG5veTd2bndkQkx6aGNHR1gKOUNmNVBwZ0NrZ1hVRnZzR1F1aGdwZmFsK0RsVjJjdGRiMHhHc2NJUkQ1Z1Y0VllyNUxYMDNnN1QxY2g3UVdiZgo0TThSV213TDMvMlQvVnJUMmlJYWpKSGp5bTh2NWlmVVVheW1UYXFub2JRbE9FVFViNEdzcExscnRxTU1vRC9yCklIYTBaS1pacmt0OXRjVy9GU1YyT2ljbXJxYnRtR3JGCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0KPC9jZXJ0Pgo8a2V5PgotLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS0KTUlJRXZRSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2N3Z2dTakFnRUFBb0lCQVFDdnhkY3NUZTVlclppagpOb1ZsbFl6VE1rMG9ZTnFubTl4bXhVZDVqcXdSV3hqTUJvdDUyeGdsMFZqaGE3TWV4U2QrTXdPYlQ5VzhyVmtUCm40TjBOdysxd3hkY3RJVk15bWhIcnpYVnJmWnhmQkF0dnBaeEJDc21OS0xXTG1SOS9KeG1DYlZybnlXRmxMZzgKTlhwR1Z6OFBsZTlUMXVIL1FlditJRlVKRms1VVF5UDZ0UzJPejY0ZlBnQWxreklkdUMwRXJDNDdXRHVLWHZrNwo5MlFHUG9iZ2dIa0hCS0xPMUdDZmhBNmNvR2FZd3YrNjEwTjI0blBjeHVaNWlOS2hSeGxmb2RGRHpOVUtxLzFCCkYzd1hWc0d3NUo5dVN3VFNUbVNSNmppZitreE5FYW1EKzA2UEswVFhtYm9oT0Exa3lrdlhQbE5uMlFiNXlOZWcKaDd6RVNVTXJBZ01CQUFFQ2dnRUFBd2NzZXNYbzZsYWhQNGFMNjhFVXlQcWYyNmMzZlJXeFNVL3l1RVJkOEhxYQpSY0dERzVsTHBETWtEZFlXSXR5UW5wcndYL2VUSGduNmM5MFduYVRwTDE5cUFwM1ZnZ29tbTcySDl1TmxVSFVyCnJpNFBWMmtUK1RlRTZwMm4rNGVqaGhwNnRwenFQNC9kVUtRM05Ba0N2QmtBSTNpYk1oT0hwandXV3U2NGNMa2sKRU5kRHhINHp6Q3BLcmtiQnFCL0J4THEyMDZJSXNad2FFaEtrUVNNZXNyeU0wTUliS0Z2aGNrcG16c2h3OE1zSApqYVZlTWpOb0xKVXVqQ0ZvVUlVR1NXQ3FwdUNCWEZPaXhBNVpweGRJN2Vwdzk3STE0THRxbS9wZHIyM0JNZjBSCnMzempjTERWZkhITyt2THNNZDUrRHFSaXhzdW9IK29MaDVKS0dWK3VZUUtCZ1FEWjNidDZQd1ZUV2RQaU5qdFMKcEtzNnVTZGNlWFRrcGRmb1Z5TUt2U0hYOGJnUmlwdWFMUW1Ha1oySWtQaEk4NmpoNVlZcGxtVEo1NGdKdXBSZApJYSthbmtDY1Q5MVJHK0JDazdOQW9vc0l3K0czWWhsaDE5Qzg1Wm1QNGdoSDZhelJQR3VwbkJ6VDVzVnp4aTJGCmp6ZzlaSmRIVk5wblk0am93RGpaMit4TWNRS0JnUURPaWZlRmtER3Z1QVFkV2tVUllvSXpRd1VJalZCVTdzY1UKNzQxTlVXcTQ4VGlGSHNmVmdnbnVwazk4ZXU4bXFXckN3TzFkLzk5T3pwNFJSK3YzNVZOSm10ZktRZWJZVWxidQpyRHRCdEliSk5NNk54UzVVL1Y4eGNuL21QTk5EdGFUYngvNktnK01YaWRGMUh2bDk1NDM5M1ZuYmdqcjA4U05ECkZsREdhZU1IV3dLQmdGdTBhNisvU3p5VWVRMmxDajkxTk9ZWS9hcDlMV2o1TGZLTWl5R0FEdmpZdEVRZDlmVmwKczdiRElHNVZwMHo5MHo2UzRIQXM3K3ZVMjN4TTN4cDhqWEFsNE1ockRadVFna3RENUpYMlZWT3hNQmVDNFhBLwo2WXM1a2ZQd2pzL0dXb29RUnJrMER5WmE0dzRpZ3hMUEFEdEhWaTRlVjNoaGUwV05jK0N3STd6aEFvR0JBSU84Ck9qVmxzRnRjNnJyeUhjV2w2RmZiOG5UdTlZTUd2ZEpick92WTkxSTVBWXpmQWlUcmlYdy9kY2wyKzl6VUNIVnAKNnJ5ZS9JYmVnTEdUQnk0WmhsTVhRWFlQTExkalpYRmNSM3QwTXRoWkp6b0R2N2FUMlVqSHVFNVpFNE5IYzN4LwpocHBBM3ZMZmc4ckpVK2I3YjNTeDM2T0Q0Q2psT1ZHTUJUOVl3R2FyQW9HQVEyZ2daTE5MbW9OV2tXekZjNHIzCkl0a3UrMGI1cDRvWmNqd1cwVVVMZ1I0ak1Fb1hhZ2xrRGtiaXFCMHBhVUVhL0xWMDVhaytLNEZUK1FjL3JOb24KR0Y2OUVCb25qdkg1cENkSEE3aE5hYi9GdWFsVVRhcDNLbHdRUmJialkrd2VPeWVLaGlkWStjNTBnTEJLMGlUNgo2blhTNk8waGhud1ZYaEpvNHNRMFZKaz0KLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQo8L2tleT4KPHRscy1hdXRoPgojCiMgMjA0OCBiaXQgT3BlblZQTiBzdGF0aWMga2V5CiMKLS0tLS1CRUdJTiBPcGVuVlBOIFN0YXRpYyBrZXkgVjEtLS0tLQo3NTMzOWRhYTVjOTUzYjk1NjMxNTYyZDcwYTVhMGQ5OQoyMDYyZDEyZWY2OTg2MGJiNTJjMDU5ODM2MGViNThlNwoxNjBhM2IwM2VjMDU1NzU2ODZjZGM1ZjEyYjk1OTM2ZAo5MzM3OThhMGY3ZTdiMTZiYzE5MzdkMGRlMjE4ZWNkNwphZGFjZTBhZTRkODlhZjE5NzBhMjIzZWFkYjE1Yjc2ZQpkZWQyZmQwN2ZkMmQyZThlZTNkMTM1YWUwZmYwNmIzMgphNTdiNTRiYjdmZjE0Nzk3YjcyYjhlMjYyMGQ4YjIwYwowMTNmYjQxMTdlYzQwYWU4MTdmMzRiNDFjMGQ4MTRhMAowNDcyMjViNWY0OWZhM2U0ZWQ3MGExZjExYmYzNDA0NAphNjdkMTM2MzM5ZGY4MWZiOTg4YzEzNmZkYzcyZGZjMwo5MjZiMWZkMjIzNmE5YzI3ZmRhYzI0YmEwMWNlZDkxOAo1ODIwNjkzMTZlOTdhMmQ4YTQwZDM4MDY5MDhiYzFjYgo2YzZjYjhjNWRjNjgwZTE0ZjFlNzExOTZlNjM0OTI5ZgpjZDQ3OGUwYThiMDVmMmQ4MDg1Mzg3NzA4MzJiYmQ2MgowYWViM2U2YjBhNmUxMzA0NjBmOGQzMzYxNDE3NDgxMwoxNTI4Mjk5MGViNzE1OWUxNGRiZDhlODE3YzRlMDhiZAotLS0tLUVORCBPcGVuVlBOIFN0YXRpYyBrZXkgVjEtLS0tLQo8L3Rscy1hdXRoPgo=', '/file/path', '2018-05-22 13:25:29.392613');

-- ipsec ikev2
INSERT INTO public.vpnserver_configuration(uuid, user_uuid, server_uuid, configuration, file_path, created_date) VALUES ('9a84de20-3bee-4329-9b8c-96eb3600c690', 'cf402144-0c02-4b97-98f2-73f7b56160cf', 'c872e7f0-76d6-4a4e-826e-c56a7c05958a', '', '/file/path', '2018-05-22 13:25:29.392613');