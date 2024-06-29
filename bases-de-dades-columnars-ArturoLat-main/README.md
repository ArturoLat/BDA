[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=14881505&assignment_repo_type=AssignmentRepo)
## Pràctica 6: Bases de dades columnars

Benvingut/da a la cinquena pràctica de l'assignatura de Bases de dades. Aquesta pràctica parteix de la plantilla de la pràctica anterior. Com sabeu tenim una API REST que ens permet crear, esborrar, modificar i consultar les dades d'una aplicació de sensors. En aquesta pràctica volem ampliar el cas d'ús de la nostra API per a fer servir una base de dades columnars,

## Com començar?

Per començar, necessitaràs clonar aquest repositori. Pots fer-ho amb el següent comandament:

```bash
git clone url-del-teu-assignment
```

Recorda que fem servir docker-compose per a executar l'entorn de desenvolupament i provar el que anem desenvolupant. Per a arrancar l'entorn de desenvolupament, pots fer servir el següent comandament:

```bash
docker-compose up -d
```

Recorda parar l'entorn de desenvolupament de la setmana passada abans de començar a treballar amb aquesta pràctica.

Si vols parar l'entorn de desenvolupament, pots fer servir el següent comandament:

```bash
docker-compose down
```

Cal que tinguis en compte que si fas servir aquest comandament, no esborraràs tota la informació que tinguis a la base de dades, ja que per defecte down només esborra els conteidors i la xarxa entre ells. Si vols esborrar tota la informació que tinguis a la base de dades, pots fer servir el següent comandament:

```bash
docker-compose down -v
```

**Important**: Quan executem `docker-compose up`, Docker construeix una imatge de Docker amb FastAPI amb una fotografia estàtica del codi que tenim al directori. Això vol dir que si modifiquem el codi, no es veurà reflexat a l'entorn de desenvolupament. Per això, cal que executem docker-compose up cada cop que modifiquem el codi. Si no ho fem, no veurem els canvis que haguem fet.


### Context

Sembla que la nostra API comença a ser robusta i els usuaris estàn contents amb ella. Per fi podem treballar amb les dades dels sensors de manera correcte i permet que els usuaris administradors puguin crear i buscar sensors.
Ara, des de negoci, ens demanen poder realitzar consultes analítiques sobre les dades que tenim. Per això, ens han donat una llista de consultes que volem poder fer sobre les dades que tenim. Aquestes consultes són:

* Consultar el valor màxim, mínim i mitjà de la temperatura dels sensors de temperatura.
* Consultar el nombre de sensors per a cada tipus de sensor.
* Consultar aquells sensors que tenen un valor de bateria inferior al 20%.

Per a poder fer aquestes consultes, necessitem una base de dades que ens permeti fer-les de manera eficient. Per això, hem decidit fer servir una base de dades columnar. En aquesta pràctica, farem servir Cassandra per a fer aquestes consultes.

Recordeu que aquestes bases de dades s'han de modelar de manera diferent a les bases de dades relacionals, es basen en la idea de modelar les dades en funció de les preguntes que volem resoldre. Per això, caldrà que penseu en com modelar les dades per a poder fer aquestes consultes de manera eficient (haureu de fer servir les estrategies de modelatge de les claus de partició i sorting que hem vist a classe i crear 3 taules, una per a cada consulta).

### Objectius

* Entendre com funciona Cassandra.
* Connectar-se a Cassandra des de Python.
* Crear les taules necessàries per a poder fer les consultes.
* Crear tres endpoints (un per a cada consulta) que retornin les dades que demanen.


## Què hem de fer?

Abans de res, explora el codi que s'ha creat per aquesta pràctica. 

### Punt 1: Mirar i Provar els tests

Tal i com vàrem fer a la setmana passada, hem creat una sèrie de tests per a comprovar que el codi que hem creat funciona correctament. Per a executar els tests, pots fer servir el següent comandament:

