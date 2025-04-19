#get Refresh Token
import os
from dotenv import load_dotenv

from spotify_func.MesFonctions_Spotify import get_current_token

load_dotenv()

load_dotenv()
CLIENT_ID = os.getenv("SP_PUB_KEY")
CLIENT_SECRET = os.getenv("SP_PRIV_KEY")

get_current_token()