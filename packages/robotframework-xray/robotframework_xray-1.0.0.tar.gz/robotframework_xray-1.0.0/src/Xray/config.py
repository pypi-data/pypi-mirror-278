import os
from os.path import join
from dotenv import load_dotenv

class Config:
    def get(value: str, environment: str = 'DEV'):
        load_dotenv(join(os.path.abspath(os.curdir), '.env'))
        environment = os.getenv('ENVIRONMENT', environment)
        return os.getenv(f'{environment}.{value}')
    
    def env():
        load_dotenv(join(os.path.abspath(os.curdir), '.env'))
        return os.getenv('ENVIRONMENT', 'DEV')
    
    def mode():
        load_dotenv(join(os.path.abspath(os.curdir), '.env'))
        return os.getenv('MODE', 'ALL')
    
    def project_key():
        return os.getenv('PROJECT_KEY', Config.get('PROJECT.KEY'))
    
    def xray_api():
        return os.getenv('XRAY_API', Config.get('XRAY.API'))
    
    def xray_client_id():
        return os.getenv('XRAY_CLIENT_ID', Config.get('XRAY.CLIENT.ID'))
    
    def xray_client_secret():
        return os.getenv('XRAY_CLIENT_SECRET', Config.get('XRAY.CLIENT.SECRET'))