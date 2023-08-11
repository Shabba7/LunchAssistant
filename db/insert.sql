INSERT INTO users (user_handle, user_name, pass_hash) VALUES('ngregorio', 'Nelson Gregório', '$2b$12$UBTMLryvaFDpRQfuuaiOnuZYSs6WSHgK7I7uK6CyXy4S2aSCGkyB6');
INSERT INTO users (user_handle, user_name, pass_hash) VALUES('emoreira', 'Edgar Moreira', '$2b$12$UBTMLryvaFDpRQfuuaiOnuZYSs6WSHgK7I7uK6CyXy4S2aSCGkyB6');

INSERT INTO restaurants (res_name, res_loc, res_user) VALUES('Passatempo', '-8.627761185482898, 41.156294713236775', '1');
INSERT INTO restaurants (res_name, res_loc, res_user) VALUES('Mimo''s Smoke House ', '-8.632313323917877, 41.158335562806215', '2');
INSERT INTO restaurants (res_name, res_loc, res_user) VALUES('Pizzaria Luzzo', '-8.633543714814978, 41.15845755163155', '1');

INSERT INTO reviews VALUES(1, 1, 5, 5, 4, 10,'2023-08-11 01:08:45.499393'); -- ngregorio review Passatempo
INSERT INTO reviews VALUES(2, 1, 5, 4, 4, 15, '2023-08-12 01:08:45.499393'); -- emoreira review Passatempo