```bash
docker exec bdda_api sh -c "pytest"
```

També pots comprovar els tests a l'autograding de github, aquesta setmana la puntuació màxima és de 130 punts i hi ha un total d' `13` tests amb un valor de `10` punts cadascun:

Veuràs que `13` tests fallen. Això és normal, ja que encara no hem implementat el codi que passa els tests.

### Punt 2: Mirar els endpoints al fitxer controller.py:

Hem creat 3 endpoints nous que ens permetran fer les consultes que se'ns demanen. Aquests endpoints són:

* `/temperature/values`: Aquest endpoint ens retornarà el valor màxim, mínim i mitjà de la temperatura dels sensors de temperatura.

* `/quantity_by_type`: Aquest endpoint ens retornarà el nombre de sensors per a cada tipus de sensor.
  
* `/low_battery`: Aquest endpoint ens retornarà aquells sensors que tenen un valor de bateria inferior al 20%.


### Punt 3: Connexió a Cassandra des de Python

Farem servir el següent driver https://github.com/datastax/python-driver. En la classe `cassandra_client.py` teniu encapsulat el client per a connectar-vos a Cassandra. 

Podeu trobar tota la docuementació del driver aquí https://docs.datastax.com/en/developer/python-driver/3.25/api/

### Punt 4: Codificar els endpoints de controller.py

* Recodifiqueu de nou els endpoints `/sensors/{sensor_id}/data` i `sensors` de tal forma que utilitzin Cassandra. Afegiu les noves taules que necessiteu per a poder fer les consultes de manera eficient i inserteu els valors de data a les taules corresponents.

* Implementeu els endpoints `/temperature/values`, `/quantity_by_type` i `/low_battery` de tal forma que retornin les consultes demanades. Feu consultes a les taules que heu creat per a poder fer aquestes consultes de manera eficient.
  
A `controller.py` teniu una connexió a Cassandra per fer servir en els endpoints necessaris. 

Informació sobre taules i columnes a Cassandra:https://cassandra.apache.org/doc/latest/cassandra/data_modeling/data_modeling_schema.html

Informació sobre llenguatge de consultes a Cassandra: 
https://cassandra.apache.org/doc/latest/cassandra/cql/





### Punt 5: Executar els tests

Ara que ja has implementat les rutes, pots tornar a executar els tests per a veure si has fet bé les coses. Per fer-ho, has de fer servir el següent comandament:

```bash
docker exec bdda_api sh -c "pytest"
```

Si tot ha anat bé, hauries de veure que tots els tests passen.



## Entrega

Durant les pràctiques farem servir GitHub Classroom per gestionar les entregues. Per tal de clonar el repositori ja has hagut d'acceptar l'assignment a GitHub Classroom. Per entregar la pràctica has de pujar els canvis al teu repositori de GitHub Classroom. El repositori conté els tests i s'executa automàticament cada vegada que puges els canvis al teu repositori. Si tots els tests passen, la pràctica està correctament entregada.

Per pujar els canvis al teu repositori, has de fer servir el següent comandament:

```bash
git add .
git commit -m "Missatge de commit"
git push
```

## Puntuació

Aquesta pràctica té una puntuació màxima de 10 punts. La puntuació es repartirà de la següent manera:

- 6 punts: Correcta execució dels tests. Important, per a que la pràctica sigui avaluable heu d'aconseguir que com a mínim `10` dels `13` tests s'executin correctament.
- 2 punts: L'estil del codi i la seva estructura i documentació.
- 2 punts: La correcta implementació de la funcionalitat.

## Qüestionari d'avaluació de cada pràctica

Cada pràctica té un qüestionari d'avaluació. Aquest qüestionari ens permet avaluar el coneixement teòric i de comprensió de la pràctica. És obligatori i forma part de l'avaluació continua de l'assignatura. Per contestar el qüestionari, has d'anar al campus virtual de l'assignatura i anar a la secció de qüestionaris.
 


