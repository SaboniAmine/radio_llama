import json
from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from starlette.datastructures import URL
from starlette.responses import FileResponse

from llamapi.container import ServerContainer
from llamapi.domain.program import Program
from llamapi.domain.track import Track
from llamapi.services.program_generation import ProgramGenerationService

router = APIRouter()


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=int,
)
@inject
def upload_playlist(
        playlist_url,
):
    tracklist = []
    with open('filename.json', 'r') as file:
        playlist = json.load(file)
        for track in playlist:
            tracklist.append(
                Track(
                    track_name=track["track_name"],
                    authors=track["authors"],
                    album=track["album"],
                    label=track["label"],
                    first_release_date=track["first_release_date"],
                    disambiguation=track["disambiguation"],
                )
            )
            track.get_music_brainz_metatadata()

    return len(tracklist)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=bool,
)
@inject
def generate_program(
        program: Program,
        programs_service: ProgramGenerationService = Depends(Provide[ServerContainer.programs_service]),
) -> str:

    return programs_service.generate_program(program)


@router.get(
    "/list_radios",
    status_code=status.HTTP_200_OK,
)
@inject
def list_radios(
        programs_service: ProgramGenerationService = Depends(Provide[ServerContainer.programs_service]),
) -> FileResponse:

    return programs_service.get_all_programs()
