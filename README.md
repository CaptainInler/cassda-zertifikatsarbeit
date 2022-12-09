In diesem Repo sind die Daten unserer Zertifikatsarbeit zum [CAS Spatial Data Analytics](https://www.fhnw.ch/de/weiterbildung/architektur-bau-geomatik/geomatik/cas-spatial-data-analytics) an der [Fachhochschule Nordwestschweiz](https://www.fhnw.ch) inklusive der abgegebenen [Zertifikatsarbeit.pdf](https://github.com/CaptainInler/cassda-zertifikatsarbeit/blob/main/Zertifikatsarbeit.pdf) abgelegt.

# Spatial Data Mining mit Python: Möglichkeiten und Tools
Etymologie von Strassennamen der Schweiz

<img src="https://user-images.githubusercontent.com/16583617/202919500-f56d75f2-60fd-4ca7-a516-18d769c4b733.png" width="500" />


## JupyterLab in Docker
Um die Notebooks in diesem Repo erfolgreich zu nutzen, werden gewisse Pythonpackages benötigt.
Der lokalen JupyterLabinstallation sind diesen mittels pip hinzuzufügen.
Die benötigten packages sind in der requirements.txt Datei aufgelistet.

Alternativ kann mit dem beigefügten Dockerfile ein Dockercontainer erstellt werden in welchem ein JupyterLab Instanz gestartet wird.
In diesem Container sind sämtliche benötigten Packages enthalten.
Um den Container und JupyterLab laufen zu lassen, ist wie folgt vorzugehen:
1. In der Eingabeaufforderung an den Ort des Dockerfiles navigieren.
2. Docker Image erstellen. `docker build -t cassda/streetnames .`
3. Docker Container laufen lassen (Linux): `docker run --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work cassda/streetnames`
4. Wurde der Container erfolgreich gestartet, erscheint in der Eingabeauffoderung eine URL. Diese ist in einem modernen Browser einzufügen.
5. Die Notebooks sind im Ordner work enthalten.
