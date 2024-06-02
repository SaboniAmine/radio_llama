from llamapi.domain.program import Program


class ProgramGenerationService:
    def __init__(self, program_repository):
        self.program_repository = program_repository

    def generate_program(self):
        return Program(self.formulaire)
