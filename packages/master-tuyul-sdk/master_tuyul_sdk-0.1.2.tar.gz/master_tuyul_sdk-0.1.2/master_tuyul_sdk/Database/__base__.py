from enum import Enum, auto
import os
from typing import Union
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database

class TypeDatabase(Enum):
    
    ONLINE  = auto()
    OFFLINE = auto()
    MEMORI  = auto()

class Database:

    @property
    def declarative(self) -> DeclarativeMeta:
        return declarative_base()

    class Build:

        FileName: Union[str, None] = None
        PathName: Union[str, None] = None
        Type: Union[TypeDatabase, None] = None

        @classmethod
        def BaseMetaData(cls, declarative: DeclarativeMeta) -> MetaData:
            return declarative.metadata
        
        def __init__(self) -> None:
            if self.Type == TypeDatabase.ONLINE:
                DATABASE_URI = str(os.getenv('DATABASE_URI'))
            else:
                if self.FileName is not None:
                    if self.Type == TypeDatabase.MEMORI:
                        if os.path.exists(self.PathName) is False: os.mkdir(self.PathName)
                        DATABASE_URI = 'sqlite:///{}/{}.sqlite'.format(self.PathName, self.FileName)
                    else:
                        if os.path.exists('Database') is False: os.mkdir('Database')
                        DATABASE_URI = 'sqlite:///Database/{}.sqlite'.format(self.FileName)
                else:
                    raise Exception('No filename provided for the Engine.\nPlease set command Database.Build.run(declarative, Type, PathName, FileName)')
            self.Engine = create_engine(DATABASE_URI, echo=False, pool_pre_ping=True)

        def Connect(self):
            return self.Engine.connect()

        def Session(self) -> Session:
            Session = sessionmaker(bind=self.Engine)
            return Session()

        @staticmethod
        def run(declarative: DeclarativeMeta, Type: TypeDatabase = None, PathName: str = None, FileName: str = None):
            setattr(Database.Build, 'PathName', PathName)
            if FileName is not None:
                setattr(Database.Build, 'FileName', FileName)
            if not Type:
                setattr(Database.Build, 'Type', TypeDatabase.OFFLINE)
            else:
                setattr(Database.Build, 'Type', Type)
            Conn = Database.Build()
            if not database_exists(Conn.Engine.url):
                create_database(Conn.Engine.url)
            Conn.BaseMetaData(declarative).create_all(Conn.Engine)
            return Conn
