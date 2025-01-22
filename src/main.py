from fastapi import FastAPI
import fastapi.cli
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.gzip import GZipMiddleware

from core.database.database import create_tables

import application.controllers.employee.employee_controller as emp
import application.controllers.employee.employee_skills_controller as emp_skill

import application.controllers.auth.authentication_controller as auth

import application.controllers.business.department_controller as dep
import application.controllers.business.position_controller as pos
import application.controllers.business.skills_controller as skill
import application.controllers.business.department_skills_controller as dep_skill

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    # generate_data()
    yield


def create_app() -> FastAPI:
    application = FastAPI(lifespan=lifespan, version=2, title="Employees CRUD")
    application.add_middleware(GZipMiddleware)
    application = _include_routers(application)
    return application

def _include_routers(application: FastAPI):
    application.include_router(emp.employee_router)
    application.include_router(auth.auth_router)
    application.include_router(dep.department_router)
    application.include_router(pos.position_router)
    application.include_router(skill.skills_router)
    application.include_router(emp_skill.employee_skills_router)
    application.include_router(dep_skill.dep_skills_router)
    return application

app = create_app()