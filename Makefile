
.PHONY: install
install:
	poetry install

.PHONY: run
run:
	python willow/manage.py runserver
