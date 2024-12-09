import os
from typing import Union, Annotated
from fastapi import FastAPI, Request, Header
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabaseClient = create_client(url, key)

app = FastAPI()

@app.get('/create-playlist')
async def index_music(x_access_token: Annotated[str | None, Header()] = None):
    #
    # This is used when a user uploads music tracks and we need to create a playlist
    #
    if not x_access_token:
        return {
            "success": False,
            "message": "Please provide an access token"
        }
    response = supabaseClient.auth.get_user(x_access_token)
    if response is None:
        return { 
            "success": False,
            "message": "Not Authorized"
         }

    try:
        files = supabaseClient.storage.from_(f'music_{response.user.id}').list(
            "",
            {"limit": 100, "offset": 0, "sortBy": {"column": "name", "order": "desc"}},
        )
        return files
    except Exception as e:
        print(e)
        return {
            "success": False,
            "message": "Something went wrong"
        }

# 

@app.get('/get_playlist')
def get_playlist():
    return None


@app.get('/predictions')
async def get_predictions():
    return None