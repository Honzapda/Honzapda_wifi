from pymongo import MongoClient, IndexModel, ASCENDING
from datetime import datetime, timedelta, timezone
from wifisearch_async import wifiSearch
import asyncio
from decouple import config

def insert_document(collection,shopId):
    count = asyncio.run(wifiSearch())
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=1)
    result=collection.insert_one({'count': count, 'expire_at': expire_at, 'shopId': shopId})
    return result.inserted_id


def admin_main(shopId):   
  
    # MongoDB 연결
    client = MongoClient(config('MONGO_URI'))

    db = client['honzapda_wifi']  
    collection = db['cafe']  

    index = IndexModel([("expire_at", ASCENDING)], expireAfterSeconds=0)
    collection.create_indexes([index])

    inserted_id=insert_document(collection,shopId)
    print(inserted_id)

    # Change Stream 생성
    with collection.watch() as stream:
        for change in stream:
            # 삭제된 문서의 _id를 출력하고, 데이터를 다시 삽입합니다.
            if change['operationType'] == 'delete' and change['documentKey']['_id'] == inserted_id:
                print(f"Document deleted: {inserted_id}")
                inserted_id=insert_document(collection,shopId)
                print(inserted_id)