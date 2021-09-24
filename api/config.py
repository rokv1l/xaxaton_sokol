import os

db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_username = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

sensors_data_path = os.getenv('SENSORS_DATA_PATH')

gh_url = os.getenv('GRAPHHOPPER_URL')
