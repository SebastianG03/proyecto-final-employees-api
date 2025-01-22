from sqlmodel import Session
from domain.factory.business.business_factory import BusinessFactory
from domain.factory.employee.employees_factory import EmployeesFactory
from domain.factory.skill.skills_factory import SkillsFactory

from domain.entities.types.request_types import RequestTypes
from domain.entities.employees.employees_roles import EmployeeRoles

from domain.entities.business.types.business_components import BusinessComponents
from domain.entities.skills.types.skills_categories import SkillsCategories 
from domain.entities.skills.types.skills_types import SkillsTypes 

from domain.entities.business.department.department import DepartmentBase, DepartmentTable
from domain.entities.business.position.position import PositionBase, PositionTable
from domain.entities.employees.employees import EmployeeBase, EmployeeTable
from domain.entities.skills.skill.skills import SkillBase, SkillTable
from domain.entities.skills.department.department_skills import DepartmentSkillTable

from core.database.database import get_session
from random import randint

def create_data():
    session = next(get_session())
    _create_departments(session)
    _create_positions(session)
    _create_employees(session)
    _create_skills(session)
    session.close()

def _create_departments(session: Session):
    departments = { 
        1: "Administración", 2: "Recursos Humanos", 3: "Finanzas", 4: "Ventas",
        5: "Marketing", 6: "Logística", 7: "Producción", 8: "Atención al Cliente",
        9: "Desarrollo de Producto", 10: "Soporte Técnico", 11: "Tecnología de la Información", 12: "Investigación y Desarrollo",
        13: "Legal", 14: "Compras", 15: "Calidad", 16: "Operaciones",
        17: "Estrategia", 18: "Relaciones Públicas", 19: "Gestión de Proyectos", 20: "Seguridad"
    }
    
    locations = {
        1: "Nueva York, Estados Unidos - 5th Avenue", 2: "Tokio, Japón - Shibuya Crossing", 3: "Londres, Reino Unido - Oxford Street",
        4: "París, Francia - Avenue des Champs-Élysées", 5: "Ciudad de México, México - Paseo de la Reforma", 6: "Shanghái, China - Nanjing Road",
        7: "Dubái, Emiratos Árabes Unidos - Sheikh Zayed Road", 8: "Sídney, Australia - George Street", 9: "Toronto, Canadá - Yonge Street",
        10: "Berlín, Alemania - Unter den Linden", 11: "São Paulo, Brasil - Avenida Paulista", 12: "Estocolmo, Suecia - Drottninggatan",
        13: "Moscú, Rusia - Tverskaya Street", 14: "Mumbai, India - Marine Drive", 15: "Ciudad del Cabo, Sudáfrica - Long Street",
        16: "Buenos Aires, Argentina - Avenida 9 de Julio", 17: "Seúl, Corea del Sur - Gangnam-daero", 
        18: "Bangkok, Tailandia - Sukhumvit Road", 19: "Ámsterdam, Países Bajos - Kalverstraat", 20: "Singapur - Orchard Road"
        }
    
    factory = BusinessFactory()
    
    for i in range(1, len(departments) + 1):
        department: DepartmentBase = factory.create(type=BusinessComponents.DEPARTMENT, request_type=RequestTypes.PATCH)
        department.name = departments.get(i)
        department.location = locations.get(randint(1, 20))
        dep_db = factory.create(type=BusinessComponents.DEPARTMENT, request_type=RequestTypes.TABLE_REQUESTS, base_content=department)
        session.add(dep_db)
        session.commit()
        session.refresh(dep_db)

