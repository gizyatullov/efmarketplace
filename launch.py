# docker-compose -f deploy/docker-compose.yaml --project-directory . up --build
import os

os.system('poetry run py -m efmarketplace')
