CREATE TABLE food_outlet_menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    price NUMERIC NOT NULL,
    description VARCHAR,
    rating JSON,
    size VARCHAR,
    cal NUMERIC,
    image VARCHAR,
    food_outlet_id INT NOT NULL,
    FOREIGN KEY (food_outlet_id) REFERENCES food_outlets(id)
);

CREATE FUNCTION validate_json_schemas_food_outlet_menu_items()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.rating IS NOT NULL THEN
        IF (NEW.rating ->> 'total')::NUMERIC IS NULL THEN
            RAISE EXCEPTION 'total rating must be a number';
        END IF;

        IF (NEW.rating ->> 'count')::NUMERIC IS NULL THEN
            RAISE EXCEPTION 'count of ratings must be a number';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_json_food_outlet_menu_items
BEFORE INSERT OR UPDATE ON food_outlet_menu_items
FOR EACH ROW EXECUTE FUNCTION validate_json_schemas_food_outlet_menu_items();