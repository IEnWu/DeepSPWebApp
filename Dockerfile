FROM continuumio/miniconda3

WORKDIR /app

# Install necessary packages using Conda
RUN conda install -c conda-forge biopython -y \
    && conda install -c bioconda hmmer -y \
    && conda install -c bioconda anarci -y \
    && conda install --file requirements.txt -y

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the Flask application using Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]

