-- Creating table mess_menus
CREATE TABLE mess_menus (
    id SERIAL PRIMARY KEY,
    month SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    breakfast JSON,
    lunch JSON,
    snacks JSON,
    dinner JSON
);

-- Validating JSON schemas
CREATE FUNCTION validate_json_schemas_mess_menus()
RETURN TRIGGER AS $$
BEGIN
    IF NEW.breakfast IS NOT NULL THEN
        IF NOT JSONB_TYPEOF(NEW.breakfast) = 'array' THEN
            RAISE EXCEPTION 'breakfast must be an array';
        END IF;

        FOR menu_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.breakfast)
        LOOP
            IF (menu_item_id)::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'item in the breakfast array must be a number';
            END IF;
        END LOOP;
    END IF;

    IF NEW.lunch IS NOT NULL THEN
        IF NOT JSONB_TYPEOF(NEW.lunch) = 'array' THEN
            RAISE EXCEPTION 'lunch must be an array';
        END IF;

        FOR menu_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.lunch)
        LOOP
            IF (menu_item_id)::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'item in the lunch array must be a number';
            END IF;
        END LOOP;
    END IF;

    IF NEW.snacks IS NOT NULL THEN
        IF NOT JSONB_TYPEOF(NEW.snacks) = 'array' THEN
            RAISE EXCEPTION 'snacks must be an array';
        END IF;

        FOR menu_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.snacks)
        LOOP
            IF NOT (menu_item_id)::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'item in the snacks array must be a number';
            END IF;
        END LOOP;
    END IF;

    IF NEW.dinner IS NOT NULL THEN
        IF NOT JSONB_TYPEOF(NEW.dinner) = 'array' THEN
            RAISE EXCEPTION 'dinner must be an array';
        END IF;

        FOR menu_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.dinner)
        LOOP
            IF (menu_item_id)::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'item in the dinner array must be a number';
            END IF;
        END LOOP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creating trigger to validate JSON schemas
CREATE TRIGGER validate_json_mess_menus
BEFORE INSERT OR UPDATE ON mess_menus
FOR EACH ROW EXECUTE FUNCTION validate_json_schemas_mess_menus();