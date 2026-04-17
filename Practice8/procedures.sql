CREATE OR REPLACE PROCEDURE upsert_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES(p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many(
    p_names TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    IF array_length(p_names,1) <> array_length(p_phones,1) THEN
        RAISE EXCEPTION 'Arrays must be same length';
    END IF;

    FOR i IN 1..array_length(p_names,1) LOOP
        
        IF p_phones[i] !~ '^[0-9]+$' THEN
            RAISE EXCEPTION 'Invalid phone number: %', p_phones[i];
        END IF;

        IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_names[i]) THEN
            UPDATE phonebook 
            SET phone = p_phones[i] 
            WHERE name = p_names[i];
        ELSE
            INSERT INTO phonebook(name, phone) 
            VALUES (p_names[i], p_phones[i]);
        END IF;

    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = value OR phone = value;
END;
$$;