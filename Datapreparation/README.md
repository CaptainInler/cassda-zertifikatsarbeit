In diesem Ordner befinden sich Jupyter Notbooks für die Datenpreparation.  
Um die Notebooks erfolgreich zu nutzen, werden gewisse Pythonpackages benötigt. Die benötigten Packages sind in der requirements.txt Datei aufgelistet.

Mit beigefügten Dockerfile kann ein Dockercontainer erstellt werden. In diesem Container sind sämtliche benötigten Packages enthalten die für die erfolgreiche Ausführung aller Befehle benötigt werden.
Um den Container und Jupyter laufen zu lassen, ist wie folgt vorzugehen:
1. In der Eingabeaufforderung an den Ort des Dockerfiles navigieren.
2. Docker Image erstellen. `docker build -t cassda/jupyterdatapreparation .`
3. Docker Container laufen lassen (Linux): `docker run --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work cassda/jupyterdatapreparation`
4. Wurde der Container erfolgreich gestartet, erscheint in der Eingabeauffoderung eine URL. Diese ist in einem modernen Browser einzufügen.
5. Die Notebooks sind im Ordner work enthalten.