from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from database import engine

app = FastAPI(title="Company ERP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Product(BaseModel):
    product_name: str
    category: str
    price: float
    quantity: int


class InventoryItem(BaseModel):
    product_id: int
    warehouse: str
    quantity: int
class UserLogin(BaseModel):
    username: str
    password: str
class SaleItem(BaseModel):
    product_id: int
    quantity: int
    sale_price: float


@app.get("/")
def home():
    return {"message": "Company ERP API is running"}


@app.get("/products")
def get_products():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM products"))
        products = [dict(row._mapping) for row in result]

    return products


@app.post("/products")
def create_product(product: Product):
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO products
                (product_name, category, price, quantity)
                VALUES (:product_name, :category, :price, :quantity)
                RETURNING product_id
            """),
            {
                "product_name": product.product_name,
                "category": product.category,
                "price": product.price,
                "quantity": product.quantity
            }
        )

        product_id = result.scalar()

    return {
        "message": "Product created successfully",
        "product_id": product_id
    }


@app.get("/inventory")
def get_inventory():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    i.inventory_id,
                    p.product_name,
                    i.warehouse,
                    i.quantity
                FROM inventory i
                JOIN products p
                    ON i.product_id = p.product_id
            """)
        )

        inventory = [dict(row._mapping) for row in result]

    return inventory


@app.post("/inventory")
def add_inventory(item: InventoryItem):
    with engine.begin() as connection:

        # Check if this product already exists in this warehouse
        existing = connection.execute(
            text("""
                SELECT inventory_id
                FROM inventory
                WHERE product_id = :product_id
                  AND warehouse = :warehouse
            """),
            {
                "product_id": item.product_id,
                "warehouse": item.warehouse
            }
        ).fetchone()

        if existing:
            # Add to existing stock
            connection.execute(
                text("""
                    UPDATE inventory
                    SET quantity = quantity + :quantity
                    WHERE inventory_id = :inventory_id
                """),
                {
                    "quantity": item.quantity,
                    "inventory_id": existing.inventory_id
                }
            )

            return {
                "message": "Inventory updated successfully",
                "inventory_id": existing.inventory_id
            }

        else:
            # Create new inventory record
            result = connection.execute(
                text("""
                    INSERT INTO inventory
                    (product_id, warehouse, quantity)
                    VALUES (:product_id, :warehouse, :quantity)
                    RETURNING inventory_id
                """),
                {
                    "product_id": item.product_id,
                    "warehouse": item.warehouse,
                    "quantity": item.quantity
                }
            )

            inventory_id = result.scalar()

            return {
                "message": "Inventory added successfully",
                "inventory_id": inventory_id
            }
@app.get("/sales")
def get_sales():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    s.sale_id,
                    p.product_name,
                    s.quantity,
                    s.sale_price,
                    s.sale_date
                FROM sales s
                JOIN products p
                    ON s.product_id = p.product_id
                ORDER BY s.sale_date DESC
            """)
        )

        sales = [dict(row._mapping) for row in result]

    return sales
@app.post("/sales")
def create_sale(sale: SaleItem):
    with engine.begin() as connection:

        # Check inventory
        inventory_result = connection.execute(
            text("""
                SELECT quantity
                FROM inventory
                WHERE product_id = :product_id
                  AND warehouse = 'Main Warehouse'
            """),
            {
                "product_id": sale.product_id
            }
        )

        inventory = inventory_result.fetchone()

        if inventory is None:
            return {"error": "Product not found in inventory"}

        if inventory.quantity < sale.quantity:
            return {"error": "Not enough stock"}

        # Record sale
        sale_result = connection.execute(
            text("""
                INSERT INTO sales
                (product_id, quantity, sale_price)
                VALUES (:product_id, :quantity, :sale_price)
                RETURNING sale_id
            """),
            {
                "product_id": sale.product_id,
                "quantity": sale.quantity,
                "sale_price": sale.sale_price
            }
        )

        sale_id = sale_result.scalar()

        # Reduce inventory
        connection.execute(
            text("""
                UPDATE inventory
                SET quantity = quantity - :quantity
                WHERE product_id = :product_id
                  AND warehouse = 'Main Warehouse'
            """),
            {
                "product_id": sale.product_id,
                "quantity": sale.quantity
            }
        )

    return {
        "message": "Sale created successfully",
        "sale_id": sale_id
    }
@app.post("/login")
def login(user: UserLogin):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT user_id, username, role
                FROM users
                WHERE username = :username
  AND password_hash = :password
            """),
            {
                "username": user.username,
                "password": user.password
            }
        )

        existing_user = result.fetchone()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful",
        "user_id": existing_user.user_id,
        "username": existing_user.username,
        "role": existing_user.role
    }

@app.get("/dashboard")
def get_dashboard():
    with engine.connect() as connection:

        # Total number of products
        product_result = connection.execute(
            text("SELECT COUNT(*) FROM products")
        )
        total_products = product_result.scalar()

        # Total inventory quantity
        inventory_result = connection.execute(
            text("SELECT COALESCE(SUM(quantity), 0) FROM inventory")
        )
        total_inventory = inventory_result.scalar()

        # Total number of sales
        sales_result = connection.execute(
            text("SELECT COUNT(*) FROM sales")
        )
        total_sales = sales_result.scalar()

        # Total sales value
        sales_value_result = connection.execute(
            text("""
                SELECT COALESCE(SUM(quantity * sale_price), 0)
                FROM sales
            """)
        )
        total_sales_value = sales_value_result.scalar()

    return {
        "total_products": total_products,
        "total_inventory": total_inventory,
        "total_sales": total_sales,
        "total_sales_value": total_sales_value
    }