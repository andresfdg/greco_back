from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import *
from ..models.ecommerceModels import *
from ..schemas import *
from ..oauth2 import *
from typing import List


#routers
router = APIRouter()

#create a order an asigned to a gremio
@router.post("/create_new_order")
def create_new_order(payload:OrderCreation,db:Session = Depends(get_db),current_user: int = Depends(get_user)):

    item = db.query(ItemDb).filter(ItemDb.id == payload.item).first()

    quantity = item.quantity_low

    gremio_exist = db.query(GuildDb).filter(GuildDb.item == item.id).first()

   
    new_gremio = GuildDb(item = payload.item, pop_max=quantity)
    db.add(new_gremio)
    db.commit()
    db.refresh(new_gremio)
    new_order = OrderDb(store_id=item.owner_store, discount=5 ,owner_id=current_user.id,gield_id=new_gremio.id  ,**payload.dict())
    db.add(new_gremio)
    db.commit()
    db.refresh(new_gremio)
   
    

   

    return new_order

# get all orders
@router.get("/all_orders")                
def get_all_orders(db:Session = Depends(get_db)):

    orders = db.query(OrderDb).all()
    return orders

#get how many items were buy by all users
@router.get("/total_quantity_item/{id}")
def total_quantity_item(id:int, db:Session = Depends(get_db)):

    cur.execute(f"  SELECT SUM(quantity) FROM orders WHERE item ={str(id)} ")
    count = cur.fetchone()

    return count


#get how many orders exist for a consulted item 
@router.get("/totalitem/{id}")
def total(id:int, db:Session = Depends(get_db)):

    cur.execute(f"  SELECT COUNT(item) FROM orders WHERE item ={str(id)} ")
    count = cur.fetchone()

    return count


@router.get("/prueba/{id}")
def prueba(id:int):

    cur.execute(f"""SELECT * FROM users """)
    user =  cur.fetchall()
    return user
    
#RETURN ALL GIELD AND THEIR ORDERS
@router.get("/join")
def prueba():

    cur.execute(f""" SELECT * FROM orders LEFT JOIN numericalguiel ON orders.gield_id = numericalguiel.id ORDER BY numericalguiel.id """)
    orders = cur.fetchall()

    return orders


@router.get("/userorders")
def get_user_orders(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    orders = db.query(OrderDb).filter(OrderDb.owner_id == current_user.id).all()



    return orders

    


 

