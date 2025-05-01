import sqlite3

"""
AI GENERATED SCRIPT TO POPULATE THE DATABASE FOR ME
"""

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dish_id INTEGER NOT NULL,
        FOREIGN KEY (dish_id) REFERENCES dishes(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        ingredient TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit TEXT,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        step_order INTEGER NOT NULL,
        instruction TEXT NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    );
    ''')

    conn.commit()


def insert_sample_data(conn):
    cursor = conn.cursor()

    # Insert dishes
    cursor.executemany('''
    INSERT INTO dishes (name, description) VALUES (?, ?)
    ''', [
        ('Herb Crusted Tenderloin', 'Tenderloin with mashed potatoes, asparagus, red wine reduction'),
        ('Grilled Cheese & Soup', 'Grilled cheese sandwich with tomato bisque')
    ])

    # Insert recipes (we need dish_id, which we assume as 1 and 2 here)
    cursor.executemany('''
    INSERT INTO recipes (name, dish_id) VALUES (?, ?)
    ''', [
        ('Tenderloin Main', 1),
        ('Sides', 1),
        ('Grilled Cheese', 2),
        ('Tomato Bisque', 2)
    ])

    # Insert ingredients with quantity + unit
    cursor.executemany('''
    INSERT INTO ingredients (recipe_id, ingredient, quantity, unit) VALUES (?, ?, ?, ?)
    ''', [
        # Tenderloin Main (recipe_id 1)
        (1, 'beef tenderloin', 500, 'g'),
        (1, 'herbs', 2, 'tbsp'),
        (1, 'breadcrumbs', 0.5, 'cup'),
        # Sides (recipe_id 2)
        (2, 'mashed potatoes', 2, 'cups'),
        (2, 'asparagus', 200, 'g'),
        (2, 'red wine reduction', 0.25, 'cup'),
        # Grilled Cheese (recipe_id 3)
        (3, 'bread', 2, 'slices'),
        (3, 'cheddar cheese', 2, 'slices'),
        # Tomato Bisque (recipe_id 4)
        (4, 'tomato soup', 1, 'bowl'),
        (4, 'basil', 1, 'tbsp')
    ])

    # Insert steps with step_order
    cursor.executemany('''
    INSERT INTO steps (recipe_id, step_order, instruction) VALUES (?, ?, ?)
    ''', [
        (1, 1, 'Preheat oven to 400°F'),
        (1, 2, 'Coat tenderloin with herbs and breadcrumbs'),
        (1, 3, 'Roast for 25-30 minutes'),

        (2, 1, 'Boil potatoes and mash with butter'),
        (2, 2, 'Blanch asparagus in boiling water'),
        (2, 3, 'Reduce red wine into a sauce'),

        (3, 1, 'Butter bread slices'),
        (3, 2, 'Place cheese between slices'),
        (3, 3, 'Grill on pan until golden brown'),

        (4, 1, 'Simmer tomatoes with cream'),
        (4, 2, 'Blend until smooth'),
        (4, 3, 'Garnish with basil')
    ])

    conn.commit()


if __name__ == '__main__':
    db_path = 'recipes.db'
    conn = sqlite3.connect(db_path)

    create_tables(conn)
    insert_sample_data(conn)

    conn.close()

    print(f"Database '{db_path}' created and populated with sample data!")