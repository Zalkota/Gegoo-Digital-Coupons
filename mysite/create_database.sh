
psql -c "CREATE DATABASE gegoo;"
psql -c "CREATE USER gegooadmin WITH PASSWORD '$Django10';" #Password breaks #TODO
psql -c "ALTER ROLE gegooadmin SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE gegooadmin SET default_transaction_isolation TO 'read committed';"
psql -c "ALTER ROLE gegooadmin SET timezone TO 'UTC';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE gegoo TO gegooadmin;"
