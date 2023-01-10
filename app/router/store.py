from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session
from ..database import *
from ..models.user import *
from ..models.ecommerceModels import *
from ..schemas import *
from ..oauth2 import *
from typing import List



router = APIRouter()

#create a new store
@router.post("/store/create")
def create_item(payload:StoreCreate, db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    print(current_user.type)

    valide_store = db.query(StoreDb).filter(StoreDb.owner == current_user.id).first()
    print(current_user.id)
    if valide_store:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE ,detail=f'cuantas tiendas quieres care verga? ya tienes una!')

    if  current_user.type == 'Store':
        new_store = StoreDb(owner=current_user.id,**payload.dict())
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        print(new_store)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'NO PUEDES METER ESA MONDA')       

    return new_store 
#---------------------------------------------------------------------------------------
# get all stores
@router.get("/allstore")               
def get_store(db:Session = Depends(get_db)):
    #get all users registered in the dataset

    stores = db.query(StoreDb).all()
    
    return stores


@router.get("/onestore")
def onestore(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    store = db.query(StoreDb).filter(StoreDb.id == current_user.id).first()

    return store


@router.get("/allstore")
def get_all_store(db:Session = Depends(get_db), current_user: int = Depends(get_user)):


    stores = db.query(StoreDb).all()

    return stores

@router.get("/allstore/{id}")
def get_all_store(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):


    store = db.query(StoreDb).filter(StoreDb.id == id).first()

    return store

@router.get("/storeitems/{id}")
def get_all_store_items(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    items = db.query(ItemDb).filter(ItemDb.owner_store == id ).all()


    return items   

