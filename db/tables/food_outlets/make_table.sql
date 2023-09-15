-- Creating table food_outlets
CREATE TABLE food_outlets (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location JSON,
    landmark VARCHAR,
    open_time TIME,
    close_time TIME,
    rating JSON,   
    menu JSON,
    image VARCHAR
);

-- Validating JSON schemas
CREATE FUNCTION validate_json_schemas_food_outlets()
RETURNS TRIGGER AS $$
DECLARE
    menu_item_id NUMERIC;
BEGIN
    IF NEW.location IS NOT NULL THEN
        IF NOT JSON_TYPEOF(NEW.location) = 'object' THEN
            RAISE EXCEPTION 'location must be an object';
        END IF;

        IF (NEW.location ->> 'latitude' IS NULL) OR (NEW.location ->> 'latitude')::TEXT IS NULL THEN
            RAISE EXCEPTION 'latitude must be a number in a string';
        END IF;

        IF (NEW.location ->> 'longitude' IS NULL) OR (NEW.location ->> 'longitude')::TEXT IS NULL THEN
            RAISE EXCEPTION 'longitude must be a number in a string';
        END IF;
    END IF;

    IF NEW.rating IS NOT NULL THEN
        IF NOT JSON_TYPEOF(NEW.rating) = 'object' THEN
            RAISE EXCEPTION 'rating must be an object';
        END IF;

        IF (NEW.rating ->> 'total' IS NULL) OR (NEW.rating ->> 'total')::NUMERIC IS NULL THEN
            RAISE EXCEPTION 'total rating must be a number';
        END IF;

        IF (NEW.rating ->> 'count' IS NULL) OR (NEW.rating ->> 'count')::NUMERIC IS NULL THEN
            RAISE EXCEPTION 'count of ratings must be a number';
        END IF;
    END IF;

    IF NEW.menu IS NOT NULL THEN
        IF NOT JSON_TYPEOF(NEW.menu) = 'array' THEN
            RAISE EXCEPTION 'menu must be an array';
        END IF;

        FOR menu_item_id IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.menu)
        LOOP
            IF menu_item_id::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'menu item id must be an integer';
            END IF;
        END LOOP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creating trigger to validate JSON schemas
CREATE TRIGGER validate_json_food_outlets
BEFORE INSERT OR UPDATE ON food_outlets
FOR EACH ROW EXECUTE FUNCTION validate_json_schemas_food_outlets();