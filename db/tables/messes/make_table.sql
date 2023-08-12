-- Creating table messes
CREATE TABLE messes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location JSON,
    landmark VARCHAR,
    timings JSON,
    rating JSON
    mess_menu_id INTEGER REFERENCES mess_menus(id),
    image VARCHAR
);

-- Validating JSON schemas
CREATE FUNCTION validate_json_schemas_messes()
RETURN TRIGGER AS $$
BEGIN
    IF NEW.timings IS NOT NULL THEN
        IF NOT JSONB_TYPEOF(NEW.timings) = 'object' THEN
            RAISE EXCEPTION 'timings must be an object'
        END IF;

        IF NOT NEW.timings ? 'breakfast' THEN
            RAISE EXCEPTION 'timings object must have breakfast key'
        END IF;

        IF NOT NEW.timings ? 'breakfast' ? 'start' THEN
            RAISE EXCEPTION 'timings object must have breakfast.start key'
        END IF;

        IF NOT NEW.timings ? 'breakfast' ? 'end' THEN
            RAISE EXCEPTION 'timings object must have breakfast.end key'
        END IF;

        IF NOT NEW.timings ? 'lunch' THEN
            RAISE EXCEPTION 'timings object must have lunch key'
        END IF;

        IF NOT NEW.timings ? 'lunch' ? 'start' THEN
            RAISE EXCEPTION 'timings object must have lunch.start key'
        END IF;

        IF NOT NEW.timings ? 'lunch' ? 'end' THEN
            RAISE EXCEPTION 'timings object must have lunch.end key'
        END IF;

        IF NOT NEW.timings ? 'snacks' THEN
            RAISE EXCEPTION 'timings object must have snacks key'
        END IF;

        IF NOT NEW.timings ? 'snacks' ? 'start' THEN
            RAISE EXCEPTION 'timings object must have snacks.start key'
        END IF;

        IF NOT NEW.timings ? 'snacks' ? 'end' THEN
            RAISE EXCEPTION 'timings object must have snacks.end key'
        END IF;

        IF NOT NEW.timings ? 'dinner' THEN
            RAISE EXCEPTION 'timings object must have dinner key'
        END IF;

        IF NOT NEW.timings ? 'dinner' ? 'start' THEN
            RAISE EXCEPTION 'timings object must have dinner.start key'
        END IF;

        IF NOT NEW.timings ? 'dinner' ? 'end' THEN
            RAISE EXCEPTION 'timings object must have dinner.end key'
        END IF;
    END IF;

    IF NEW.rating IS NOT NULL THEN
        IF NOT JSONB_TYPEOF(NEW.rating) = 'object' THEN
            RAISE EXCEPTION 'rating must be an object'
        END IF;

        IF NOT NEW.rating ? 'total' THEN
            RAISE EXCEPTION 'rating object must have total key'
        END IF;

        IF NOT NEW.rating ? 'total' ? 'count' THEN
            RAISE EXCEPTION 'rating.total object must have count key'
        END IF;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Creating trigger to validate JSON schema
CREATE TRIGGER validate_json_messes
BEFORE INSERT OR UPDATE ON messes
FOR EACH ROW EXECUTE FUNCTION validate_json_schemas_messes();
