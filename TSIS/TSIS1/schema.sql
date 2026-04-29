-- Explicitly drop the function to avoid return type conflicts during re-initialization
DROP FUNCTION IF EXISTS search_contacts(text);

-- Drop existing tables to ensure a clean state (Cascade order)
DROP TABLE IF EXISTS phones;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS groups;

-- Create 'groups' table for contact categorization
CREATE TABLE groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Pre-populate default categories
INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other');

-- Create 'contacts' table with extended attributes
CREATE TABLE contacts (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(100) UNIQUE NOT NULL,
    email    VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL
);

-- Create 'phones' table to support multiple numbers (One-to-Many)
CREATE TABLE phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);