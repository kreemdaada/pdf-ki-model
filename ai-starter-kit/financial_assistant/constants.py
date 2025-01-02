import datetime
import os
import sys
from uuid import uuid4

import yaml

# Main directories
current_dir = os.path.dirname(os.path.abspath(__file__))
kit_dir = current_dir
repo_dir = os.path.abspath(os.path.join(kit_dir, '..'))
sys.path.append(kit_dir)
sys.path.append(repo_dir)

# Main config file
CONFIG_PATH = os.path.join(kit_dir, 'config.yaml')

# Read config file
with open(CONFIG_PATH, 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)

# Get the llm information
prod_mode = config['prod_mode']

# Initialize SEC EDGAR credentials
if prod_mode or os.getenv('SEC_API_ORGANIZATION') is None or os.getenv('SEC_API_EMAIL') is None:
    os.environ['SEC_API_ORGANIZATION'] = 'SambaNova'
    os.environ['SEC_API_EMAIL'] = f'user_{str(uuid4())}@sambanova_cloud.com'

# Minutes for scheduled cache deletion
EXIT_TIME_DELTA = 30

# Main text processing, RAG, and web scraping constants
MIN_CHUNK_SIZE = 4
MAX_CHUNK_SIZE = 1024
CHUNK_OVERLAP = 256
RETRIEVE_HEADLINES = False
TOP_K = 10
MAX_URLS = 1000

# SambaNova
SAMBANOVA_LOGO = 'https://sambanova.ai/hubfs/logotype_sambanova_orange.png'
SAMBANOVA_ORANGE = (238, 118, 36)

# STOCK INFO
YFINANCE_COLUMNS_JSON = os.path.join(kit_dir, 'streamlit/yfinance_columns.json')

# Define default values for text inputs
DEFAULT_COMPANY_NAME = 'Meta'
DEFAULT_DATAFRAME_NAME = 'income_stmt'
DEFAULT_STOCK_QUERY = 'What is the research and development spending trend for Meta?'
DEFAULT_HISTORICAL_STOCK_PRICE_QUERY = 'Meta close value'
DEFAULT_RAG_QUERY = (
    'Have there been changes in strategy, products, and research for Meta? Can you provide some examples?'
)
DEFAULT_PDF_RAG_QUERY = "What conclusions can we draw about Meta's strategy?"
DEFAULT_START_DATE = datetime.datetime.today().date() - datetime.timedelta(days=365)
DEFAULT_END_DATE = datetime.datetime.today().date()
DEFAULT_FILING_TYPE = '10-K'
DEFAULT_FILING_QUARTER = 0
DEFAULT_FILING_YEAR = datetime.datetime.today().date().year - 1
DEFAULT_PDF_TITLE = 'Financial Report'


# Unit tests
TEST_DIR = os.path.join(kit_dir, 'tests/')
TEST_CACHE_DIR = os.path.join(TEST_DIR, 'cache/')
