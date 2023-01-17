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

    if not gremio_exist:
        new_gremio = GuildDb(item = payload.item, pop_max=quantity)
        db.add(new_gremio)
        db.commit()
        db.refresh(new_gremio)
        new_order = OrderDb(store_id=item.owner_store, discount=5 ,owner_id=current_user.id,gield_id=new_gremio.id  ,**payload.dict())
        db.add(new_gremio)
        db.commit()
        db.refresh(new_gremio)
    
    if gremio_exist:
        gremio_active = db.query(GuildDb).filter(GuildDb.item == item.id and GuildDb.active == True).first()
        if not gremio_active:
            new_gremio = GuildDb(item = payload.item, pop_max=quantity)
            db.add(new_gremio)
            db.commit()
            db.refresh(new_gremio)    
            new_order = OrderDb(store_id=item.owner_store, discount=5 ,owner_id=current_user.id,gield_id=new_gremio.id  ,**payload.dict())
            db.add(new_order)
            db.commit()
            db.refresh(new_order)

        if gremio_active:
            
            cur.execute(f"""SELECT SUM(quantity) FROM orders WHERE orders.gield_id = {str(gremio_active.id)}""")
            actual_quantity = cur.fetchone()
            actual_quantity = list(actual_quantity.items())

            if(int(actual_quantity[0][1]) + int(payload.quantity) > gremio_active.pop_max):
                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            if(actual_quantity[0][1] + payload.quantity == gremio_active.pop_max):
                gremio_active.active = False
                gremio_active.order_number = gremio_active.order_number + 1
                new_order = OrderDb(store_id=item.owner_store, discount=5 ,owner_id=current_user.id,gield_id=new_gremio.id  ,**payload.dict())
                db.add(new_order)
                db.commit()
                db.refresh(new_order)
    

   

    return "well"

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

    


 

