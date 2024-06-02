from contextlib import AbstractContextManager
from typing import Callable, List
from uuid import uuid4

from llamapi.domain.program import Program, CollectionProgram
from llamapi.infra.database.sql_models import Program as SqlModelProgram


class SqlAlchemyRepository:
    def __init__(self, session_factory) -> Callable[..., AbstractContextManager]:
        self.session_factory = session_factory

    def create_program(self, program: CollectionProgram) -> bool:
        with self.session_factory() as session:
            db_program = SqlModelProgram(
                id=uuid4(),
                name=program.name,
                path=program.path
            )
            session.add(db_program)
            session.commit()
            session.refresh(db_program)
            return True if db_program else False

    def list_programs(self) -> List[CollectionProgram]:
        with self.session_factory() as session:
            e = session.query(SqlModelProgram)
            if e is None:
                return []
            programs: List[CollectionProgram] = []
            for program in programs:
                programs.append(CollectionProgram(
                    name=program.name,
                    path=program.path
                ))
            return programs
