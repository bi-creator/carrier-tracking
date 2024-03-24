from fastapi import FastAPI,Response, status,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime,timedelta
from pydantic import BaseModel
from dbfun import createuser,getuser,createshipment,updateshipementtracking,getshipmenttracking
from alljwt import authenticate_user,create_access_token,verify_access_token
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="asendia/gettoken")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

class signup(BaseModel):
    username:str
    email:str
    phone:str
    address:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class getquote(BaseModel):
    pickup:str
    drop:str
    weight_in_kg:int


class user(BaseModel):
    username:str
    password:str


class shipment(BaseModel):
    pickup:str
    drop:str
    weight_in_kg:int
    sender_name:str
    receiver_name:str
    package_length:int
    package_width:int
    package_height:int
    package_description:str



@app.post('/asendia/singup')
def singup(user:signup):
    createuser(user.username,user.email,user.phone,user.address,user.password)
    return {"status":"User Created"}



@app.post("/asendia/gettoken")
def login_for_access_token(user:user):
    userpass=getuser(user.username)
    isuser = authenticate_user(userpass['password'], user.password)
    if not isuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post('/asendia/getQuote')
def getQuote(quote:getquote,token: str = Depends(oauth2_scheme)):
    # verify token
    payload=verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    geolocator = Nominatim(user_agent="myapp")
    location1 = geolocator.geocode(quote.pickup)
    location2 = geolocator.geocode(quote.drop)
    coord1 = (location1.latitude, location1.longitude)
    coord2 = (location2.latitude, location2.longitude)
    distance = geodesic(coord1, coord2).kilometers
    rate= (distance*2)*quote.weight_in_kg
    rate=round(rate)
    returnpbj={
        "rate":f"₹{rate}",
        "pickup":quote.pickup,
        "drop":quote.drop,
        "weight_in_kg":quote.weight_in_kg,
        "distance_in_KM":round(distance,2)
        }
    return returnpbj



@app.post('/asendia/createShipment')
def createShipment(shipment:shipment,token: str = Depends(oauth2_scheme)):
    payload=verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    geolocator = Nominatim(user_agent="myapp")
    location1 = geolocator.geocode(shipment.pickup)
    location2 = geolocator.geocode(shipment.drop)
    coord1 = (location1.latitude, location1.longitude)
    coord2 = (location2.latitude, location2.longitude)
    distance = geodesic(coord1, coord2).kilometers
    rate= (distance*2)*shipment.weight_in_kg
    rate=round(rate)
    insertobj={
        "rate":rate,
        "pickup":shipment.pickup,
        "drop":shipment.drop,
        "weight_in_kg":shipment.weight_in_kg,
        "distance_in_KM":round(distance,2),
        "sender_name":shipment.sender_name,
        "receiver_name":shipment.receiver_name,
        "package_length":shipment.package_length,
        "package_width":shipment.package_width,
        "package_height":shipment.package_height,
        "package_description":shipment.package_description,
        "estimated_delivery_date":f"{(datetime.now()+timedelta(days=3)).strftime('%Y-%m-%d')}"
        }
    print(insertobj)
    shipment_id=createshipment(insertobj)
    updateshipementtracking(shipment_id,shipment.pickup)
    return {
        "shipment_id":shipment_id,
        "rate":f"₹{rate}",
        "pickup":shipment.pickup,
        "drop":shipment.drop,
        "weight_in_kg":shipment.weight_in_kg,
        "distance_in_KM":round(distance,2),
        "sender_name":shipment.sender_name,
        "receiver_name":shipment.receiver_name,
        "package_length":shipment.package_length,
        "package_width":shipment.package_width,
        "package_height":shipment.package_height,
        "package_description":shipment.package_description,
        "estimated_delivery_date":f"{datetime.now()+timedelta(days=3)}"
    }
    


@app.get('/asendia/getshipmenttracking/{shipment_id}')
def getshipmenttrackingapi(shipment_id:int,token: str = Depends(oauth2_scheme)):
    payload=verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return getshipmenttracking(shipment_id)
