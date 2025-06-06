import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(root / 'backend'))
from llm import Llm

output_path = root / 'model_ids.json'
with open(output_path, 'w') as f:
    json.dump([model.value for model in Llm], f, indent=2)
