# app/service/item_service.py
from db.firebaseConfig import FirebaseConfig
from model.bias_metric import BiasMetric, BiasMetricRequest
from model.method import MethodInfo
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class MethodService:
    def __init__(self):
        firebase_config = FirebaseConfig()
        self.db = firebase_config.get_db()

    def fetch_all_methods(self) -> List[MethodInfo]:
        methods_ref = self.db.collection('methods')
        docs = methods_ref.stream()

        methods = []
        for doc in docs:
            data = doc.to_dict()
            
            method = MethodInfo(
                id=doc.id,
                name=data.get('name'),
                url=data.get('url'),
                description=data.get('description'),
                type=data.get('type')
            )
            methods.append(method)
        
        self.methods = methods
        return self.methods
    
    def add_method(self, name: str, url: HttpUrl, description: str, type: str) -> MethodInfo:
        methods_ref = self.db.collection('methods')
        
        result = methods_ref.add({
            'name': name,
            'url': url,
            'description': description,
            'type': type
        })

        doc_ref = result[1]
        method_id = doc_ref.id

        doc_ref.update({
            'id': method_id
        })

        new_method = MethodInfo(
            id= method_id,
            name= name,
            url= url,
            description= description,
            type= type
        )
        
        return new_method