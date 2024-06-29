[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=13985456&assignment_repo_type=AssignmentRepo)
# Bases de dades clau valor

Benvingut/da a la segona pràctica de l'assignatura de Bases de dades clau valor. Aquesta pràctica parteix de la plantilla de la pràctica anterior. Com sabeu tenim una API REST que ens permet crear, esborrar, modificar i consultar les dades d'una aplicació de sensors. Durant aquesta pràctica, treballarem amb una base de dades clau valor i farem servir Redis per a implementar-la.

## Repàs conceptes

### Bases de dades clau valor
Les Bases de dades clau valor són un tipus de bases de dades que emmagatzemen dades en format clau-valor. Aquestes bases de dades són molt eficients per a emmagatzemar dades que es poden identificar amb una clau única.

### Claus
Les claus són els identificadors únics que utilitzem per a emmagatzemar dades a la base de dades. Les claus són molt importants perquè ens permeten accedir a les dades de manera molt eficient. Hi ha diferents tipus de claus:

- **Clau simple**: La clau simple és la clau més senzilla. Una clau simple és una cadena de caràcters que identifica una única entrada a la base de dades. Per exemple, si volem emmagatzemar les dades d'un sensor de temperatura, podem utilitzar la clau simple `sensor-1` per a identificar aquest sensor. Aquesta clau simple identifica de manera única aquest sensor. En el nostre cas, una clau senzilla podria ser l'id d'un sensor o el nom d'un sensor (fixeu-vos que vem forçar que el nom del sensor sigui únic).

- **Clau composta**: Cada clau es correspon a un sól valor, si volem emmagatzemar més d'un valor per a una clau, podem utilitzar una clau composta. Una clau composta és una clau que conté un o més identificadors únics i tants qualificadors com siguin necesaris. Per exemple, si volem emmagatzemar la temperatura d'un sensor, podem utilitzar la clau composta `sensor-1:temperatura` per a identificar aquest sensor. Aquesta clau composta identifica de manera única aquest sensor i la qualifica per a saber que el que emmagatzemarà com a valor serà la temperatura.

Dissenyar les claus és bàsic quan es treballa amb bases de dades clau valor. Les claus han de ser úniques i han de ser fàcils de generar i de llegir.

### Valors
Els valors són les dades que emmagatzemem a la base de dades. En funció de la base de dades que utilitzem, els valors poden ser de diferents tipus. Per exemple, en Redis els valors poden ser de tipus string, hash, set, sorted set o list.


### Redis
Redis és una base de dades clau valor molt popular que es pot utilitzar per a implementar aquest tipus de bases de dades. Redis està escrit en C i té una implementació de clients en diferents llenguatges de programació, incloent Python.

És una base de dades molt eficient que guarda les dades en memòria, al no treballar en disc s'acostuma a utilitzar en aplicacions sense peristencia, com els caches. No obstant es pot configurar per a que guardi les dades en disc, per a això utilitza un sistema de snapshots i logs.

