SELECT * FROM Place

DO $$
DECLARE
    place_id   place.place_id%TYPE;
    place_country place.place_country%TYPE;

BEGIN
    place_id := 0;
    place_country := 'country';
    FOR counter IN 1..5
        LOOP
            INSERT INTO place(place_id, place_country, place_state)
            VALUES (place_id + counter, place_country || ' ' || counter, NULL);
        END LOOP;
END;
$$
