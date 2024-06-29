# introducció-pràctiques-template

Benvingut a la plantilla de les pràctiques de l'assignatura de Bases de dades avançades de la Universitat de Barcelona.
Aquesta plantilla conté un conjunt de fitxers que et permetran crear un entorn de desenvolupament per a tota la part pràctica de la matèria.

## Què conté la plantilla?

La plantilla conté una API REST que et permetrà crear, esborrar, modificar i consultar les dades de la nostra aplicació de pràctiques. Aquesta API REST està implementada amb Python i FastAPI, i en aquest exemple està connectada a una base de dades PostgreSQL. Et serà molt útil per poder fer les pràctiques..

Totes les pràctques de l'assignatura segueixen el mateix patró però anirem treballant diferents tecnologies de bases de dades i arquitectures. Aquesta plantilla et servirà com a referència per a totes les que venen.

## Requisits previs per a totes les pràctiques

Per començar, necessitaràs tenir instal·lat Docker i Docker Compose. Si no els tens instal·lats, pots seguir les instruccions de la web oficial de Docker:

- [Instal·lar Docker](https://docs.docker.com/get-docker/)
- [Instal·lar Docker Compose](https://docs.docker.com/compose/install/)

Farem servir Docker Compose per crear un entorn de desenvolupament amb Docker. Aquest entorn contindrà un servidor PostgreSQL i un servidor FastAPI. Aquest entorn està definit en el fitxer `docker-compose.yml`. Pots xafardejar el fitxer DockerFile per veure com s'ha construït la imatge de FastAPI i el fitxer `docker-compose.yml` amb la configuració del servidor PostgreSQL i FastAPI.

Si no coneixes Docker, pots seguir aquest tutorial per entendre com funciona: [Docker Tutorial](https://docker-curriculum.com/)

Si no coneixes Docker Compose, pots seguir aquest tutorial per entendre com funciona: [Docker Compose Tutorial](https://docs.docker.com/compose/gettingstarted/)

Si no coneixes FastAPI, pots seguir aquest tutorial per entendre com funciona: [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### Opcional: Instal·lar Python 3.11, si fas servir docker no et fa falta

A part de docker, si volguessis executar l'entorn sense docker també necessitaries tenir instal·lat Python 3.11. Si no el tens instal·lat, pots seguir les instruccions de la web oficial de Python:

- [Instal·lar Python](https://www.python.org/downloads/)

(Nota: Si tens vàries versions de Python instal·lades, pots utilitzar [pyenv](https://github.com/pyenv/pyenv) per a gestionar-les)

## Com començar?

Per començar, necessitaràs clonar aquest repositori. Pots fer-ho amb el següent comandament:

```bash
git clone url-del-teu-assignment
```

Com que farem servir Docker per crear l'entorn de desenvolupament, podràs executar l'API REST sense tenir instal·lat Python. Per això, arrancar l'entorn de desenvolupament és molt senzill. Només has de fer servir el següent comandament:

```bash
docker-compose up
```

Això farà que s'executin els següents passos:

- Es construirà una imatge de Docker amb FastAPI i les dependències necessàries.
- S'executarà un contenidor de Docker amb FastAPI. Aquest contenidor arrancarà un servidor FastAPI que estarà escoltant peticions al port 8000. (http://localhost:8000) Ens hem d'assegurar que aquest port està lliure.
- S'executarà un contenidor de Docker amb PostgreSQL. Aquest contenidor arrancarà un servidor PostgreSQL que estarà escoltant peticions al port 5432. (postgresql://localhost:5432) Ens hem d'assegurar que aquest port està lliure.

Si tot ha anat bé, podràs executar les peticions a l'API REST. Per exemple, pots fer una petició GET a http://localhost:8000/ per veure si l'API REST està funcionant correctament.

Si vols parar l'entorn de desenvolupament, pots fer servir el següent comandament:

```bash
docker-compose down
```

Cal que tinguis en compte que si fas servir aquest comandament, no esborraràs tota la informació que tinguis a la base de dades, ja que per defecte down només esborra els conteidors i la xarxa entre ells. Si vols esborrar tota la informació que tinguis a la base de dades, pots fer servir el següent comandament:

```bash
docker-compose down -v
```

**Important**: Quan executem `docker-compose up`, Docker construeix una imatge de Docker amb FastAPI amb una fotografia estàtica del codi que tenim al directori. Això vol dir que si modifiquem el codi, no es veurà reflexat a l'entorn de desenvolupament. Per això, cal que executem docker-compose up cada cop que modifiquem el codi. Si no ho fem, no veurem els canvis que haguem fet.

## Què podem fer amb aquesta API REST?

Aquesta API REST representa una aplicació de gestió de sensors de temperatura i humitat. De moment, només tenim una taula a la base de dades, la taula `sensors`. Aquesta taula conté els següents camps:

- `id`: Identificador del sensor. És un camp únic i autogenerat.
- `name`: Nom del sensor.
- `latitude`: Coordenada de latitud del sensor.
- `longitude`: Coordenada de longitud del sensor.
- `joined_at`: Data en la que el sensor es va registrar a la base de dades.
- `last_seen`: Data en la que el sensor va enviar dades per última vegada.
- `temperature`: Temperatura del sensor.
- `humidity`: Humitat del sensor.
- `battery_level`: Nivell de bateria del sensor.

La API REST conté les següents rutes:

- `GET /`: Retorna un missatge de benvinguda.
- `GET /sensors`: Retorna tots els sensors de la base de dades (La implementarem durant la pràctica).
- `GET /sensors/{id}`: Retorna el sensor amb l'identificador `id`.
- `POST /sensors`: Crea un nou sensor a la base de dades.
- `DELETE /sensors/{id}`: Esborra el sensor amb l'identificador `id`.
- `POST /sensors/{id}/data`: Envia dades del sensor amb l'identificador `id`.

## Què hem de fer?

Cada pràctica tindrà com a objectiu afegir noves funcionalitats i connexions a l'aplicació, a cada una trobaràs un fitxer README amb les instruccions de la pràctica i una serie de tests automàtics que has de passar per poder-la entregar.

A més cada pràctica té un repte opcional d'un nivell de dificultat més alt. Els repte opcional no són obligatoris, però si els resols correctament et poden ajudar a sumar fins a 1 punt extra a la nota final de l'assignatura i a aprofundir en reptes claus en el disseny d'aplicacions i en la gestió de dades.

L'objectiu d'aquesta primera entrega és que et familiaritzis amb el funcionament de FastAPI i amb la creació de rutes. És a dir, no té un objectiu concret. Només has de seguir els passos que s'indiquen a continuació.

### Punt 1: Provar els tests

Per començar, has de provar els tests que s'han creat per aquesta pràctica. Per a fer-ho, has de fer servir el següent comandament:

```bash
docker exec bdda_api sh -c "pytest"
```

Veurem que part dels tests fallen. Això és normal, ja que l'objectiu de les pràctiques és fer passar tots els tests.

### Punt 2: Crear una ruta GET per a obtenir tots els sensors

La primera ruta que s'ha de crear és una ruta GET que ens permeti obtenir tots els sensors de la base de dades. Per això, has de crear una ruta GET a la ruta `/sensors` que retorni tots els sensors de la base de dades.

Per fer-ho, has de fer servir el següent codi:

```python
@app.get("/sensors")
def get_sensors():
    return []
```

Podem tornar a executar el servidor i fer una petició GET a http://localhost:8000/sensors per a veure si funciona correctament. Si tot ha anat bé, hauríem de rebre una array buida.

Per a que aquesta ruta retorni tots els sensors de la base de dades, has de fer servir el següent codi:

```python
@app.get("/sensors")
def get_sensors():
    return db.query(models.Sensor).all()
```

Aquest codi fa servir el mètode `all()` de SQLAlchemy per obtenir tots els sensors de la base de dades. Aquest mètode retorna una llista de sensors.

Si tornem a executar el servidor i fem una petició GET a http://localhost:8000/sensors, hauríem de rebre una array amb tots els sensors de la base de dades. Si no hi ha cap sensor a la base de dades, hauríem de rebre una array buida.

### Punt 3: Fer servir la ruta `POST /sensors` per a crear un sensor

La ruta per crear un sensor és la ruta `POST /sensors`. Aquesta ruta ja està implementada, intenta trobar el mètode al codi i veuràs que rep un objecte JSON amb els següents camps:

- `name`: Nom del sensor.
- `latitude`: Coordenada de latitud del sensor.
- `longitude`: Coordenada de longitud del sensor.

I si la petició és vàlida, crea un nou sensor a la base de dades i retorna el sensor creat.

Per provar aquesta ruta, has de fer servir el següent codi:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Sensor 1", "latitude": 41.387917, "longitude": 2.169919}' http://localhost:8000/sensors
```

Ara bé, fer servir curl per desplegar una petició POST és molt enutjós. Per fer-ho més fàcil, pots fer servir [Insomnia](https://insomnia.rest/) o [Postman](https://www.postman.com/). Aquests dos programes permeten fer peticions HTTP de forma molt senzilla. Al repositori de la pràctica pots trobar un fixter que conté una col·lecció d'Insomnia amb les peticions que has de fer per a completar la pràctica.

### Punt 4: Jugant amb les rutes

Ara que ja tens rutes per crear i obtenir sensors, pots jugar amb elles. Per exemple, pots crear un sensor, obtenir-lo i actualitzar-lo. Dedica un temps a jugar amb les rutes i a provar-les.

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
git commit -m "Canvis per a la pràctica 1"
git push
```

## Puntuació

Aquesta primera pràctica no té puntuació. Només has de fer-la per familiaritzar-te amb el funcionament de FastAPI i amb la creació de rutes i connexions amb una base de dades.

## Qüestionari d'avaluació de cada pràctica

Cada pràctica té un qüestionari d'avaluació. Aquest qüestionari ens permet avaluar el coneixement teòric i de comprensió de la pràctica. És obligatori i forma part de l'avaluació continua de l'assignatura.


