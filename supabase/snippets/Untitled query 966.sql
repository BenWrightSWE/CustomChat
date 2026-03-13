SELECT proname, pg_get_function_arguments(oid)
FROM pg_proc
WHERE proname = 'update_secret'
AND pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'vault');