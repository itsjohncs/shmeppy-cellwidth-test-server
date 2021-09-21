.PHONY: start-wsgi-app init-db lint

start-wsgi-app:
	cd server && ./venv/bin/flask run --reload --eager-loading

init-db:
	cd server && ./venv/bin/python3 -c 'import app; app.db.drop_all(); app.db.create_all(); app.sync_to_upload_directory()'

lint:
	find . -name 'venv' -prune -o -name '*.sh' -print0 | xargs -0 -t shellcheck --shell=bash
	./venv/bin/pylint --rcfile ./.pylintrc *.py
