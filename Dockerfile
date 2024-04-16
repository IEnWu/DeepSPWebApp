FROM continuumio/miniconda3

# Install gcc and other build tools
RUN apt-get update && \
    apt-get install -y gcc build-essential

WORKDIR /app

RUN conda create -n myenv python=3.11.5
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

RUN conda install -c conda-forge keras==2.12.0
RUN conda install -c conda-forge tensorflow==2.12.0
RUN conda install -c conda-forge biopython -y
RUN conda install -c bioconda hmmer -y 
RUN conda install bioconda::anarci 

COPY . /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["gunicorn", "app:app"]

CMD ["gunicorn", "app:app"]
