from typing import Dict
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import subprocess


source_untokenized_path = "/apps/Gargantua/corpus_to_align/source_language_corpus_untokenized/text.txt"
source_tokenized_path = "/apps/Gargantua/corpus_to_align/source_language_corpus_tokenized/text.txt"
target_untokenized_path = "/apps/Gargantua/corpus_to_align/target_language_corpus_untokenized/text.txt"
target_tokenized_path = "/apps/Gargantua/corpus_to_align/target_language_corpus_tokenized/text.txt"

cwd = "/apps/Gargantua"
clean_cmd = "./clean.sh"
prepare_filesystem_cmd = "./prepare-filesystem.sh"
prepare_data_cmd = "./prepare-data.sh"
sentence_aligner_cwd = "/apps/Gargantua/src"
sentence_aligner_cmd = "./sentence-aligner"
output_path_source = "/apps/Gargantua/src/output_data_aligned/aligned_sentences_source_language.txt"
output_path_target = "/apps/Gargantua/src/output_data_aligned/aligned_sentences_target_language.txt"
output_path_info = "/apps/Gargantua/src/output_data_aligned/info.txt"
output_path = "/apps/Gargantua/src/output_data_aligned/"


def write_files(source_untokenized: str, source_tokenized: str, target_untokenized: str, target_tokenized: str) -> None:
    for filename, content in [
        (source_untokenized_path, source_untokenized),
        (source_tokenized_path, source_tokenized),
        (target_untokenized_path, target_untokenized),
        (target_tokenized_path, target_tokenized),
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


class InputData(BaseModel):
    source_tokenized: str
    source_untokenized: str
    target_tokenized: str
    target_untokenized: str


async def prepare_filesystem():
    subprocess.run(clean_cmd, cwd=cwd)
    subprocess.run(prepare_filesystem_cmd, cwd=cwd)


@app.on_event("startup")
async def startup():
    await prepare_filesystem()
    

@app.post("/")
async def align_text(data: InputData, background_tasks: BackgroundTasks):  # async in order to be blocking for the file access to work
    try:
        write_files(data.source_untokenized, data.source_tokenized, data.target_untokenized, data.target_tokenized)
        
        subprocess.run(prepare_data_cmd, cwd=cwd)
        subprocess.run(sentence_aligner_cmd, cwd=sentence_aligner_cwd)

        result = read_files()
        
        background_tasks.add_task(prepare_filesystem)

        return result
    except FileNotFoundError:
        raise HTTPException(
            status_code=400, detail="Processing did not finish; possibly because of invalid input data."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during processing: " + str(e)) from e
