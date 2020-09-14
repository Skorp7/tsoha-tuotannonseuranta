CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE, 
    status INTEGER, 
    password TEXT;
    visible INTEGER
);

CREATE TABLE clinics (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
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
    clinic_id INTEGER REFERENCES clinics, 
    visible INTEGER
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY, 
    order_type_id INTEGER REFERENCES order_types,
    customer_id INTEGER REFERENCES customers,
    time TIMESTAMP
);

CREATE TABLE events (
    order_id INTEGER REFERENCES orders,
    user_id INTEGER REFERENCES users,
    description TEXT,
    time TIMESTAMP,
    is_pending INTEGER
);
   


