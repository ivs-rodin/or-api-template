import os, logging
import io
import shutil

import openpyxl
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse

from knapsack_problem.input import ModelConfig
from knapsack_problem.main import run_model

logger = logging.getLogger("or-api")

app = FastAPI()


@app.post('/create_scenario/')
async def create_scenario(
        tag: str,
        max_cost: int,
        costs_file: UploadFile,
):
    if tag == 'base':
        return {'result': 'error', 'desc': f'Запрещено создавать сценарий с тэгом {tag}'}

    if not costs_file.filename.endswith('.xlsx'):
        return {'result': 'error', 'desc': f'Файл {costs_file.filename} должен быть формата .xlsx'}

    scenario_dir = os.path.join('scenarios', tag)
    if os.path.exists(scenario_dir):
        shutil.rmtree(scenario_dir)
    os.makedirs(scenario_dir)

    f = await costs_file.read()
    xlsx = io.BytesIO(f)
    wb = openpyxl.load_workbook(xlsx)

    config = ModelConfig(
        max_cost=max_cost,
    )

    config.to_json(scenario_dir)
    wb.save(os.path.join(scenario_dir, 'costs.xlsx'))
    return {'result': 'success', 'desc': f'Входные данные для расчета с тэгом {tag} успешно загружены'}


@app.post('/download_scenario/')
async def download_scenario(
        tag: str,
):

    scenario_dir = os.path.join('scenarios', tag)
    if not os.path.exists(scenario_dir):
        return {'result': 'error', 'desc': f'Входные данные с тэгом {tag} не загружены'}

    import zipfile

    tmp_zf_path = os.path.join('scenarios', 'tmp', f'{tag}.zip')
    tmp_zf_data = zipfile.ZipFile(tmp_zf_path, "w")
    for dirname, subdirs, files in os.walk(scenario_dir):
        for filename in files:
            tmp_zf_data.write(os.path.join(dirname, filename), filename)
    tmp_zf_data.close()

    return_data = io.BytesIO()
    with open(tmp_zf_path, 'rb') as fo:
        return_data.write(fo.read())
    return_data.seek(0)

    os.remove(tmp_zf_path)

    return StreamingResponse(return_data, media_type="application/zip",
                             headers={'Content-Disposition': f'attachment; filename="input_{tag}"'})


@app.post('/calculate_scenario/')
async def calculate_scenario(
        tag: str = 'base'
):
    scenario_dir = os.path.join('scenarios', tag)
    if not os.path.exists(scenario_dir):
        return {'result': 'error', 'desc': f'Входные данные с тэгом {tag} не загружены'}

    result = run_model(scenario_dir)
    if not result:
        return {'result': 'error', 'desc': f'Не удалось решить модель'}

    return {'result': 'success', 'desc': result}
