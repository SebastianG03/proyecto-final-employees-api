from typing import Dict
from sqlmodel import SQLModel
from abc import ABC, abstractmethod

from domain.entities.skills.types.skills_categories import SkillsCategories
from domain.collection.collection_models import *

class CollectionBase(ABC):
    collection: list[CollectorBase] = []
    
    def __init__(
        self, 
        initial_collection: list[CollectorBase] = None):
        super().__init__()
        self.collection = initial_collection or []
        self.reference_map: Dict[int, CollectorBase] = {
            id(item.model_reference): item for item in self.collection
        } 
    
    def append(self, collector: CollectorBase):
        ref = self.find_by_reference(collector.model_reference)
        if(ref is not None):
            self.collection.append(collector)
            self.reference_map[id(collector.model_reference)] = collector
    
    def pop(self, index: int) -> CollectorBase:
        collector = self.collection.pop(index)
        self.reference_map.pop(id(collector.model_reference))
        return collector
    
    def remove(self, collector: CollectorBase):
        if collector in self.collection:
            self.collection.remove(collector)
            self.reference_map.pop(id(collector.model_reference), None)
    
    def find_by_reference(self, model_reference: SQLModel) -> CollectorBase | None:
        return self.reference_map.get(id(model_reference))
         
          
    def sort_by_weight(self) -> list[CollectorBase]:
        return sorted(self.collection, key=lambda x: x.skills_raiting.total_weight, reverse=True)
        
    def filter_by_weight(self, collector: CollectorBase, category: SkillsCategories = SkillsCategories.SOFT) -> list[CollectionModel]:
        return filter(lambda x: x.skill_reference.category == category, collector.model_skills)
    
    def get_weight(self, collector: CollectorBase, category: SkillsCategories = None) -> float:
        return collector.skills_raiting.hard_weight if category == SkillsCategories.HARD else collector.skills_raiting.soft_weight
    
    def get_total_weight(self, model_reference: SQLModel) -> float:
        return self.find_by_reference(model_reference).skills_raiting.total_weight
    
    @abstractmethod
    def calculate_weight(self, skill_type: SkillsCategories):
        pass
    
    
    @abstractmethod
    def calculate_total_weight(self):
        pass
    