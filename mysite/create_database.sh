
psql -c "CREATE DATABASE mod;"
psql -c "CREATE USER modadmin WITH PASSWORD '$Django10';" #Password breaks #TODO
psql -c "ALTER ROLE modadmin SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE modadmin SET default_transaction_isolation TO 'read committed';"
psql -c "ALTER ROLE modadmin SET timezone TO 'UTC';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE mod TO modadmin;"
