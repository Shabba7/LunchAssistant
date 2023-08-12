DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Enable for Point data manipulation (similar to PostGIS)
CREATE EXTENSION cube;
CREATE EXTENSION earthdistance;

CREATE TABLE users (
    user_id     SERIAL          PRIMARY KEY,
    user_handle VARCHAR(255)    NOT NULL UNIQUE,
    user_name   VARCHAR(255)    NOT NULL,
    pass_hash   VARCHAR(255)    NOT NULL,
    user_email  VARCHAR(255)
);

CREATE TABLE restaurants (
    res_id      SERIAL                        PRIMARY KEY,
    res_name    VARCHAR(255)                  NOT NULL UNIQUE,
    res_loc     point                         NOT NULL,
    res_user    INT REFERENCES users(user_id) NOT NULL
);

CREATE TABLE reviews(
    user_id         INT REFERENCES users(user_id)       NOT NULL,
    res_id          INT REFERENCES restaurants(res_id)  NOT NULL,
    food_rating     INT              NOT NULL CHECK (food_rating    > 0),
    service_rating  INT              NOT NULL CHECK (service_rating > 0),
    price_rating    INT              NOT NULL CHECK (price_rating   > 0),
    price_paid      NUMERIC(5,2)     NOT NULL CHECK (price_paid     > 0),
    review_date     TIMESTAMP        NOT NULL,
    PRIMARY KEY (user_id, res_id)
);


CREATE VIEW restaurant_quality AS
    SELECT re.res_id, re.res_name, re.res_loc, count(rv.*) review_count,
        avg(rv.food_rating) avg_food, avg(rv.service_rating) avg_service, avg(rv.price_rating) avg_price, avg(rv.price_paid) avg_paid
    FROM restaurants re
    LEFT JOIN reviews rv ON re.res_id = rv.res_id
    GROUP BY re.res_id
;