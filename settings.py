from decouple import config, Csv


BASE_URL = config('BASE_URL', default='http://localhost:8000')

ADMIN_USERNAME=config('ADMIN_USERNAME')
ADMIN_PASSWORD = config('ADMIN_PASSWORD')

DEMO_USERNAME=config('DEMO_USERNAME')
DEMO_PASSWORD = config('DEMO_PASSWORD')

PROJECT_PATH = config('PROJECT_PATH', default="~/Renthub-Connect")