INSERT INTO users (user_handle, user_name, pass_hash) VALUES('ngregorio', 'Nelson Gregório', 'abc123');
INSERT INTO users (user_handle, user_name, pass_hash) VALUES('bmoreira', 'Edgar Moreira', 'abc123');

INSERT INTO restaurants (res_name, res_loc) VALUES('Passatempo', '-8.627761185482898, 41.156294713236775');
INSERT INTO restaurants (res_name, res_loc) VALUES('Mimo''s Smoke House ', '-8.632313323917877, 41.158335562806215');
INSERT INTO restaurants (res_name, res_loc) VALUES('Pizzaria Luzzo', '-8.633543714814978, 41.15845755163155');

INSERT INTO reviews VALUES(1, 1, 5, 5, 4, 10); -- ngregorio review Passatempo
INSERT INTO reviews VALUES(2, 1, 5, 4, 4, 15); -- bmoreira review Passatempo