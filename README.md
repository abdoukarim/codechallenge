docker-compose build codechallenge
The command docker-compose down --volumes removes the containers, default network, and the database.
The command docker-compose down removes the containers and default network, but preserves your database.

To build the project run docker-compose up -d
The app is not immediately available on port 8888 because the containers are still being initialized and may take a couple of minutes before the first load.
