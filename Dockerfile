FROM continuumio/miniconda3


WORKDIR /app


RUN conda install -c conda-forge biopython -y
RUN conda install -c bioconda hmmer -y 
RUN conda install bioconda::anarci 


COPY . /app

RUN pip install -r requirements.txt 

EXPOSE 80

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]
