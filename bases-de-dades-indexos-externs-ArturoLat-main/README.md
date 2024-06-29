[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=14308468&assignment_repo_type=AssignmentRepo)
## Pràctica 4: Índexos externs

Benvingut/da a la quarta pràctica de l'assignatura de Bases de dades. Aquesta pràctica parteix de la plantilla de la pràctica anterior. Com sabeu tenim una API REST que ens permet crear, esborrar, modificar i consultar les dades d'una aplicació de sensors. En aquesta pràctica volem ampliar el cas d'ús de la nostra API per a poder buscar sobre text.

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

Fins ara hem aconseguit que els nostres usuaris puguin registrar qualsevol tipus de sensor i guardar la informació que aquest sensor genera. Ara, el volum de sensors guardats està creixent molt, i els nostres usuaris ens demanen poder buscar de manera més còmode sobre els sensors connectats a la xarxa.

Ara per ara, els nostres usuaris només poden buscar els sensor per posició (pràctica 3).

Així doncs, volem crear un índex extern per a poder buscar sobre text. Aquest índex extern, serà una instància de ElasticSearch, que ens permeti guardar els camps als que volem permetre cerques de tipus text.

Volem conservar la base de dades relacional per apoder guardar la informació estàtica i estructurada dels sensors, que ens permetrà més endavant relacionar amb altres taules de la base de dades relacional. I la base de dades documental per guardar la informació semiestructurada.

### Objectius

* Crear un índex extern (elasticsearch) per a poder buscar sobre text
* Indexar els camps: nom, descripció i tipus de sensor a l'índex extern
* Exposar un endpoint per a poder fer cerques sobre text a l'índex extern

L'endpoint haurà de tenir la següent signatura:

```
GET /search?query=...
```

On query és un diccionari de claus i valors que volem buscar. Per exemple:

```
GET /search?query={"nom":"sensor1"}
```

Per defecte es retornaran els 10 primers resultats. Però també es podrà especificar el nombre de resultats que es volen obtenir:

```
GET /search?query={"nom":"sensor1"}&size=20
```

Podem especificar també quin tipus de cerca realitzarem:

- match: cerca exacta
- prefix: cerca per prefix
- similar: cerca similar (similaritat de text)

Aquesta cerca es pot especificar a la signatura de l'endpoint:

```
GET /search?query={"nom":"sensor1"}&size=20&search_type=match
```

Per defecte, si no es especifica el tipus de cerca, es farà una cerca de tipus match.

## Què hem de fer?

Abans de res, explora el codi que s'ha creat per aquesta pràctica. 

### Punt 1: Mirar i Provar els tests

Tal i com vàrem fer a la setmana passada, hem creat una sèrie de tests per a comprovar que el codi que hem creat funciona correctament. Per a executar els tests, pots fer servir el següent comandament:

```bash
docker exec bdda_api sh -c "pytest"
```

També pots comprovar els tests a l'autograding de github, aquesta setmana la puntuació màxima és de 110 punts i hi ha un total d' `11` tests amb un valor de `10` punts cadascun:

Veuràs que 11 tests fallen i 1, els ping, funciona. Això és normal, ja que encara no hem implementat el codi que passa els tests.

### Punt 2: Mirar els endpoints al fitxer controller.py:

L'endpoint que hem afegit és aquest:

```python
	🙋🏽‍♀️ Add here the route to search sensors by query to Elasticsearch
	# Parameters:
	# - query: string to search
	# - size (optional): number of results to return
	# - search_type (optional): type of search to perform
	# - db: database session
	# - mongodb_client: mongodb client
	@router.get("/search")
	def search_sensors(query: str, size: int = 10, search_type: str = "match", db: Session = Depends(get_db), mongodb_client: MongoDBClient = Depends(get_mongodb_client), es: ElasticsearchClient = Depends(get_elastic_search)):

```

