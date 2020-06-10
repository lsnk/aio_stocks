import os


DEBUG = False

# DB
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 5432)

DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

DB_NAME = os.environ.get('DB_NAME', 'aio_stocks')

DB_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# Parsing
PARSING_INTERVAL = int(os.environ.get('PARSING_INTERVAL', 10 * 60))  # 10 min
