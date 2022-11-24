FROM jupyter/minimal-notebook:lab-3.4.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python -m spacy download fr_core_news_md
RUN python -m spacy download de_core_news_md