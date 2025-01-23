from sqlmodel import SQLModel, Session
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
    departments_list = [
        "Administración", "Recursos Humanos", "Finanzas", "Ventas",
        "Marketing", "Logística", "Producción", "Atención al Cliente",
        "Desarrollo de Producto", "Soporte Técnico", "Tecnología de la Información", 
        "Investigación y Desarrollo", "Legal", "Compras", "Calidad", "Operaciones",
        "Estrategia", "Relaciones Públicas", "Gestión de Proyectos", "Seguridad"
    ]

    locations_list = [
        "Nueva York, Estados Unidos - 5th Avenue",
        "Tokio, Japón - Shibuya Crossing",
        "Londres, Reino Unido - Oxford Street",
        "París, Francia - Avenue des Champs-Élysées",
        "Ciudad de México, México - Paseo de la Reforma",
        "Shanghái, China - Nanjing Road",
        "Dubái, Emiratos Árabes Unidos - Sheikh Zayed Road",
        "Sídney, Australia - George Street",
        "Toronto, Canadá - Yonge Street",
        "Berlín, Alemania - Unter den Linden",
        "São Paulo, Brasil - Avenida Paulista",
        "Estocolmo, Suecia - Drottninggatan",
        "Moscú, Rusia - Tverskaya Street",
        "Mumbai, India - Marine Drive",
        "Ciudad del Cabo, Sudáfrica - Long Street",
        "Buenos Aires, Argentina - Avenida 9 de Julio",
        "Seúl, Corea del Sur - Gangnam-daero",
        "Bangkok, Tailandia - Sukhumvit Road",
        "Ámsterdam, Países Bajos - Kalverstraat",
        "Singapur - Orchard Road"
    ]
    
    factory = BusinessFactory()
    
    for i in range(len(departments_list)):
        dep_db = DepartmentTable(
            name=departments_list[i],  # Asegura que el campo 'name' se asigne
            location=f"Calle {i}, {locations_list[i]}"
        )
        session.add(dep_db)
    
    session.commit()

def _create_positions(session: Session):
    positions: dict[str] = {
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
    
    for key, name in positions.items():
        position_db: PositionTable = PositionTable(name=name)
        session.add(position_db)
        session.commit()
        session.refresh(position_db)

def _create_employees(session: Session):
    locations: dict[str] = {
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


        employee_db: EmployeeTable = EmployeeTable(name=f"Empleado {i}",
            email=f"empleado{i}@company.com",
            department_id=randint(1, 20),
            role=roles[randint(0, 4)],
            leadsTeam=bool(randint(0, 1)),
            position_id=randint(1, 40),
            salary=randint(1000, 10000),
            address=f"Calle {i} " + locations.get(randint(1, 20)),
            daily_hours=randint(8, 12),
            phone=f"+1 123 {i+2}{i*3}{i**2} 7{i+1}9{i}",
            password="password",)
        session.add(employee_db)
        session.commit()
        session.refresh(employee_db)
        
        

def _create_skills(session: Session):
    factory = SkillsFactory()
    for i in range(1, 100):
        
        skill_db = SkillTable(
            name=f"Skill {i}",
            weight=randint(0, 100),
            category=SkillsCategories.HARD if 1 == randint(0, 1) else SkillsCategories.SOFT)
        session.add(skill_db)
        session.commit()
        session.refresh(skill_db)