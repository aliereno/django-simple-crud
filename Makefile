install:
	if [ ! -d "$(.venv)" ]; then \
		echo "creating virtualenv"; \
		python3 -m venv ./venv; \
	fi
	source venv/bin/activate; \
	echo "installing requirements"; \
	venv/bin/pip3 install -r requirements.txt; \
	venv/bin/pre-commit install
run:
	python manage.py runserver
test:
	python manage.py test
