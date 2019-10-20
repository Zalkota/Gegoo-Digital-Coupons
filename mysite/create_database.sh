
psql -c "CREATE DATABASE estore;"
psql -c "CREATE USER estoreadmin WITH PASSWORD '$Django10';" #Password breaks #TODO
psql -c "ALTER ROLE estoreadmin SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE estoreadmin SET default_transaction_isolation TO 'read committed';"
psql -c "ALTER ROLE estoreadmin SET timezone TO 'UTC';"
psql -c "l"
