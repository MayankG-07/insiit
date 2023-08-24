-- Creating table messes
CREATE TABLE messes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location JSON,
    landmark VARCHAR,
    timings JSON,
    rating JSON,
    mess_menu_id INTEGER REFERENCES mess_menus(id),
    image VARCHAR
);

-- Validating JSON schemas
CREATE FUNCTION validate_json_schemas_messes()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.timings IS NOT NULL THEN
        IF NOT JSONB_TYPEOF(NEW.timings AS JSONB) = 'object' THEN
            RAISE EXCEPTION 'timings must be an object';
        END IF;

        IF NOT JSONB_TYPEOF(NEW.timings ->> 'breakfast' AS JSONB) = 'object' THEN
            RAISE EXCEPTION 'breakfast must be an object';
        END IF;

        IF (NEW.timings ->> 'breakfast' ->> 'start')::TIME IS NULL THEN
            RAISE EXCEPTION 'breakfast.start must be a time';
        END IF;

        IF (NEW.timings ->> 'breakfast' ->> 'end')::TIME THEN
            RAISE EXCEPTION 'breakfast.end must be a time';
        END IF;

        IF NOT JSONB_TYPEOF(NEW.timings ->> 'lunch' AS JSONB) = 'object' THEN
            RAISE EXCEPTION 'lunch must be an object';
        END IF;

        IF (NEW.timings ->> 'lunch' ->> 'start')::TIME IS NULL THEN
            RAISE EXCEPTION 'lunch.start must be a time';
        END IF;

        IF (NEW.timings ->> 'lunch' ->> 'end')::TIME IS NULL THEN
            RAISE EXCEPTION 'lunch.end must be a time';
        END IF;

        IF NOT JSONB_TYPEOF(NEW.timings ->> 'snacks' AS JSONB) = 'object' THEN
            RAISE EXCEPTION 'snacks must be an object';
        END IF;

        IF (NEW.timings ->> 'snacks' ->> 'start')::TIME IS NULL THEN
            RAISE EXCEPTION 'snacks.start must be a time';
        END IF;

        IF (NEW.timings ->> 'snacks' ->> 'end')::TIME IS NULL THEN
            RAISE EXCEPTION 'snacks.end must be a time';
        END IF;

        IF NOT JSONB_TYPEOF(NEW.timings ->> 'dinner' AS JSONB) = 'object' THEN
            RAISE EXCEPTION 'dinner must be an object';
        END IF;

        IF (NEW.timings ->> 'dinner' ->> 'start')::TIME IS NULL THEN
            RAISE EXCEPTION 'dinner.start must be a time';
        END IF;

        IF (NEW.timings ->> 'dinner' ->> 'end')::TIME IS NULL THEn
            RAISE EXCEPTION 'dinner.end must be a time';
        END IF;
    END IF;

    IF NEW.rating IS NOT NULL THEN
        IF NOT JSONB_TYPEOF(NEW.rating AS JSONB) = 'object' THEN
            RAISE EXCEPTION 'rating must be an object';
        END IF;

        IF (NEW.rating ->> 'total')::NUMERIC IS NULL THEN
            RAISE EXCEPTION 'rating.total must be a float between 0 and 5';
        END IF;

        IF (NEW.rating ->> 'count')::NUMERIC IS NULL THEN
            RAISE EXCEPTION 'rating.count must be an integer';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creating trigger to validate JSON schema
CREATE TRIGGER validate_json_messes
BEFORE INSERT OR UPDATE ON messes
FOR EACH ROW EXECUTE FUNCTION validate_json_schemas_messes();