També hem modificat l'esquema Sensor, ara també te un camp `description` que es passarà amb les dades del post. Aquest camp l'heu d'afegir al document que es desa a la base de dades mongo.
 

### Punt 3: Connectar-nos a l'Elastic Search

Per accedir a l'ElasticSearch farem servir el client de python 
 [elasticsearch](https://elasticsearch-py.readthedocs.io/en/v8.6.2/index.html). Veureu que ja tenim instal·lada aquesta llibreria a la nostra imatge de Docker.
En la classe `ElasticSearchClient.py` podeu veure les crides als mètodes bàsics per a fer servir l'ElasticSearch:

```python
	def create_index(self, index_name):
        return self.client.indices.create(index=index_name)
    
    def create_mapping(self, index_name, mapping):
        return self.client.indices.put_mapping(index=index_name, body=mapping)
    
    def search(self, index_name, query):
        return self.client.search(index=index_name, body=query)
    
    def index_document(self, index_name, document):
        return self.client.index(index=index_name, document=document)
```

Per crear l'índex el podeu usar de la següent manera:

```python

es = ElasticsearchClient(host="elasticsearch")
# Create the index
es.create_index('my_index')
# Define the mapping for the index
mapping = {
    'properties': {
        'title': {'type': 'text'},
        'description': {'type': 'text'},
        'price': {'type': 'float'}
    }
}
es.create_mapping('my_index',mapping)

```

Per afegir documents del mongoDB a l'índex podem fer-ho amb el client de la següent manera:

```python

from pymongo import MongoClient
from elasticsearch import Elasticsearch

mongodb = MongoDBClient(host="mongodb")

# Select the database and collection containing the data to be indexed
mongo_db = mongodb.getDatabase("my_db")
mongo_collection = mongodb.getCollection("my_collection")

es = ElasticsearchClient(host="elasticsearch")

es_index_name = 'my_index'

# Loop through the documents in the MongoDB collection and index them in ElasticSearch
for mongo_doc in mongo_collection.find():
    es_doc = {
        'title': mongo_doc['title'],
        'description': mongo_doc['description'],
        'price': mongo_doc['price']
    }
    es.index_document(es_index_name, es_doc)

```

Per fer una cerca en l'índex extern ElasticSearch ho pots fer de la següent manera usant el client:

```python

es = ElasticsearchClient(host="elasticsearch")

# Define the name of the index to search
index_name = 'my_index'

# Define the search query
query = {
    'query': {
        'match': {
            'title': 'product'
        }
    }
}
# Perform the search and get the results
results = es.search(index_name, query)

# Loop through the results and print the title and price of each document
for hit in results['hits']['hits']:
    print(f"Title: {hit['_source']['title']}")
    print(f"Price: {hit['_source']['price']}")


```

Per veure totes les possibilitats que us ofereix les `queries` d'ElasticSearch consulteu la [documentació](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)


### Punt 4: Codificar els endpoints de controller.py

Codifiqueu de nou  els endpoints de `controller.py`de tal forma que utilitzin ElasticSearch i el MongoDb.
Haureu de modificar els mètodes a `repository.py` per tal d'implementar aquests canvis. Fixeu-vos bé amb els `schemas` que heu de fer servir per a que els `payloads` de l'API de fastAPI funcioni adequadament. 


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

- 6 punts: Correcta execució dels tests. Important, per a que la pràctica sigui avaluable heu d'aconseguir que com a mínim `11` dels `12` tests s'executin correctament.
- 2 punts: L'estil del codi i la seva estructura i documentació.
- 2 punts: La correcta implementació de la funcionalitat.

## Qüestionari d'avaluació de cada pràctica

Cada pràctica té un qüestionari d'avaluació. Aquest qüestionari ens permet avaluar el coneixement teòric i de comprensió de la pràctica. És obligatori i forma part de l'avaluació continua de l'assignatura. Per contestar el qüestionari, has d'anar al campus virtual de l'assignatura i anar a la secció de qüestionaris.
 






