# P2 project

This project makes server/client connection between n thermostats and a docker with timescaledb.

The connection is made via OPC UA protocol where the server part is sending all information of the thermostats and sending to the client that inserts that into a timescaledb docker.

Thermostats are simulated using a state machine, helped by python transitions package.

Once timescale is receiving data, these data is visualiced on Grafana.

Thermostat.py creates a instance of the object stateMachine. This instance creates a state machine and will simulate a working thermostat that will warm or cool based on the target temperature.


## Use guide

1. Start docker-compose
2. Run lab.py
3. Run app.py

## Usefull code

Open postgres terminal inside the docker:

    docker exec -it <dockerID> psql -U postgres

Insert data to DB with generate_series:

    insert into  auto(dateTime, info) values (generate_series('2020-01-01'::date, '2020-12-31'::date, INTERVAL '1 day'),generate_series(1,365)*(10 + 10 * random()));