-- Creating table food_outlets
CREATE TABLE food_outlets (
    id serial PRIMARY KEY,
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
    menu_item JSON;
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

        FOR menu_item IN SELECT * FROM JSON_ARRAY_ELEMENTS(NEW.menu)
        LOOP
            IF NOT JSON_TYPEOF(menu_item) = 'object' THEN
                RAISE EXCEPTION 'item in the menu array must be an object';
            END IF;

            IF (menu_item ->> 'name' IS NULL) OR ((menu_item ->> 'name')::TEXT IS NULL) OR TRIM(menu_item ->> 'name') = '' THEN
                RAISE EXCEPTION 'item in the menu array must have a name';
            END IF;

            IF (menu_item ->> 'price' IS NULL) OR (menu_item ->> 'price')::NUMERIC IS NULL THEN
                RAISE EXCEPTION 'item in the menu array must have a price';
            END IF;

            IF (menu_item ->> 'description' IS NOT NULL) AND ((menu_item ->> 'description')::TEXT IS NULL) THEN
                RAISE EXCEPTION 'description of item in the menu array must be a string';
            END IF;

            IF (menu_item ->> 'rating' IS NOT NULL) THEN
                IF NOT JSON_TYPEOF(menu_item ->> 'rating') = 'object' THEN
                    RAISE EXCEPTION 'rating of item in the menu array must be an object';
                END IF;

                IF (menu_item ->> 'rating' ->> 'total')::NUMERIC IS NULL THEN
                    RAISE EXCEPTION 'total rating of item in the menu array must be a number';
                END IF;

                IF (menu_item ->> 'rating' ->> 'count')::NUMERIC IS NULL THEN
                    RAISE EXCEPTION 'count of ratings of item in the menu array must be a number';
                END IF;
            END IF;

            IF (menu_item ->> 'size' IS NOT NULL) AND ((menu_item ->> 'size')::TEXT IS NULL) THEN
                RAISE EXCEPTION 'size of item in the menu array must be a string';
            END IF;

            IF (menu_item ->> 'cal' IS NOT NULL) AND ((menu_item ->> 'cal')::NUMERIC IS NULL) THEN
                RAISE EXCEPTION 'calories of item in the menu array must be a number';
            END IF;

            IF (menu_item ->> 'image' IS NOT NULL) AND ((menu_item ->> 'image')::TEXT IS NULL) THEN
                RAISE EXCEPTION 'url of image of item in the menu array must be a string';
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