INSERT INTO public.users (user_id, user_handle, user_name, pass_hash, user_email)
VALUES
  (1, 'ngregori', 'Nelson Gregório', '$2b$12$UBTMLryvaFDpRQfuuaiOnuZYSs6WSHgK7I7uK6CyXy4S2aSCGkyB6', NULL),
  (2, 'emoreira', 'Edgar Moreira', '$2b$12$UBTMLryvaFDpRQfuuaiOnuZYSs6WSHgK7I7uK6CyXy4S2aSCGkyB6', NULL);

INSERT INTO public.restaurants (res_id, res_name, res_loc, res_user)
VALUES
  (1, 'Camada Porto Boavista', '(-8.6306842,41.15695300000001)', 2),
  (2, 'Pizzaria Luzzo | Av. Boavista Porto', '(-8.6335439,41.1584403)', 2),
  (3, 'Casa Isa', '(-8.6338217,41.1585837)', 2),
  (14, 'Lado B - Mercado Bom Sucesso', '(-8.6292967,41.15553999999999)', 2),
  (15, 'Vitaminas Mercado Bom Sucesso', '(-8.5901683,41.16871159999999)', 2),
  (16, 'Ris8tto Mercado Bom Sucesso', '(-8.6288509,41.1559411)', 2),
  (17, 'Forno do Mercado - Mercado do Bom Sucesso', '(-8.628542,41.15650490000001)', 2),
  (18, 'Chicha', '(-8.6291233,41.1557109)', 1),
  (20, 'RT Focaccias by Reitoria - Mercado Bom Sucesso', '(-8.6293112,41.1557892)', 2);


INSERT INTO public.reviews (user_id, res_id, food_rating, service_rating, price_rating, price_paid, review_date, comment)
VALUES
  (2, 1, 8, 4, 5, 17.00, '2023-08-16 09:43:55.748599', ''),
  (1, 18, 7, 9, 7, 10.95, '2023-08-16 12:27:21.225123', ''),
  (2, 18, 7, 7, 8, 10.95, '2023-08-16 12:31:52.245375', '');