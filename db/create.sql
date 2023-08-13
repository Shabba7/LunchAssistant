DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Enable for Point data manipulation (similar to PostGIS)
CREATE EXTENSION cube;
CREATE EXTENSION earthdistance;

------------------------------------------
--           TABLES
------------------------------------------
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
    food_rating     INT NOT NULL CHECK (food_rating    > 0),
    service_rating  INT NOT NULL CHECK (service_rating > 0),
    price_rating    INT NOT NULL CHECK (price_rating   > 0),
    price_paid      INT NOT NULL CHECK (price_paid     > 0),
    review_date     TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, res_id)
);

CREATE TABLE elections (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    restaurant_ids INT[] NOT NULL
);

CREATE TABLE votes (
    election_id INT REFERENCES elections(id),
    voter_id INT REFERENCES users(user_id),
    restaurant_id INT REFERENCES restaurants(res_id),
    PRIMARY KEY (election_id, voter_id, restaurant_id)
);


------------------------------------------
--           FUNCTIONS
------------------------------------------
CREATE OR REPLACE FUNCTION start_election(ids INT[]) RETURNS VOID AS $$
BEGIN
    -- Check if an open election already exists
    IF EXISTS (SELECT 1 FROM elections WHERE end_time IS NULL) THEN
        RAISE EXCEPTION 'An open election already exists.';
    END IF;

    -- Start a new election
    INSERT INTO elections (start_time, restaurant_ids) VALUES (current_timestamp, ids);
END;
$$ LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION vote(v_id INT, r_id INT) RETURNS VOID AS $$
DECLARE
    e_id INT;
BEGIN
    -- Get the most recent open election
    SELECT id INTO e_id FROM elections WHERE end_time IS NULL ORDER BY start_time DESC LIMIT 1;

    -- Check if a valid open election is available
    IF e_id IS NOT NULL THEN
        -- Check if the user has already voted in the current election
        IF EXISTS (SELECT 1 FROM votes WHERE election_id = e_id AND voter_id = v_id) THEN
            -- Update the vote
            UPDATE votes
            SET restaurant_id = r_id
            WHERE election_id = e_id AND voter_id = v_id;
        ELSE
            -- Insert the vote
            INSERT INTO votes (election_id, voter_id, restaurant_id) VALUES (e_id, v_id, r_id);
        END IF;
    ELSE
        RAISE EXCEPTION 'No open election available for voting.';
    END IF;
END;
$$ LANGUAGE PLPGSQL;


------------------------------------------
--           VIEWS
------------------------------------------
-- CREATE VIEW restaurant_quality AS
--     SELECT re.res_id, re.res_name, re.res_loc, count(rv.*) review_count,
--         avg(rv.food_rating) avg_food, avg(rv.service_rating) avg_service, avg(rv.price_rating) avg_price, avg(rv.price_paid) avg_paid
--     FROM restaurants re
--     LEFT JOIN reviews rv ON re.res_id = rv.res_id
--     GROUP BY re.res_id
-- ;