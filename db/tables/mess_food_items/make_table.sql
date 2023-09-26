-- Creating table mess_food_items
CREATE TABLE mess_food_items (
    id serial PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    rating JSON,
    cal INTEGER,
    image VARCHAR
);

-- Validating JSON schemas
CREATE FUNCTION validate_json_schemas_mess_food_items()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.rating IS NOT NULL THEN
        IF NOT JSON_TYPEOF(NEW.rating AS JSON) = 'object' THEN
            RAISE EXCEPTION 'rating must be an object';
        END IF;

        IF (NEW.rating ->> 'total' IS NULL) OR (NEW.rating ->> 'total')::NUMERIC IS NULL THEN
            RAISE EXCEPTION 'total rating must be a number';
        END IF;

        IF (NEW.rating ->> 'count' IS NULL) OR (NEW.rating ->> 'count')::NUMERIC IS NULL THEN
            RAISE EXCEPTION 'count of ratings must be a number';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creating trigger to validate json schema
CREATE TRIGGER validate_json_mess_food_items
BEFORE INSERT OR UPDATE ON mess_food_items
FOR EACH ROW EXECUTE FUNCTION validate_json_schemas_mess_food_items();