FROM continuumio/miniconda3

# Install gcc and other build tools
RUN apt-get update && \
    apt-get install -y gcc build-essential

WORKDIR /app

# Install Python packages using pip first
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN conda install -c conda-forge biopython -y
RUN conda install -c bioconda hmmer -y 
RUN conda install bioconda::anarci 


COPY . /app




CMD ["gunicorn", "app:app"]
