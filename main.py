from fastapi import Response, Request, FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from db import select, insert, update, delete
import jwt
import time
import uvicorn

class JWTBearer(HTTPBearer):
	def __init__(self, auto_error: bool = True):
		super(JWTBearer, self).__init__(auto_error=auto_error)

	async def __call__(self, request: Request):
		credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
		if credentials:
			if not credentials.scheme == "Bearer":
				raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
			if not self.verify_jwt(credentials.credentials):
				raise HTTPException(status_code=403, detail="Invalid token or expired token.")
			return credentials.credentials
		else:
			raise HTTPException(status_code=403, detail="Invalid authorization code.")

	def verify_jwt(self, jwtoken: str):
		isTokenValid: bool = False
		try:
			payload = decodeJWT(jwtoken)
		except:
			payload = None
		if payload:
			isTokenValid = True
		return isTokenValid

JWT_SECRET = "DES424"
JWT_ALGORITHM = "HS256"

def signJWT(user_id: int, username: str):
	payload = {"user_id": user_id, "username": username, "expires": time.time() + 1800}
	token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
	return {"token": token}

def decodeJWT(token: str):
	try:
		decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
		return decoded_token if decoded_token["expires"] >= time.time() else None
	except:
		return {}

#schema
class userLoginSchema(BaseModel):
	username: str
	password: str

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.post("/user/login")
async def post_login(user: userLoginSchema):
	try: id, password = select('UserID, password', 'USERS', 'username="'+user.username+'"')[0]
	except: raise HTTPException(status_code=401, detail="Username is invalid")
	if password == user.password:
		return signJWT(id, user.username)
	return {"error": "wrong login details"}

@app.post("/file", status_code=201, dependencies=[Depends(JWTBearer())])
async def post_file(files: UploadFile = File(...), token: str = Depends(JWTBearer())):
	username = decodeJWT(token)['username']
	user_id = decodeJWT(token)['user_id']
	data = files.file.read()
	path = "files/"+username+"/"+str(time.time())+"_"+files.filename
	f = open(path, "wb")
	f.write(data)
	f.close()
	insert("files", "NAME, TYPE, PATH, UserID", "'"+files.filename+"', '"+files.content_type+"', '"+path+"', "+str(user_id))
	return {"result": "file uploaded"}

@app.get("/file", dependencies=[Depends(JWTBearer())])
def get_files(token: str = Depends(JWTBearer())):
	data = select("FileID, name", "files", "userID = "+str(decodeJWT(token)['user_id']))
	return data

@app.get("/file/{id}")
def download_file(id: int):
	data = select("path, name, type, userID", "files", "FileID = "+str(id))
	return FileResponse(path=data[0][0], filename=data[0][1], media_type=data[0][2])

@app.delete("/file/{id}", dependencies=[Depends(JWTBearer())])
def delete_file(id: int, token: str = Depends(JWTBearer())):
	user_id = decodeJWT(token)['user_id']
	delete("files", "userID="+str(user_id)+" and fileID="+str(id))
	return {"result": "File deleted"}

@app.get("/user/me", dependencies=[Depends(JWTBearer())])
def get_user(token: str = Depends(JWTBearer()))	:
	username = decodeJWT(token)['username']
	return {"username": username}
app.mount("/", StaticFiles(directory="web"), name="web")