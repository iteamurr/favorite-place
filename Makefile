APPLICATION_NAME = favorite_place


.PHONY: run
run: # Run the service.
		poetry run python -m $(APPLICATION_NAME) $(ARGS)


.PHONY: clean
clean: # Clear the directory of unnecessary files.
		poetry run pyclean -v $(APPLICATION_NAME)/


.PHONY: to_db
to_db: # Exec the db.
		docker compose exec mongodb mongosh --username favorite_place_agent --password favorite_place_password


.PHONY: createsuperuser
createsuperuser: # Create superuser.
		@poetry run python $(APPLICATION_NAME)/utils/createsuperuser.py


.PHONY: nice
nice: # Format the code.
		poetry run isort $(APPLICATION_NAME)/ && poetry run black $(APPLICATION_NAME)/


.PHONY: lint
lint: # Lint the code.
		poetry run pylint $(APPLICATION_NAME)/


.PHONY: wow
wow: # Clear the directory of unnecessary files and format the code.
		make clean && make nice


.PHONY: help
help: # Show help for each of the Makefile recipes.
		@grep -E '^[a-zA-Z0-9 -]+:.*#' Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
