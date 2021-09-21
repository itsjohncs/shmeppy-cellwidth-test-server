#!/usr/bin/env bash

set -eu
shopt -s failglob

SCRIPT_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"

set -o allexport
# shellcheck source=env
source "$SCRIPT_DIR/env"
set +o allexport

if [[ $# != 1 ]]; then
	echo "USAGE: $0 TARGET" 2>&1
	exit 1
fi

case $1 in
	server)
		"$SCRIPT_DIR/venv/bin/flask" run \
			--reload \
			--eager-loading \
			--port "$FLASK_PORT" \
			--host "$FLASK_HOST"
		;;

	init-db)
		"$SCRIPT_DIR/venv/bin/python3" -c \
			'import app; app.db.drop_all(); app.db.create_all(); app.sync_to_upload_directory()'
		;;

	lint)
		find "$SCRIPT_DIR" -name 'venv' -prune -o -name '*.sh' -print0 \
			| xargs -0 -t shellcheck -x --shell=bash
		find "$SCRIPT_DIR" -name 'venv' -prune -o -name '*.py' -print0 \
			| xargs -0 -t "$SCRIPT_DIR/venv/bin/pylint" \
				--rcfile "$SCRIPT_DIR/.pylintrc"
		;;

	*)
		echo "Unknown target $1" 1>&2
esac
