use admin;
db.grantRolesToUser('root', [{ role: 'root', db: 'django_db' }])