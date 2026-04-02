CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(contact_name VARCHAR, contact_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.name AS contact_name, p.phone AS contact_phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$;

CREATE OR REPLACE FUNCTION get_contacts_paginated(limit_count INT, offset_count INT)
RETURNS TABLE(contact_name VARCHAR, contact_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.name AS contact_name, p.phone AS contact_phone
    FROM phonebook p
    LIMIT limit_count
    OFFSET offset_count;
END;
$$;

