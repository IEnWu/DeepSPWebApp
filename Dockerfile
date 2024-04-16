FROM continuumio/miniconda3


WORKDIR /app


RUN conda install -c conda-forge biopython -y
RUN conda install -c bioconda hmmer -y 
RUN conda install bioconda::anarci 

COPY . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app"]