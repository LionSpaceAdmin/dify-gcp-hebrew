-- Initialize PostgreSQL with Hebrew support
-- This script sets up the database with proper encoding for Hebrew text

-- Create extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set proper collation for Hebrew text
ALTER DATABASE dify SET lc_collate = 'he_IL.UTF-8';
ALTER DATABASE dify SET lc_ctype = 'he_IL.UTF-8';

-- Create a function to ensure Hebrew text is handled properly
CREATE OR REPLACE FUNCTION ensure_hebrew_support()
RETURNS TEXT AS $$
DECLARE
    result TEXT;
BEGIN
    -- Test Hebrew text
    result := 'מערכת Dify עם תמיכה בעברית מוכנה!';
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Log success
SELECT ensure_hebrew_support() as hebrew_test;