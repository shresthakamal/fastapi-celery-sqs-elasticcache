local:
	docker-compose -f docker-compose.local.yml up --build

worker:
	docker-compose -f docker-compose.worker.yml up --build

localstack:
	docker-compose -f docker-compose-localstack.yml up --build


clean:
	docker-compose -f docker-compose.local.yml down -v
	docker-compose -f docker-compose-localstack.yml down -v
	docker-compose -f docker-compose.worker.yml down -v