Per a més informació, podeu consultar la web oficial de Redis: [https://redis.io/](https://redis.io/)

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

## Objectius de la pràctica

Durant aquesta setmana la nostra aplicació ha crescut molt, més de 100.000 sensors s'han creat i s'han connectat a la nostra plataforma.

Tots aquests sensors envien les seves dades amb una freqüència molt alta, i això provoca que la nostra plataforma no pugui processar tant volum d'escriptures.

De fet, ha posat en manifest un error de disseny molt gran del sistema. Al fer servir una única taula per a emmagatzemar tant les dades estàtiques del sensors (com el seu nom, la seva ubicació, etc) com les dades dinàmiques (com la seva temperatura, humitat, etc), les escriptures de les dades dinàmiques estan provocant que la taula sigui escrita molt sovint, i això provoca que el rendiment de la nostra plataforma es vegi afectat.

Per això, hem decidit que és el moment de fer una reestructuració de la nostra base de dades. En comptes d'emmagatzemar totes les dades en una única taula, hem decidit que és millor emmagatzemar les dades estàtiques en una taula i les dades dinàmiques (la última dada de temperatura i humitat de cada sensor) a una base de dades clau valor.

## Què hem de fer?

Abans de res, explora el codi que s'ha creat per aquesta pràctica. Pots veure que s'ha mantingut la classe `Sensor` que representa un sensor. Aquesta classe conté els atributs que són estàtics, com el nom, la ubicació, etc. Però s'han eliminat els atributs que són dinàmics, com la temperatura, la humitat o la data de la última actualització.

### Punt 1: Provar els tests

Tal i com vem fer a la setmana passada, hem creat una sèrie de tests per a comprovar que el codi que hem creat funciona correctament. Per a executar els tests, pots fer servir el següent comandament:

```bash
docker exec bdda_api sh -c "pytest"
```

També pots comprovar els tests a l'autograding de github, aquesta setmana la puntuació màxima és de 100 punts i hi ha un total de 5 tests amb un valor de 20 punts cadascun:

Veuràs que tots els tests fallen. Això és normal, ja que encara no hem implementat el codi que passa els tests.

### Punt 2: Connectar-nos a la base de dades de Redis

Per a començar, hem de fer que els sensors puguin escriure les seves dades a la base de dades. Per a fer-ho, hem de fer servir la ruta `POST /sensors/{sensor_id}/data`. Veureu que aquesta ruta no està implementada, però que ja tenim un test que comprova que funciona correctament. Implementeu la funció `record_data`en el controlador que implementi aquesta ruta. 

Si ens fixem amb deteniment als resultats del test, veurem que el test espera que la ruta `POST /sensors/{sensor_id}/data` rebi un objecte JSON amb els següents camps:

- `temperature`: Temperatura del sensor.
- `humidity`: Humitat del sensor` 
- `battery_level`: Nivell de la bateria
- `last_seen`: Últim cop en que es va connectar el sensor  

I si la petició és vàlida, actualitza la dada del sensor a la base de dades i retorna simplement un HTTP OK (200).

Per a escriure dades a redis necesitarem una instancia de Redis, fixeu-vos que ja tenim una instància de Redis a la nostra configuració de docker-compose. Aquesta instància de Redis està configurada per a que es pugui accedir des de qualsevol altre contenidor de docker que estigui a la mateixa xarxa.

Per a accedir a la instància de Redis des de Python, podeu fer servir la llibreria [redis-py](https://redis-py.readthedocs.io/en/latest/). Veureu que ja tenim instal·lada aquesta llibreria a la nostra imatge de Docker.

A continuació podeu veure un exemple de com escriure dades a redis des de Python:

```python
redis = redis.Redis(host='redis', port=6379, db=nom_de_la_base_de_dades)
redis.set('foo', 'bar')
```

Aquest exemple crea una connexió a la instància de Redis que està a la mateixa xarxa que el contenidor de Docker, i després escriu la clau `foo` amb el valor `bar` a la base de dades `nom_de_la_base_de_dades`.

Per a llegir dades de redis, podeu fer servir el mètode `get`:

```python
redis = redis.Redis(host='redis', port=6379, db=nom_de_la_base_de_dades)
redis.get('foo')
```

Aquest exemple crea una connexió a la instància de Redis que està a la mateixa xarxa que el contenidor de Docker, i després llegeix la clau `foo` de la base de dades `nom_de_la_base_de_dades`.

Com us podeu imaginar, anar obtenint la connexió a la base de dades cada vegada que volem escriure o llegir dades és molt ineficient. Per això,  creeu una classe `RedisClient` que encapsuli la connexió a la base de dades i que tingui els mètodes `set` i `get` per a escriure i llegir dades de la base de dades.

Veureu que hem creat un módul nou dins el módul `sensors` anomenat `last_data`. Feu servir aquest mòdul per a emmagatzemar les dades dinàmiques dels sensors a redis.

Ara hem de fer que es puguin veure les dades dels sensors a la base de dades. Per a fer-ho, hem de fer servir la ruta `GET /sensors/{sensor_id}/data`. Veureu que aquesta ruta no està implementada, però que ja tenim un test que comprova que funciona correctament. Implementeu la funció `get_data` en el controlador associada en aquesta ruta. 

### Punt 3: Executar els tests

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

- 6 punts: Correcta execució dels tests. Important, per a que la pràctica sigui evaluable heu d'aconseguir que com a mínim 3 dels 5 tests s'executin correctament.
- 2 punts: L'estil del codi i la seva estructura i documentació.
- 2 punts: La correcta implementació de la funcionalitat.

## Qüestionari d'avaluació de cada pràctica

Cada pràctica té un qüestionari d'avaluació. Aquest qüestionari ens permet avaluar el coneixement teòric i de comprensió de la pràctica. És obligatori i forma part de l'avaluació continua de l'assignatura. Per contestar el qüestionari, has d'anar al campus virtual de l'assignatura i anar a la secció de qüestionaris.


