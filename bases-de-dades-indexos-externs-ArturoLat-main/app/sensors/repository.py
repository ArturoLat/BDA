import json

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas
from app.redis_client import RedisClient
from ..elasticsearch_client import ElasticsearchClient
from ..mongodb_client import MongoDBClient

def get_sensor(db: Session, sensor_id: int) -> Optional[models.Sensor]:
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def get_sensor_mongo(mongodb: MongoDBClient, db_sensor: models.Sensor) -> schemas.SensorCreate:
    sensor_dict = mongodb.getCollection('Sensors').find_one({'name': db_sensor.name}, {'_id': 0})
    sensor_dict.update({'id': db_sensor.id})
    return sensor_dict

def get_sensor_by_name(db: Session, name: str) -> Optional[models.Sensor]:
    return db.query(models.Sensor).filter(models.Sensor.name == name).first()

def get_sensors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Sensor]:
    return db.query(models.Sensor).offset(skip).limit(limit).all()
def create_sensor(db: Session, sensor: schemas.SensorCreate, mongodb: MongoDBClient, elasticdb: ElasticsearchClient) -> models.Sensor:
    db_sensor = models.Sensor(name=sensor.name)

    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)

    db_sensor_data = sensor.dict()
    # Guardem a MONGODB
    mongodb.insertDoc(db_sensor_data)

    elastic_data = {
        'name': sensor.name,
        'type': sensor.type,
        'description': sensor.description
    }

    elasticdb.index_document('sensors', elastic_data)

    db_sensor_dict = sensor.dict()
    db_sensor_dict.update({'id': db_sensor.id})

    return db_sensor_dict

def record_data(redis: RedisClient, sensor_id: int, data: schemas.SensorData) -> schemas.SensorData:
    db_sensordata = data
    redis.set(sensor_id, json.dumps(data.dict()))
    return db_sensordata

def get_data(redis: RedisClient, db_sensor: models.Sensor):
    db_data = redis.get(db_sensor.id)

    if db_data is None:
        raise HTTPException(status_code=404, detail="Sensor data not found")
    json_data = json.loads(db_data)
    # Create the dictionary for return with id or name if exists
    db_data = {
        'id': db_sensor.id,
        'name': db_sensor.name
    }
    # We add the information of get_Data at id and name
    db_data.update(json_data)
    return db_data

def delete_sensor(db: Session, sensor_id: int, mongodb: MongoDBClient, redis: RedisClient, elasticdb: ElasticsearchClient):
    db_sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    db.delete(db_sensor)
    db.commit()
    mongodb.deleteDoc(db_sensor.name)
    redis.delete(sensor_id)
    return db_sensor

def get_sensors_near(mongodb: MongoDBClient, latitude: float, longitude: float, radius: float, redis: RedisClient, db: Session):
    list_near = []
    query = {"latitude": {"$gte": latitude - radius, "$lte": latitude + radius},
     "longitude": {"$gte": longitude - radius, "$lte": longitude + radius}}

    sensors = mongodb.collection.find(query)
    for sensor in sensors:
        db_sensor = get_sensor_by_name(db, sensor['name'])
        db_sensor_data = get_data(redis, db_sensor)
        list_near.append(db_sensor_data)

    return list_near

def search_sensors(db: Session, mongodb: MongoDBClient, elasticdb: ElasticsearchClient, query=str, size=int, search_type=str):
    search_sensors_dict = []
    #We get the final query
    final_query = get_query(query, search_type)
    #We search it in Elastic DB
    query_results = elasticdb.search('sensors', final_query, size)

    # We see in the hits of the query_results
    for doc in query_results['hits']['hits']:
        db_sensor = get_sensor_by_name(db, doc['_source']['name'])
        mongo_sensor = get_sensor_mongo(mongodb, db_sensor)
        search_sensors_dict.append(mongo_sensor)

    return search_sensors_dict


#Method for get the query for search sensors that depends on the type of search
#Match and prefix have the same type of query and Similar is diferent.
def get_query(query=str, search_type=str):
    final_query = {}
    query = json.loads(query.lower())
    if search_type in ['match', 'prefix']:
        final_query = {
            'query': {
                search_type: query
            }
        }
    elif search_type == 'similar':
        key = list(query)[0]
        final_query = {
            "query": {
                "match": {
                    key: {
                        "query": query[key],
                        "fuzziness": 'auto',
                        'operator': 'and'
                    }
                }
            }
        }

    return final_query