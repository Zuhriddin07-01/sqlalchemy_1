from database import Base
from sqlalchemy import Integer, String, DECIMAL, Foreignkey
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Seller(Base) :
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(Integer, primary_key = True , index = True)
    name : Mapped[str] = mapped_column(String(length = 50) , index = True)
    products: Mapped[list["Product"]] = relationship("Product" , back_populates = "seller" , cascade = "all, delete-orphan")



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key = True , index = True)
    name : Mapped[str] = mapped_column(String(length = 100) , index = True)
    description: Mapped[str] = mapped_column(String(length = 500))
    seller_id : Mapped[str] = mapped_column(Foreignkey("sallers.id"))
    seller: Mapped["Seller"] = relationship("seller" , back_populates = "products")
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    order_items  = relationship("OrderItem", back_populates="product")


class Customer(Base):
    id: Mapped[int] = mapped_column(Integer , primary_key = True , index = True)
    first_name : Mapped[String] = mapped_column(String(length = 100) , index = True) 
    last_name : Mapped[String] = mapped_column(String(length = 200), index = True)
    username: Mapped[String] = mapped_column(String(length = 300), index = True)  
    phone: Mapped[String] = mapped_column(String(length = 300) , index = True)
    address : Mapped[String] = mapped_column(String(length = 300) , index = True)
    order_items    = relationship("OrderItem", back_populates="order")

class Order:
    id: Mapped[int] = mapped_column(Integer , primary_key = True , index = True)
    status: Mapped[String] = mapped_column(String(length = 100) , index = True)
    order_namber : Mapped[String] = mapped_column(String(length = 100) , index = True)
    customer_id : Mapped[str] = mapped_column(Foreignkey("customer_id")) 
    status : Mapped[String] = mapped_column(String(length = 100) , index = True)
    product_id: Mapped[str] = mapped_column(Foreignkey("product_id"))
    product = relationship("Product", back_populates="order_items")




