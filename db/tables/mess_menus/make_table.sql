-- Creating table mess_menus
CREATE TABLE mess_menus (
    id SERIAL PRIMARY KEY,
    month INT NOT NULL,
    year INT NOT NULL,
    breakfast JSON,
    lunch JSON,
    snacks JSON,
    dinner JSON
);

-- Validating JSON schemas
CREATE FUNCTION validate_json_schemas_mess_menus()
RETURNS TRIGGER AS $$
DECLARE
    breakfast_menu_item JSON;
    breakfast_food_item_id NUMERIC;
    lunch_menu_item JSON;
    lunch_food_item_id NUMERIC;
    snacks_menu_item JSON;
    snacks_food_item_id NUMERIC;
    dinner_menu_item JSON;
    dinner_food_item_id NUMERIC;
BEGIN
    IF NEW.breakfast IS NOT NULL THEN
        IF NOT JSON_TYPEOF(NEW.breakfast) = 'array' THEN
            RAISE EXCEPTION 'breakfast must be an array';
        END IF;

        FOR breakfast_menu_item IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.breakfast)
        LOOP
            IF NOT JSON_TYPEOF(breakfast_menu_item) = 'object' THEN
                RAISE EXCEPTION 'item in the breakfast array must be an object';
            END IF;

            IF (breakfast_menu_item ->> 'day')::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'day property of object in the breakfast array must be a number';
            END IF;

            IF NOT JSON_TYPEOF(breakfast_menu_item ->> 'food') = 'array' THEN
                RAISE EXCEPTION 'food property of object in the breakfast array must be an array';
            END IF;

            FOR breakfast_food_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(breakfast_menu_item ->> 'food')
            LOOP
                IF (breakfast_food_item_id)::NUMERIC IS NULL THEN
                    RAISE EXCEPTION 'item in the food array must be a number';
                END IF;
            END LOOP;
        END LOOP;
    END IF;

    IF NEW.lunch IS NOT NULL THEN
        IF NOT JSON_TYPEOF(NEW.lunch) = 'array' THEN
            RAISE EXCEPTION 'lunch must be an array';
        END IF;

        FOR lunch_menu_time IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.lunch)
        LOOP
            IF NOT JSON_TYPEOF(lunch_menu_time) = 'object' THEN
                RAISE EXCEPTION 'item in the lunch array must be an object';
            END IF;

            IF (lunch_menu_time ->> 'day')::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'day property of object in the lunch array must be a number';
            END IF;

            IF NOT JSON_TYPEOF(lunch_menu_time ->> 'food') = 'array' THEN
                RAISE EXCEPTION 'food property of object in the lunch array must be an array';
            END IF;

            FOR lunch_food_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(lunch_menu_time ->> 'food')
            LOOP
                IF (lunch_food_item_id)::NUMERIC IS NULL THEN
                    RAISE EXCEPTION 'item in the food array must be a number';
                END IF;
            END LOOP;
        END LOOP;
    END IF;

    IF NEW.snacks IS NOT NULL THEN
        IF NOT JSON_TYPEOF(NEW.snacks) = 'array' THEN
            RAISE EXCEPTION 'snacks must be an array';
        END IF;

        FOR snacks_menu_item IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.snacks)
        LOOP
            IF NOT JSON_TYPEOF(snacks_menu_item) = 'object' THEN
                RAISE EXCEPTION 'item in the snacks array must be an object';
            END IF;

            IF (snacks_menu_item ->> 'day')::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'day property of object in the snacks array must be a number';
            END IF;

            IF NOT JSON_TYPEOF(snacks_menu_item ->> 'food') = 'array' THEN
                RAISE EXCEPTION 'food property of object in the snacks array must be an array';
            END IF;

            FOR snacks_food_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(snacks_menu_item ->> 'food')
            LOOP
                IF (snacks_food_item_id)::NUMERIC IS NULL THEN
                    RAISE EXCEPTION 'item in the food array must be a number';
                END IF;
            END LOOP;
        END LOOP;
    END IF;

    IF NEW.dinner IS NOT NULL THEN
        IF NOT JSON_TYPEOF(NEW.dinner) = 'array' THEN
            RAISE EXCEPTION 'dinner must be an array';
        END IF;

        FOR dinner_menu_item IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.dinner)
        LOOP
            IF NOT JSON_TYPEOF(dinner_menu_item) = 'object' THEN
                RAISE EXCEPTION 'item in the dinner array must be an object';
            END IF;

            IF (dinner_menu_item ->> 'day')::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'day property of object in the dinner array must be a number';
            END IF;

            IF NOT JSON_TYPEOF(dinner_menu_item ->> 'food') = 'array' THEN
                RAISE EXCEPTION 'food property of object in the dinner array must be an array';
            END IF;

            FOR dinner_food_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(dinner_menu_item ->> 'food')
            LOOP
                IF (dinner_food_item_id)::NUMERIC IS NULL THEN
                    RAISE EXCEPTION 'item in the food array must be a number';
                END IF;
            END LOOP;
        END LOOP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creating trigger to validate JSON schemas
CREATE TRIGGER validate_json_mess_menus
BEFORE INSERT OR UPDATE ON mess_menus
FOR EACH ROW EXECUTE FUNCTION validate_json_schemas_mess_menus();