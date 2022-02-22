FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml
COPY . .
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "restopcua", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
WORKDIR /app/app
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "restopcua", "python", "app.py"]