def _create_positions(session: Session):
    positions = {
        1: "Gerente General", 2: "Analista Financiero", 3: "Desarrollador de Software", 4: "Diseñador Gráfico", 
        5: "Administrador de Sistemas", 6: "Especialista en Marketing Digital", 7: "Ingeniero de Datos", 8: "Técnico de Soporte",
        9: "Científico de Datos", 10: "Gerente de Ventas", 11: "Especialista en Recursos Humanos", 12: "Contador",
        13: "Consultor Empresarial", 14: "Gerente de Producto", 15: "Ingeniero de Redes", 16: "Desarrollador Front-End", 17: "Desarrollador Back-End",
        18: "Gerente de Proyectos", 19: "Investigador de Mercado", 20: "Editor de Contenidos", 21: "Arquitecto de Software", 22: "Especialista en Seguridad Informática",
        23: "Diseñador UX/UI", 24: "Auditor Interno", 25: "Ingeniero de Calidad", 26: "Especialista en Comercio Electrónico", 27: "Redactor Técnico",
        28: "Agente de Servicio al Cliente", 29: "Especialista en Logística", 30: "Programador Mobile", 31: "Desarrollador de Videojuegos", 32: "Gerente de Operaciones",
        33: "Técnico de Mantenimiento", 34: "Ingeniero Civil", 35: "Especialista en Analítica Web", 36: "Diseñador Industrial",
        37: "Ingeniero Mecánico", 38: "Jefe de Almacén", 39: "Especialista en Inteligencia Artificial", 40: "Analista de Negocios"
        }
    
    factory = BusinessFactory()
    
    for i in range(1, len(positions) + 1):
        position: PositionBase = factory.create(type=BusinessComponents.POSITION, request_type=RequestTypes.PATCH)
        position.name = positions.get(i)
        position_db = factory.create(type=BusinessComponents.POSITION, request_type=RequestTypes.TABLE_REQUESTS, base_content=position)
        session.add(position_db)
        session.commit()
        session.refresh(position_db)

def _create_employees(session: Session):
    locations = {
        1: "Nueva York, Estados Unidos - 5th Avenue", 2: "Tokio, Japón - Shibuya Crossing", 3: "Londres, Reino Unido - Oxford Street",
        4: "París, Francia - Avenue des Champs-Élysées", 5: "Ciudad de México, México - Paseo de la Reforma", 6: "Shanghái, China - Nanjing Road",
        7: "Dubái, Emiratos Árabes Unidos - Sheikh Zayed Road", 8: "Sídney, Australia - George Street", 9: "Toronto, Canadá - Yonge Street",
        10: "Berlín, Alemania - Unter den Linden", 11: "São Paulo, Brasil - Avenida Paulista", 12: "Estocolmo, Suecia - Drottninggatan",
        13: "Moscú, Rusia - Tverskaya Street", 14: "Mumbai, India - Marine Drive", 15: "Ciudad del Cabo, Sudáfrica - Long Street",
        16: "Buenos Aires, Argentina - Avenida 9 de Julio", 17: "Seúl, Corea del Sur - Gangnam-daero", 
        18: "Bangkok, Tailandia - Sukhumvit Road", 19: "Ámsterdam, Países Bajos - Kalverstraat", 20: "Singapur - Orchard Road"
        }
    roles = [ EmployeeRoles.ADMIN, EmployeeRoles.DEPARTMENT_MANAGER, EmployeeRoles.INTERN,
              EmployeeRoles.TRAINEE, EmployeeRoles.TEAM_MANAGER ]
    factory = EmployeesFactory()
    for i in range(100):
        employee: EmployeeBase = EmployeeBase(
            name=f"Empleado {i}",
            email=f"empleado{i}@company.com",
            department_id=randint(1, 20),
            role=roles[randint(0, 4)],
            leadsTeam=bool(randint(0, 1)),
            position_id=randint(1, 40),
            salary=randint(1000, 10000),
            address=f"Calle {i} " + locations.get(randint(1, 20)),
            daily_hours=randint(8, 12),
            phone=f"+1 123 {i+2}{i*3}{i**2} 7{i+1}9{i}",
            password="password",
        ) 

        employee_db = factory.create(base_content=employee, requestType=RequestTypes.TABLE_REQUESTS)
        session.add(employee_db)
        session.commit()
        session.refresh(employee_db)
        
        

def _create_skills(session: Session):
    factory = SkillsFactory()
    for i in range(1, 100):
        skill = SkillBase(
            name=f"Skill {i}",
            weight=randint(0, 100),
            category=SkillsCategories.HARD if 1 == randint(0, 1) else SkillsCategories.SOFT
        )

        skill_db = factory.create(base_content=skill, requestType=RequestTypes.TABLE_REQUESTS)
        session.add(skill_db)
        session.commit()
        session.refresh(skill_db)