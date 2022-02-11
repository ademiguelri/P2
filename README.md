# P2 project

This project is a simulation of a thermostat using python transitions and OPCUA packages and TimescaleDB and Grafana Dockers.

Thermostat.py creates a instance of the object stateMachine. This instance creates a state machine that will simulate a working thermostat thats oscilates between 16 and 23 grades.

The information that generates will be send by server.py that is connected with client.py using OPC UA protocols.

Once the client had recived the information, it will store in the database that is on the TimescaleDB docker. This information will be visible in Grafana that is hosted on Docker.

## Usefull code

Open postgres terminal inside the docker:

    docker exec -it <dockerID> psql -U postgres

Insert data to DB with generate_series:

    insert into  auto(dateTime, info) values (generate_series('2020-01-01'::date, '2020-12-31'::date, INTERVAL '1 day'),generate_series(1,365)*(10 + 10 * random()));