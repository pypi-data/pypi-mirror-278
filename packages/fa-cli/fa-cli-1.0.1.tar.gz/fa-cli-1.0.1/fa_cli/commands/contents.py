PROJECT_STRUCTURE = {
    ".": {
        ".gitignore": """**/__pycache__/
.env
yoyo.ini
engines/
""",
        "app.py": """import inspect
import uuid
import src.controller as controller
from src.db.migration import run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.jwt_middleware import JWTMiddleware
from src.middleware.logging_middleware import LoggingMiddleware, configure_logging
configure_logging(level='INFO', service='Mediator service',
                  instance=str(uuid.uuid4()))
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTMiddleware)
app.add_middleware(LoggingMiddleware)
controller_classes = []


controller_classes = [cls for name, cls in inspect.getmembers(
    controller) if inspect.isclass(cls) and hasattr(cls, 'controller')]
for cls in controller_classes:
    cls(app)
if __name__ == "__main__":
    import uvicorn
    run()
    # uvicorn.run(app="app:app", host="0.0.0.0", port=5000, reload=True)
    uvicorn.run(app=app, host="0.0.0.0", port=5000)
""",
        "configs.py": """import os
from dotenv import load_dotenv
load_dotenv()

# database config
PSQL_DATABASE = os.getenv("PSQL_DATABASE")
PSQL_HOST = os.getenv("PSQL_HOST")
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
PSQL_PORT = os.getenv("PSQL_PORT")
PSQL_USER = os.getenv("PSQL_USER")
ECHO_QUERIES = False if os.getenv('ECHO_QUERIES').lower() == "false" else True
sync_db_url = f'postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{
    PSQL_HOST}:{PSQL_PORT}/{PSQL_DATABASE}'

async_db_url = f'postgresql+asyncpg://{PSQL_USER}:{
    PSQL_PASSWORD}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DATABASE}'

# JWT envs

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


# Allowed paths :

ALLOWED_PATHS = [
    "/docs",
    "/openapi.json",
    "/favicon.ico",
    "/user/sign-up"
]
""",
        ".env": """# database configuration
PSQL_DATABASE=crud
PSQL_HOST=localhost
PSQL_PASSWORD=123456
PSQL_PORT=5432
PSQL_USER=postgres
ECHO_QUERIES=False
# paths configurations
SECRET_KEY=this_is_my_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=20
""",
        "migration_rollback.sh": """#!/bin/bash

# Load variables from the .env file
source .env

# Run yoyo rollback command using the environment variables
yoyo rollback --database postgresql://$PSQL_USER:$PSQL_PASSWORD@$PSQL_HOST/$PSQL_DATABASE ./src/db/migrations
""",
        "requirements.txt": """yoyo-migrations
python-dotenv
fastapi
uvicorn
passlib
pyjwt
python_json_logger""",
        "yoyo.ini": """[DEFAULT]
sources = ./db/migrations
database = postgresql://postgres:123456@localhost/bane
migration_table = _yoyo_migration
batch_mode = off
verbosity = 0

"""
    },
    "src": {
        "common": {
            "hasher.py": """from passlib.context import CryptContext

hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password: str, hashed_password: str) -> bool:
    return hasher.verify(password, hashed_password)
""",
            "jwt_token.py": """from fastapi import HTTPException
import jwt
from datetime import datetime, timezone, timedelta
from src.db.tables.user import Users
from configs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validate_token(token: str) -> bool:
    if not token or token == "":
        raise HTTPException(
            status_code=403,
            detail="Wrong credentials"
        )
    payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("username")
    email = payload.get("email")
    if username is None and email is None:
        raise HTTPException(
            status_code=403,
            detail="Wrong credentials"
        )
    user = await Users.select(name=username, email=email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user
"""
        },
        "controller": {
            "core.py": """from fastapi import APIRouter, Depends
# from db.connector import get_db_session
from abc import ABC


def Controller(cls):
    cls.controller = True
    return cls


class GenericController():

    def __init__(self, app: APIRouter) -> None:
        self.app: APIRouter = app
        self.router: APIRouter = APIRouter()

    def add_api_route(self, path, endpoint, methods, dependencies: list = None):
        print(type(endpoint))
        self.router.add_api_route(
            path, endpoint, methods=methods, dependencies=dependencies)


class BaseController(ABC, GenericController):
    def __init__(self, app: APIRouter) -> None:
        super().__init__(app)
""",
            "__init__.py": """from .user.router import *""",
            "user": {
                "router.py": """from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.controller.core import GenericController, Controller
from src.db.tables.user import Users

from .schema import UserCreate
from src.common.hasher import hasher


@Controller
class UserController(GenericController):
    def __init__(self, app: APIRouter) -> None:
        super().__init__(app)
        self.url_prefix = "/user"
        self.add_api_route("/sign-up", self.create_user, methods=['POST'])
        self.app.include_router(self.router, prefix=self.url_prefix)

    async def create_user(self, user: UserCreate):
        exist = await Users.select(email=user.email)
        if exist:
            raise HTTPException(
                status_code=400,
                detail="Email already registred"
            )
        user.password = hasher.hash(user.password)
        registerd = await Users.insert(**user.dict())
        return JSONResponse(status_code=200, content=dict(id=registerd.get('id')))

    async def get_user(self, id: int):
        exists = await Users.select(id=id)
        if exists:
            return JSONResponse(
                status_code=200,
                content=exists
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"User with id= {id} not found"
            )
""",
                "schema.py": """from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
"""
            }
        },
        "db": {
            "connector.py": """import contextlib
from typing import Any, AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from configs import async_db_url, ECHO_QUERIES


class DatabaseSessionManager:

    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}) -> None:
        self._engine = create_async_engine(
            url=host,
            **engine_kwargs
        )
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine, self._sessionmaker = None, None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.commit()
            await session.flush()
            await session.close()


sessionmanager = DatabaseSessionManager(
    async_db_url,
    {
        "echo": ECHO_QUERIES
    }
)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session
""",
            "core_orm.py": """from sqlalchemy import Integer
from typing import Any, List, Dict
from sqlalchemy.future import select
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import delete as sqlalchemy_delete,  update as sqlalchemy_update
from sqlalchemy.orm import DeclarativeBase, declared_attr, joinedload, mapped_column

from .connector import sessionmanager


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseORM(Base):
    __abstract__ = True
    id = mapped_column(Integer, primary_key=True, autoincrement=True)

    def dump(self, relationships: List[str] = None):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if relationships:
            for rel in relationships:
                rel_data = getattr(self, rel)
                if isinstance(rel_data, list):
                    data[rel] = [item.dump() for item in rel_data]
                else:
                    data[rel] = rel_data.dump() if rel_data else None
        return data

    @classmethod
    async def select(cls, **kwargs) -> List[Any]:
        async with sessionmanager.session() as session:
            query = select(cls)
            relationships = []
            for name, attr in cls.__dict__.items():
                if isinstance(attr, InstrumentedAttribute) and hasattr(attr.property, 'direction'):
                    relationships.append(name)
                    query = query.options(joinedload(getattr(cls, name)))
            for attr, value in kwargs.items():
                query = query.where(getattr(cls, attr) == value)
            result = await session.execute(query)
            instances = result.unique().scalars().all()
            return [instance.dump(relationships) for instance in instances]

    @classmethod
    async def insert(cls, **kwargs) -> Dict:
        async with sessionmanager.session() as session:
            obj = cls(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj.dump()

    @classmethod
    async def update(cls, values: Dict[str, Any], **kwargs) -> None:
        async with sessionmanager.session() as session:
            query = sqlalchemy_update(cls).where(
                *(getattr(cls, attr) == value for attr, value in kwargs.items())
            ).values(**values)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **kwargs) -> None:
        async with sessionmanager.session() as session:
            query = sqlalchemy_delete(cls).where(
                *(getattr(cls, attr) == value for attr, value in kwargs.items())
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, values: Dict[str, Any], **kwargs) -> None:
        async with sessionmanager.session() as session:
            query = sqlalchemy_update(cls).where(
                *(getattr(cls, attr) == value for attr, value in kwargs.items())
            ).values(**values)
            await session.execute(query)
            await session.commit()
""",
            "migration.py": """
from yoyo import read_migrations
from yoyo import get_backend
from configs import sync_db_url
import os
from typing import List


def find_migrations_dirs() -> List[str]:
    root_dir = os.getcwd()
    found_paths = list()
    for root, dirs, _ in os.walk(root_dir):
        if "migrations" in dirs and "python" not in root:
            print(root)
            found_paths.append(os.path.join(root, "migrations"))
    return found_paths


def apply_migrations(database_uri, migrations_path):
    backend = get_backend(database_uri)
    migrations = read_migrations(migrations_path)

    with backend.lock():
        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))


def run():
    # Check if the migrations directory exists
    migrations_dirs = find_migrations_dirs()
    try:
        # Apply migrations if the directory exists
        for migration_path in migrations_dirs:
            apply_migrations(sync_db_url, migration_path)
    except Exception as e:
        raise Exception(f"Couldn't apply the migrations, {e}")
""",
            "migrations": {
                "0001_define_tables.py": '''from yoyo import step

steps = [
    step(
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR,
            password VARCHAR,
            active BOOLEAN
        );

        """,
        """
        DROP TABLE users;
        """
    )
]
''',
                "0002_define_domains.py": '''from yoyo import step
__depends__ = {"0001_define_tables"}
steps = [
    step(
        """
        CREATE TABLE dns (
            id SERIAL PRIMARY KEY,
            url VARCHAR NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        DROP TABLE dns
        """
    )
]
'''
            },
            "tables": {
                "user.py": '''from src.db.core_orm import BaseORM
from sqlalchemy.dialects.postgresql import VARCHAR, BOOLEAN
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, Integer


class Users(BaseORM):
    __tablename__ = "users"
    name = mapped_column(VARCHAR, nullable=False)
    email = mapped_column(VARCHAR)
    password = mapped_column(VARCHAR)
    active = mapped_column(BOOLEAN)
    dns = relationship("Dns", back_populates="user",
                       cascade="all, delete-orphan")


class Dns(BaseORM):
    __tablename__ = "dns"
    url = mapped_column(VARCHAR, nullable=False)
    user_id = mapped_column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)

    user = relationship("Users", back_populates="dns")
'''
            }
        },
        "middleware": {
            "jwt_middleware.py": '''from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from fastapi import HTTPException, status
from starlette.responses import Response
from src.common.jwt_token import validate_token
from rich import print
from configs import ALLOWED_PATHS


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in ALLOWED_PATHS:
            response = await call_next(request)
        else:
            try:
                token = request.headers.get('Authorization')
                if token:
                    token = token.split(' ')[1]
                    user = await validate_token(token=token)
                    request.state.user = user
                    response = await call_next(request)
                    # return response
                else:
                    raise HTTPException(
                        status_code=401,
                        detail="Mising Token"
                    )
            except HTTPException as exc:
                response = JSONResponse(
                    status_code=exc.status_code, content={"detail": exc.detail}
                )
        return response
''',
            "logging_middleware.py": """import json
import os
import uuid
from pythonjsonlogger import jsonlogger
from logging.config import dictConfig
import logging
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        body = await request.body()

        # Log the request
        self.logger.info("Request received", extra={
            'type': 'api-request',
            'method': request.method,
            'url': str(request.url),
            'body': body.decode('utf-8'),
            'timestamp': datetime.utcnow().isoformat()
        })

        # Next middleware or route handler
        response = await call_next(request)

        # Log the response
        self.logger.info("Response sent", extra={
            'type': 'api-response',
            'status_code': response.status_code,
            'timestamp': datetime.utcnow().isoformat()
        })

        return response


# Custom JSON encoder which enforces standard ISO 8601 format, UUID format


class ModelJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


class LogFilter(logging.Filter):
    def __init__(self, service=None, instance=None):
        self.service = service
        self.instance = instance

    def filter(self, record):
        record.service = self.service
        record.instance = self.instance
        return True


class JsonLogFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Add timestamp field with default : now
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().isoformat()

        # Add level field
        log_record['level'] = record.levelname

        # Add type field for internal logs
        if not log_record.get('type'):
            log_record['type'] = 'internal'

# Configure logging


def configure_logging(level='DEBUG', service=None, instance=None):
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            '()': JsonLogFormatter,
            'format': '%(timestamp)s %(level)s %(service)s %(instance)s %(type)s %(message)s',
            'json_encoder': ModelJsonEncoder
        }},
        'filters': {'default': {
            '()': LogFilter,
            'service': service,
            'instance': instance
        }},
        'handlers': {'default_handler': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['default'],
            'formatter': 'default'
        }},
        'root': {
            'level': level,
            'handlers': ['default_handler']
        }
    })
"""
        }
    },
    ".vscode": {
        "launch.json": """{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "App debug",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "envFile": "${workspaceFolder}/.env",
            "console": "integratedTerminal"
        }
    ]
}"""
    }
}
