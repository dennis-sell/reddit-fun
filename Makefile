
.PHONY: install
install:
	poetry install

.PHONY: run
run:
	flask run

.PHONY: clean
clean:
	#rm -r .venv/
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
