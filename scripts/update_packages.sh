sudo apt update
sudo apt upgrade
sudo apt install ffmpeg
poetry run python -m pip install --upgrade pip
poetry run pip install --upgrade langchain llama_index
poetry install
poetry shell
