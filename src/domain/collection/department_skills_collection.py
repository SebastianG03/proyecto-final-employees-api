from typing import Dict, List
from pydantic import BaseModel
from domain.collection.collection_models import CollectionModel
from domain.entities.business.department.department import DepartmentTable
from domain.entities.skills.department.department_skills import DepartmentSkillTable
from domain.entities.skills.skill.skills import SkillTable
from domain.entities.skills.types.skills_categories import SkillsCategories
from domain.collection.collection import CollectorBase, CollectionBase, CollectionSingleton

## Objetivos: Ordenar la lista en base al peso total, peso de
## habilidades duras, peso de habilidades suaves y su performance de mayor a menor

class DepartmentSkillModel(CollectionModel):
    model_skill_reference: DepartmentSkillTable

class DepartmentSkillsCollector(CollectorBase):
    model_reference: DepartmentSkillTable
    model_skills: List[DepartmentSkillModel]

class DepartmentSkillsCollection(CollectionBase, metaclass=CollectionSingleton):
    collection: list[DepartmentSkillsCollector]
    
    def __init__(
        self, 
        initial_collection: list[CollectorBase] = None):
        super().__init__()
        self.collection = initial_collection or []
        self.reference_map: Dict[int, CollectorBase] = {
            id(item.original_reference): item for item in self.collection
        } 
        
    def calculate_weight(self, skill_type):
        for collector_list in self.collection:
            filtered_collection: list[DepartmentSkillModel] = self.filter_by_weight(collector= collector_list,category=skill_type)
            raiting = []

            for collector in filtered_collection:
                segment = collector.model_skill_reference.skill_segment
                priority = collector.model_skill_reference.skill_priority
                weight = collector.model_skill_reference.weight
                raiting.append((segment * weight + priority * weight) / segment)

            if skill_type == SkillsCategories.HARD:
                collector_list.skills_raiting.hard_weight = 1 / sum(raiting)
            elif skill_type == SkillsCategories.SOFT:
                collector_list.skills_raiting.soft_weight = 1 / sum(raiting)
    
    def calculate_total_weight(self):
        for collector_list in self.collection:
            collector_list.skills_raiting.total_weight = (
                (1 / collector_list.skills_raiting.hard_weight) + (1 / collector_list.skills_raiting.soft_weight)
                ) / len(collector_list.model_skills)