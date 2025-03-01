start :
	@docker build -t controller .
	@docker-compose up -d

stop:
	@docker-compose down
