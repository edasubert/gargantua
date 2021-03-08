from typing import Dict, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import subprocess


source_untokenized_path = (
    "/apps/Gargantua/corpus_to_align/source_language_corpus_untokenized/text.txt"
)
source_tokenized_path = (
    "/apps/Gargantua/corpus_to_align/source_language_corpus_tokenized/text.txt"
)
target_untokenized_path = (
    "/apps/Gargantua/corpus_to_align/target_language_corpus_untokenized/text.txt"
)
target_tokenized_path = (
    "/apps/Gargantua/corpus_to_align/target_language_corpus_tokenized/text.txt"
)

cwd = "/apps/Gargantua"
clean_cmd = "./clean.sh"
prepare_filesystem_cmd = "./prepare-filesystem.sh"
prepare_data_cmd = "./prepare-data.sh"
sentence_aligner_cwd = "/apps/Gargantua/src"
sentence_aligner_cmd = "./sentence-aligner"
output_path_source = (
    "/apps/Gargantua/src/output_data_aligned/aligned_sentences_source_language.txt"
)
output_path_target = (
    "/apps/Gargantua/src/output_data_aligned/aligned_sentences_target_language.txt"
)
output_path_info = "/apps/Gargantua/src/output_data_aligned/info.txt"
output_path = "/apps/Gargantua/src/output_data_aligned/"


class InputData(BaseModel):
    source_tokenized: str
    source_untokenized: str
    target_tokenized: str
    target_untokenized: str

    class Config:
        schema_extra = {
            "example": {
                "source_tokenized": """Action taken on Parliament 's resolutions : see Minutes\nDocuments received : see Minutes\nWritten statements ( Rule 116 ) : see Minutes\nTexts of agreements forwarded by the Council : see Minutes\nMembership of Parliament : see Minutes\nMembership of committees and delegations : see Minutes\nFuture action in the field of patents ( motions for resolutions tabled ) : see Minutes\nAgenda for next sitting : see Minutes\nClosure of sitting""",
                "source_untokenized": """Action taken on Parliament's resolutions: see Minutes\nDocuments received: see Minutes\nWritten statements (Rule 116): see Minutes\nTexts of agreements forwarded by the Council: see Minutes\nMembership of Parliament: see Minutes\nMembership of committees and delegations: see Minutes\nFuture action in the field of patents (motions for resolutions tabled): see Minutes\nAgenda for next sitting: see Minutes\nClosure of sitting""",
                "target_tokenized": """Následný postup na základě usnesení Parlamentu : viz zápis\nPředložení dokumentů : viz zápis\nPísemná prohlášení ( článek 116 jednacího řádu ) : viz zápis\nTexty smluv dodané Radou : viz zápis\nSložení Parlamentu : viz zápis\nČlenství ve výborech a delegacích : viz zápis\nBudoucí akce v oblasti patentů ( předložené návrhy usnesení ) : viz zápis\nPořad jednání příštího zasedání : viz zápis\nUkončení zasedání""",
                "target_untokenized": """Následný postup na základě usnesení Parlamentu: viz zápis\nPředložení dokumentů: viz zápis\nPísemná prohlášení (článek 116 jednacího řádu): viz zápis\nTexty smluv dodané Radou: viz zápis\nSložení Parlamentu: viz zápis\nČlenství ve výborech a delegacích: viz zápis\nBudoucí akce v oblasti patentů (předložené návrhy usnesení): viz zápis\nPořad jednání příštího zasedání: viz zápis\nUkončení zasedání""",
            },
        }


class OutputData(BaseModel):
    source_language: List[str]
    target_language: List[str]
    pairing: List[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "source_language": [
                    "Action taken on Parliament's resolutions: see Minutes ",
                    "Documents received: see Minutes ",
                    "Written statements (Rule 116): see Minutes ",
                    "Texts of agreements forwarded by the Council: see Minutes ",
                    "Membership of Parliament: see Minutes ",
                    "Membership of committees and delegations: see Minutes ",
                    "Future action in the field of patents (motions for resolutions tabled): see Minutes ",
                    "Agenda for next sitting: see Minutes ",
                    "Closure of sitting ",
                ],
                "target_language": [
                    "Následný postup na základě usnesení Parlamentu: viz zápis ",
                    "Předložení dokumentů: viz zápis ",
                    "Písemná prohlášení (článek 116 jednacího řádu): viz zápis ",
                    "Texty smluv dodané Radou: viz zápis ",
                    "Složení Parlamentu: viz zápis ",
                    "Členství ve výborech a delegacích: viz zápis ",
                    "Budoucí akce v oblasti patentů (předložené návrhy usnesení): viz zápis ",
                    "Pořad jednání příštího zasedání: viz zápis ",
                    "Ukončení zasedání ",
                ],
                "pairing": [
                    ["1", "1"],
                    ["2", "2"],
                    ["3", "3"],
                    ["4", "4"],
                    ["5", "5"],
                    ["6", "6"],
                    ["7", "7"],
                    ["8", "8"],
                    ["9", "9"],
                ],
            },
        }


class Message400(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Processing did not finish; possibly because of invalid input data.",
            },
        }


class Message500(Message400):
    class Config:
        schema_extra = {
            "example": {
                "detail": "Error during processing",
            },
        }


def write_files(input_data: InputData) -> None:
    for filename, content in [
        (source_untokenized_path, input_data.source_untokenized),
        (source_tokenized_path, input_data.source_tokenized),
        (target_untokenized_path, input_data.target_untokenized),
        (target_tokenized_path, input_data.target_tokenized),
    ]:
        with open(filename, "w") as f:
            f.write(content)


def read_files() -> Dict[str, str]:
    result = {}
    for filename, key in [
        (output_path_source, "aligned_sentences_source_language"),
        (output_path_target, "aligned_sentences_target_language"),
        (output_path_info, "info"),
    ]:
        with open(filename, "r") as f:
            result[key] = f.read()
    return result


app = FastAPI()


async def prepare_filesystem():
    subprocess.run(clean_cmd, cwd=cwd)
    subprocess.run(prepare_filesystem_cmd, cwd=cwd)


@app.on_event("startup")
async def startup():
    await prepare_filesystem()


@app.post(
    "/",
    response_model=OutputData,
    responses={
        200: {"model": OutputData},
        400: {"model": Message400},
        500: {"model": Message500},
    },
)
async def align_text(
    data: InputData, background_tasks: BackgroundTasks
):  # async in order to be blocking for the file access to work
    try:
        write_files(data)

        subprocess.run(prepare_data_cmd, cwd=cwd)
        subprocess.run(sentence_aligner_cmd, cwd=sentence_aligner_cwd)

        result = read_files()

        background_tasks.add_task(prepare_filesystem)

        return OutputData(
            source_language=[line for line in result["aligned_sentences_source_language"].split("\n") if line],
            target_language=[line for line in result["aligned_sentences_target_language"].split("\n") if line],
            pairing=[
                line.split("\t")[1:] for line in result["info"].split("\n") if line
            ],
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="Processing did not finish; possibly because of invalid input data.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error during processing: " + str(e)
        ) from e
