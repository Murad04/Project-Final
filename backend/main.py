from fastapi import FastAPI, Depends, HTTPException
from typing import List
from . import schemas, database
from .recommender_recbole import get_recommender
from fastapi.middleware.cors import CORSMiddleware

# This application uses `pyodbc` connections (provided by `backend.database.get_db`) instead of SQLAlchemy.

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency is provided by `database.get_db` (pyodbc connection)
def get_db():
    yield from database.get_db()


@app.on_event("startup")
def load_recbole():
    try:
        # attempt to load recbole recommender (may be slow or require installed recbole/torch)
        app.state.recbole = get_recommender()
    except Exception:
        app.state.recbole = None


# No LightFM startup loading; we'll use SQL-based popularity recommendations or RecBole externally

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db=Depends(get_db)):
    conn = db
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", user.email)
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_hashed_password = user.password + "notreallyhashed"
    # Insert and return inserted id using OUTPUT
    cursor.execute(
        "INSERT INTO users (email, hashed_password, is_active) OUTPUT INSERTED.id VALUES (?,?,?)",
        user.email,
        fake_hashed_password,
        1,
    )
    row = cursor.fetchone()
    conn.commit()
    user_id = int(row[0]) if row else None
    return {"id": user_id, "email": user.email, "is_active": True, "orders": []}

@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    conn = db
    cursor = conn.cursor()
    # OFFSET/FETCH requires ORDER BY in SQL Server
    cursor.execute(
        "SELECT id, name, description, price, image_url, category FROM products ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY",
        skip,
        limit,
    )
    rows = cursor.fetchall()
    results = []
    for r in rows:
        results.append(
            {
                "id": int(r[0]),
                "name": r[1],
                "description": r[2],
                "price": float(r[3]) if r[3] is not None else None,
                "image_url": r[4],
                "category": r[5],
            }
        )
    return results

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db=Depends(get_db)):
    conn = db
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, description, price, image_url, category) OUTPUT INSERTED.id VALUES (?,?,?,?,?)",
        product.name,
        product.description,
        product.price,
        product.image_url,
        product.category,
    )
    row = cursor.fetchone()
    conn.commit()
    prod_id = int(row[0]) if row else None
    return {
        "id": prod_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "image_url": product.image_url,
        "category": product.category,
    }

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, user_id: int, db=Depends(get_db)):
    conn = db
    cursor = conn.cursor()
    # Insert order and get id and created_at
    cursor.execute(
        "INSERT INTO orders (user_id, created_at) OUTPUT INSERTED.id, INSERTED.created_at VALUES (?, SYSUTCDATETIME())",
        user_id,
    )
    row = cursor.fetchone()
    order_id = int(row[0]) if row else None
    created_at = row[1] if row else None
    # Insert order items
    for item in order.items:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?,?,?)",
            order_id,
            item.product_id,
            item.quantity,
        )
    conn.commit()
    items_out = [{"product_id": it.product_id, "quantity": it.quantity} for it in order.items]
    return {"id": order_id, "created_at": created_at, "items": items_out}

@app.get("/recommendations/{user_id}", response_model=List[schemas.Product])
def get_recommendations(user_id: int, db=Depends(get_db)):
    conn = db
    cursor = conn.cursor()
    rec = getattr(app.state, 'recbole', None)
    if rec:
        try:
            item_ids = rec.recommend_for_user(str(user_id), k=5)
            if item_ids:
                # Try to fetch product rows by integer ids first
                try:
                    ids_int = [int(x) for x in item_ids]
                    placeholders = ','.join('?' for _ in ids_int)
                    sql = f"SELECT id, name, description, price, image_url, category FROM products WHERE id IN ({placeholders})"
                    cursor.execute(sql, *ids_int)
                    rows = cursor.fetchall()
                    # preserve order
                    row_map = {int(r[0]): r for r in rows}
                    rows = [row_map[i] for i in ids_int if i in row_map]
                except ValueError:
                    placeholders = ','.join('?' for _ in item_ids)
                    sql = f"SELECT id, name, description, price, image_url, category FROM products WHERE CAST(id AS NVARCHAR(100)) IN ({placeholders})"
                    cursor.execute(sql, *item_ids)
                    rows = cursor.fetchall()
                results = []
                for r in rows:
                    results.append(
                        {
                            "id": int(r[0]),
                            "name": r[1],
                            "description": r[2],
                            "price": float(r[3]) if r[3] is not None else None,
                            "image_url": r[4],
                            "category": r[5],
                        }
                    )
                return results
        except Exception:
            # fall back to popularity
            pass

    # Popularity-based fallback
    try:
        cursor.execute(
            "SELECT TOP 10 p.id, p.name, p.description, p.price, p.image_url, p.category, COUNT(oi.product_id) AS cnt "
            "FROM products p LEFT JOIN order_items oi ON oi.product_id = p.id "
            "GROUP BY p.id, p.name, p.description, p.price, p.image_url, p.category "
            "ORDER BY cnt DESC"
        )
        rows = cursor.fetchall()
    except Exception:
        cursor.execute(
            "SELECT TOP 5 id, name, description, price, image_url, category FROM products ORDER BY NEWID()"
        )
        rows = cursor.fetchall()
    results = []
    for r in rows[:5]:
        results.append(
            {
                "id": int(r[0]),
                "name": r[1],
                "description": r[2],
                "price": float(r[3]) if r[3] is not None else None,
                "image_url": r[4],
                "category": r[5],
            }
        )
    return results


# ML-specific endpoints removed (switching to RecBole for ML training/inference)
