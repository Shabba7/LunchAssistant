INSERT INTO public.users (user_id, user_handle, user_name, pass_hash, user_email)
VALUES
  (1, 'ngregori', 'Nelson Gregório', '$2b$12$UBTMLryvaFDpRQfuuaiOnuZYSs6WSHgK7I7uK6CyXy4S2aSCGkyB6', NULL),
  (2, 'emoreira', 'Edgar Moreira', '$2b$12$UBTMLryvaFDpRQfuuaiOnuZYSs6WSHgK7I7uK6CyXy4S2aSCGkyB6', NULL),

INSERT INTO public.restaurants (res_id, res_name, res_loc, res_user)
VALUES
  (1, 'Camada Porto Boavista', '(-8.6306842,41.15695300000001)', 2),
  (2, 'Pizzaria Luzzo | Av. Boavista Porto', '(-8.6335439,41.1584403)', 2),
  (3, 'Casa Isa', '(-8.6338217,41.1585837)', 2),
  (4, 'bbgourmet Porto | Maiorca', '(-8.641944400000002,41.1569444)', 6),
  (5, 'Sushimia Boavista', '(-8.626747199999999,41.1537914)', 6),
  (6, 'Madureira''s Campo Alegre', '(-8.6328328,41.1525172)', 6),
  (7, 'Cacau Wine Terrace', '(-8.6478136,41.1604216)', 6),
  (11, 'Real Hamburgueria', '(-8.6200427,41.1525646)', 6),
  (12, 'Subway Gaia Shopping', '(-8.622617800000002,41.1181929)', 6),
  (13, 'Pão com Manteiga', '(-8.6370871,41.15261999999999)', 6),
  (14, 'Lado B - Mercado Bom Sucesso', '(-8.6292967,41.15553999999999)', 2),
  (15, 'Vitaminas Mercado Bom Sucesso', '(-8.5901683,41.16871159999999)', 2),
  (16, 'Ris8tto Mercado Bom Sucesso', '(-8.6288509,41.1559411)', 2),
  (17, 'Forno do Mercado - Mercado do Bom Sucesso', '(-8.628542,41.15650490000001)', 2),
  (18, 'Chicha', '(-8.6291233,41.1557109)', 1),
  (19, 'My''Kai Poké Bowls', '(-8.6292514,41.1558522)', 7),
  (20, 'RT Focaccias by Reitoria - Mercado Bom Sucesso', '(-8.6293112,41.1557892)', 2),
  (21, 'Tacos & Tequila', '(-8.6293066,41.1555601)', 9);


INSERT INTO public.reviews (user_id, res_id, food_rating, service_rating, price_rating, price_paid, review_date)
VALUES
  (2, 1, 8, 4, 5, 17.00, '2023-08-16 09:43:55.748599'),
  (7, 19, 6, 4, 6, 12.30, '2023-08-16 12:27:32.50532'),
  (1, 18, 7, 9, 7, 10.95, '2023-08-16 12:27:21.225123'),
  (2, 18, 7, 7, 8, 10.95, '2023-08-16 12:31:52.245375'),
  (8, 20, 6, 7, 6, 10.25, '2023-08-16 12:51:41.894862'),
  (9, 21, 8, 7, 6, 12.90, '2023-08-16 12:56:50.857353'),
  (6, 18, 7, 7, 7, 10.95, '2023-08-16 13:58:14.915942'),
  (5, 18, 8, 5, 8, 10.95, '2023-08-16 16:18:38.907546'),
  (5, 1, 8, 5, 5, 17.00, '2023-08-16 16:19:05.265185');
