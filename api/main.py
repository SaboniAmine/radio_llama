from api.config import Settings
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAccessTokenInfo, FiefAsync
from fief_client.integrations.fastapi import FiefAuth

settings = Settings()

fief = FiefAsync(  
    settings.fief_domain,
    settings.fief_client_id,
    settings.fief_client_secret,
)

scheme = OAuth2AuthorizationCodeBearer(  
    settings.fief_domain+"/authorize",  
    settings.fief_domain+"/api/token",  
    scopes={"openid": "openid", "offline_access": "offline_access"},
    auto_error=False,  
)

auth = FiefAuth(fief, scheme)  

app = FastAPI()

print(settings.fief_domain)


@app.get("/user")
async def get_user(
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),  
):
    return access_token_info