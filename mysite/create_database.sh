
psql -c "CREATE DATABASE printrender;"
psql -c "CREATE USER printrenderadmin WITH PASSWORD '$Django10';" #Password breaks #TODO
psql -c "ALTER ROLE printrenderadmin SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE printrenderadmin SET default_transaction_isolation TO 'read committed';"
psql -c "ALTER ROLE printrenderadmin SET timezone TO 'UTC';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE printrender TO printrenderadmin;"
