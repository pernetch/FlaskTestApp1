import secrets 
import os

key = secrets.token_hex(16)
print(key)

chemin = os.path.dirname(__file__)

print(os.path.join(chemin, 'config.py'))