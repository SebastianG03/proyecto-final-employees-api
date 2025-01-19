from typing import Dict
from pydantic import BaseModel
from domain.entities.business.department.department import DepartmentTable
from domain.entities.skills.department.department_skills import DepartmentSkillTable
from domain.entities.skills.skill.skills import SkillTable
from domain.entities.skills.types.skills_categories import SkillsCategories
from domain.collection.collection import CollectorBase, CollectionBase
from domain.entities.interfaces.singleton import FactorySingleton

## Objetivos: Ordenar la lista en base al peso total, peso de
## habilidades duras, peso de habilidades suaves y su performance de mayor a menor
class DepartmentSkillsCollector(CollectorBase):
    model_reference: DepartmentSkillTable

class DepartmentSkillsCollection(CollectionBase, metaclass=FactorySingleton):
    original_reference: DepartmentTable
    collection: list[DepartmentSkillsCollector]
    
    def __init__(
        self, 
        initial_collection: list[CollectorBase] = None):
        super().__init__()
        self.collection = initial_collection or []
        self.reference_map: Dict[int, CollectorBase] = {
            id(item.original_reference): item for item in self.collection
        } 
        
    def sort_by_weight(self, skill_type: SkillsCategories = SkillsCategories.SOFT):
        filtered_collection = filter(lambda x: x.skill_reference.category == skill_type, self.collection)
        
        self.filtered_collection = sorted(filtered_collection, key=lambda x: x.total_weight, reverse=True)
        self.collection = filtered_collection
    
    def get_weight(self, skill_type = None):
        if skill_type is SkillsCategories.HARD:
            return self.hard_weight
        elif skill_type is SkillsCategories.SOFT:
            return self.soft_weight
    
    def calculate_weight(self, skill_type):
        filtered_collection = filter(lambda x: x.skill_reference.category == skill_type, self.collection)
        raiting = []
        
        for collector in filtered_collection:
            segment = collector.original_skill_reference.skill_segment
            priority = collector.original_skill_reference.skill_priority
            weight = collector.original_skill_reference.weight
            raiting.append((segment * weight + priority * weight) / segment)
            
        if skill_type == SkillsCategories.HARD:
            self.hard_weight = 1 / sum(raiting)
        elif skill_type == SkillsCategories.SOFT:
            self.soft_weight = 1 / sum(raiting)
    
    def calculate_total_weight(self, skill_type):
        department_values = []
        skills_values = []
        
        for collector in self.collection:
            segment = collector.original_skill_reference.skill_segment
            priority = collector.original_skill_reference.skill_priority
            weight = collector.original_skill_reference.weight
            department_values.append([ segment, priority])
            skills_values.append([weight, weight * priority])
        
        raiting = []
        for i in range(0, len(department_values), 1):
            for j in range(0, len(skills_values), -1):
                raiting.append(department_values[i][0] * skills_values[j][0] + department_values[i][1] * skills_values[j][1])
                
        self.total_weight = 1 / sum(raiting) 