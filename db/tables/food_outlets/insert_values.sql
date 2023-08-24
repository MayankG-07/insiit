-- Inserting values into the food_outlets table
INSERT INTO food_outlets
    (name, landmark, open_time, close_time, menu)
VALUES
    ('Atul Bakery', 'at Chimair', '13:00:00', '02:00:00', null),
    ('Shri Sainath Canteen (A)', 'at Panchayat Circle', '19:00:00', '03:00:00', jsonb_build_array(
        jsonb_build_object(
            'name', 'Aloo Paratha (with Pickle + Ketchup)',
            'price', 40,
            'description', null,
            'rating', null,
            'size', '215 gm',
            'cal', null,
            'image', null
        ),
        jsonb_build_object(
            'name', 'Paneer Paratha',
            'price', 50,
            'description', null,
            'rating', null,
            'size', '210 gm',
            'cal', null,
            'image', null
        )
    ));