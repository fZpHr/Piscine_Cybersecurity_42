IMAGE_NAME = ft_onion_image
CONTAINER_NAME = ft_onion_container

all:
	@echo "  __ _                  _             "
	@echo " / _| |_     ___  _ __ (_) ___  _ __  "
	@echo "| |_| __|   / _ \| '_ \| |/ _ \| '_ \ "
	@echo "|  _| |_   | (_) | | | | | (_) | | | |"
	@echo "|_|  \__|___\___/|_| |_|_|\___/|_| |_|"
	@echo "       |_____|                        "
	@docker build -t $(IMAGE_NAME) .
	@docker run -d -p 8042:80 -p 4242:4242 --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	-@docker stop $(CONTAINER_NAME)

ls:
	@docker ps
	@docker images
	@docker volume ls
	@docker network ls

clean:
	-@docker stop $(CONTAINER_NAME)
	-@docker system prune -f
	-@docker volume prune -f
	-@docker network prune -f
	-@docker image rm $(IMAGE_NAME)

re: stop clean all


.PHONY: start stop ls clean all
