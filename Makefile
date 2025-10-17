install:
	poetry install

project:
	poetry run project

run:
	poetry run python -m labyrinth_game.main

build:
	poetry build 

publish:
	poetry publish --dry-run 

package-install:
	python3 -m pip install dist/*.whl