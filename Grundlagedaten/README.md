Um die Notebooks erfolgreich zu nutzen, werden zusätzliche pythenpackages benötigt.
Der lokalen Jupyterinstallation sind diesen mittels pip hinzuzufügen.
Die benötigten packages sind in der requirements.txt Datei aufgelistet.

Alternativ kann mit dem beigefügten Dockerfile ein Dockercontainer erstellt werden.
In diesem Container sind sämtliche benötigten Packages enthalten.
Um den Container und Jupyter laufen zu lassen, ist wie folgt vorzugehen:
1. In der Eingabeaufforderung an den Ort des Dockerfiles navigieren.
2. Docker Image erstellen. `docker build -t cassda/jupyterdataunderstanding .`
3. Docker Container laufen lassen (Linux): `docker run --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work cassda/jupyterdataunderstanding`
4. Wurde der Container erfolgreich gestartet, erscheint in der Eingabeauffoderung eine  URL. Diese ist in einem modernen Browser einzufügen.
