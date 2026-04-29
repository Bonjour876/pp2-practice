-- Advanced pattern matching search across multiple tables
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(c_name VARCHAR, c_email VARCHAR, c_birthday DATE, g_name VARCHAR, all_phones TEXT) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email, c.birthday, g.name, 
           string_agg(p.phone || ' (' || p.type || ')', ', ')
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END; $$;

-- Procedure to handle contact migration between groups
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_g_id INT;
BEGIN
    -- Ensure the group exists (Idempotent insertion)
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_g_id FROM groups WHERE name = p_group_name;
    
    -- Assign contact to the group
    INSERT INTO contacts (name, group_id) 
    VALUES (p_contact_name, v_g_id)
    ON CONFLICT (name) DO UPDATE SET group_id = v_g_id;
END; $$;

-- Procedure to append a new phone number to an existing record
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    END IF;
END; $$;