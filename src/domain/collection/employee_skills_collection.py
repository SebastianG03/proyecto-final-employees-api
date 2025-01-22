
from typing import Dict, List

from domain.collection.collection import CollectorBase, CollectionBase, CollectionSingleton
from domain.collection.collection_models import CollectionModel
from domain.entities.employees.employees import EmployeeTable

from domain.entities.skills.types.skills_categories import SkillsCategories 
from domain.entities.skills.employee.employee_skills import EmployeeSkillTable



class EmployeeSkillModel(CollectionModel):
    model_skill_reference: EmployeeSkillTable

class EmployeeSkillsCollector(CollectorBase):
    model_reference: EmployeeTable
    model_skills: List[EmployeeSkillModel]
    
class EmployeeSkillsCollection(CollectionBase, metaclass=CollectionSingleton):
    collection: list[EmployeeSkillsCollector]
    
    def __init__(
        self, 
        initial_collection: list[CollectorBase] = None):
        super().__init__()
        self.collection = initial_collection or []
        self.reference_map: Dict[int, CollectorBase] = {
            id(item.original_reference): item for item in self.collection
        } 
    
    def calculate_weight(self, skill_type: SkillsCategories) -> int:
        for collector in self.collection:
            filtered_collection = self.filter_by_weight(collector, skill_type)
            raiting: list[int] = []

            employee_raiting = [[ collector.model_reference.projects_cancelled / 100, 
                                 collector.model_reference.projects_completed / 100 , 
                                 collector.model_reference.projects_rejected / 100 ],
                                [collector.model_reference.daily_hours, 
                                 collector.model_reference.performance, 
                                 collector.model_reference.performance * 
                                 collector.model_reference.time_employee_months]]

            skill_value = []
            for skill in filtered_collection:
                skill_value.append([skill.skill_reference.weight, skill.model_skill_reference.domain])

            for skill in skill_value:
                for raiting in employee_raiting:
                    raiting.append(skill[0] * raiting[0] + skill[1] * raiting[1] + skill[2] * raiting[2])

            if skill_type == SkillsCategories.HARD:
                collector.skills_raiting.hard_weight = 1 / sum(raiting)
            elif skill_type == SkillsCategories.SOFT:
                collector.skills_raiting.soft_weight = 1 / sum(raiting)
            
    
    
    def calculate_total_weight(self):
        self.calculate_weight(SkillsCategories.HARD)
        self.calculate_weight(SkillsCategories.SOFT)
        for collector in self.collection:
            self.total_weight = ((1 / collector.skills_raiting.hard_weight) + (1 / collector.skills_raiting.soft_weight))/ len(collector.model_skills)
    
    def _calculate_performance(self):
        for collector in self.collection:
            employee_raiting = [[collector.model_reference.projects_cancelled / 100,
                                 collector.model_reference.projects_completed / 100 , 
                                 collector.model_reference.projects_rejected / 100 ],
                                [collector.model_reference.daily_hours, 
                                 collector.model_reference.performance, 
                                 collector.model_reference.performance * 
                                 collector.model_reference.time_employee_months]]
            performance = 0

            for raiting in employee_raiting:
                performance += raiting[0] * raiting[0] + raiting[1] * raiting[1] + raiting[2] * raiting[2]

            collector.skills_raiting.performance = performance

        
        

