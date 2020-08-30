FROM mariadb:10.5.5-focal

# WARNING: set these to something unique on the production server, 
# the ones set in the repo are for demo purposes only
COPY ./root_password /run/secrets/mysql-root-password
COPY ./user_password /run/secrets/mysql-user-password
COPY ./user_name /run/secrets/mysql-user-name
COPY ./50-server.cnf /etc/mysql/mariadb.conf.d/50-server.cnf