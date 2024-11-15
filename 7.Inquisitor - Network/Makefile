IMAGE_NAME = ftp
IMAGE_NAME1 = victim
CONTAINER_NAME = ftp
CONTAINER_NAME1 = victim

all:
	@echo "▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖ ▗▖ ▗▖▗▄▄▄▖ ▗▄▄▖▗▄▄▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖ "
	@echo "  █  ▐▛▚▖▐▌▐▌ ▐▌ ▐▌ ▐▌  █  ▐▌     █    █ ▐▌ ▐▌▐▌ ▐▌"
	@echo "  █  ▐▌ ▝▜▌▐▌ ▐▌ ▐▌ ▐▌  █   ▝▀▚▖  █    █ ▐▌ ▐▌▐▛▀▚▖"
	@echo "▗▄█▄▖▐▌  ▐▌▐▙▄▟▙▖▝▚▄▞▘▗▄█▄▖▗▄▄▞▘▗▄█▄▖  █ ▝▚▄▞▘▐▌ ▐▌"
												   
	@docker compose -f dockercompose.yml up -d || echo "Docker compose failed, continuing..."
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} {{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $(CONTAINER_NAME) $(CONTAINER_NAME1) | tr '\n' ' '

stop:
	@docker compose -f dockercompose.yml stop

ls:
	@-docker compose -f dockercompose.yml ps
	@docker images
	@docker volume ls
	@docker network ls

info:
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} {{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $(CONTAINER_NAME) $(CONTAINER_NAME1) | tr '\n' ' '

clean:
	@-docker compose -f dockercompose.yml down
	@docker system prune -a -f
	@docker volume prune -f
	@docker network prune -f

re: stop clean all

.PHONY: start stop ls clean all info re
