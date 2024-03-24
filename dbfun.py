import psycopg2
import datetime
from psycopg2.extras import RealDictCursor
from alljwt import get_password_hash
conn = psycopg2.connect(database = "carrier", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "manjith",
                        port = 5432)



def getuser(username):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"SELECT password FROM customers WHERE customer_name='{username}'")
    user=cur.fetchone()
    return user    

def getuserID(username):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"SELECT customer_id FROM customers WHERE customer_name='{username}'")
    user=cur.fetchone()
    return user['customer_id']

def createuser(username,email,phone,address,password):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"INSERT INTO customers(customer_name,customer_email,customer_phone,customer_address,password) VALUES ('{username}','{email}','{phone}','{address}','{get_password_hash(password)}')")
    conn.commit()
    cur.close()


def createshipment(shipment):
    sender_id=getuserID(shipment["sender_name"])
    receiver_id=getuserID(shipment["receiver_name"])
    cur = conn.cursor(cursor_factory=RealDictCursor)
    sql=f"""
    INSERT INTO shipments(pickup,drop,weight_in_kg,sender_id,receiver_id,package_length,package_width,package_height,package_description,estimated_time,estimated_cost_in_rupes) VALUES (
                '{shipment["pickup"]}',
                '{shipment["drop"]}',
                '{shipment["weight_in_kg"]}',
                '{sender_id}',
                '{receiver_id}',
                '{shipment["package_length"]}',
                '{shipment["package_width"]}',
                '{shipment["package_height"]}',
                '{shipment["package_description"]}',
                '{shipment["estimated_delivery_date"]}',
                '{shipment["rate"]}'
                ) RETURNING shipment_id
                """

    cur.execute(sql)
    conn.commit()
    shipment_id=cur.fetchone()
    cur.close()
    return shipment_id['shipment_id']



def getfreedriver():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"SELECT driver_id FROM drivers WHERE driver_status='free'")
    driver=cur.fetchone()
    return driver['driver_id']


def updateshipementtracking(shipment_id,location):
    driver_id=getfreedriver()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    sql=f"""
    INSERT INTO shipmenttracking(shipment_id,driver_id,status_update,location,update_time) VALUES (
                '{shipment_id}',
                '{driver_id}',
                'onway',
                '{location}',
                '{datetime.datetime.now()}'
                )
                """
    cur.execute(sql)
    conn.commit()
    cur.close()




def getshipmenttracking(shipment_id):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    sql=f"""
    SELECT st.shipment_id,
(select customer_name from customers 
where customer_id= sp.sender_id) as sender,
(select customer_name from customers 
where customer_id= sp.receiver_id) as receiver,
dr.driver_name,
dr.driver_license_number,
dr.driver_phone,
dr.driver_vehicle_plate,
sp.pickup,
sp.drop,
sp.estimated_cost_in_rupes,
sp.estimated_time as estimated_delivery_date,
st.location as current_location
FROM shipmenttracking st
join drivers dr on st.driver_id=dr.driver_id
join shipments sp ON sp.shipment_id = st.shipment_id
WHERE st.shipment_id='{shipment_id}'
    """
    cur.execute(sql)
    shipment=cur.fetchone()
    return shipment
    