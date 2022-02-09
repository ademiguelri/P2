This project is a simulation of a thermostat using python transitions and OPCUA packages and TimescaleDB and Grafana Dockers.

Thermostat.py creates a instance of the object stateMachine. This instance creates a state machine that will simulate a working thermostat thats oscilates between 16 and 23 grades.

The information that generates will be send by server.py that is connected with client.py using OPC UA protocols.

Once the client had recived the information, it will store in the database that is on the TimescaleDB docker. This information will be visible in Grafana that is hosted on Docker.