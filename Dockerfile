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


# Run app.py when the container launches
CMD ["gunicorn", "app:app"]
