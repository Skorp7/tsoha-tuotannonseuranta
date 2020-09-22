CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE, 
    status INTEGER, 
    password TEXT,
    visible INTEGER
);

CREATE TABLE clinics (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    adress TEXT,
    postal_code TEXT,
    city TEXT
);

CREATE TABLE order_types (
    id SERIAL PRIMARY KEY,
    product_type TEXT,
    main_materials TEXT
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    visible INTEGER
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY, 
    order_type_id INTEGER REFERENCES order_types,
    customer_id INTEGER REFERENCES customers,
    clinic_id INTEGER REFERENCES clinics,
    delivery_date TIMESTAMP,
    in_progress INTEGER,
    time TIMESTAMP
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders,
    user_id INTEGER REFERENCES users,
    description TEXT,
    time TIMESTAMP,
    is_pending INTEGER
);
   
CREATE TABLE citys_fi (
    name TEXT
);

\copy citys_fi FROM 'kunnat.txt';

