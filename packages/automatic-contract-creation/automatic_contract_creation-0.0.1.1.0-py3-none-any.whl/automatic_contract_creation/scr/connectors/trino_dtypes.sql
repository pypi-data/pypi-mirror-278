SELECT
    column_name,
    is_nullable,
    data_type
FROM
    INFORMATION_SCHEMA.COLUMNS
WHERE
    TABLE_SCHEMA = '{schema}'
    AND TABLE_NAME = '{tablename}'