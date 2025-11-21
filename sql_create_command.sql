-- Create database if not exists
IF DB_ID(N'sql_app') IS NULL
BEGIN
    CREATE DATABASE [sql_app];
END
GO

USE [sql_app];
GO

CREATE TABLE dbo.users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(320) NOT NULL UNIQUE,
    hashed_password NVARCHAR(256) NOT NULL,
    is_active BIT NOT NULL DEFAULT (1)
);

CREATE TABLE dbo.products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NULL,
    description NVARCHAR(MAX) NULL,
    price DECIMAL(10,2) NULL,
    image_url NVARCHAR(1024) NULL,
    category NVARCHAR(128) NULL
);

CREATE TABLE dbo.orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_orders_users FOREIGN KEY (user_id) REFERENCES dbo.users(id)
);

CREATE TABLE dbo.order_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    CONSTRAINT FK_orderitems_orders FOREIGN KEY (order_id) REFERENCES dbo.orders(id),
    CONSTRAINT FK_orderitems_products FOREIGN KEY (product_id) REFERENCES dbo.products(id)
);

-- Indexes (mirrors SQLAlchemy index=True)
CREATE INDEX IX_users_email ON dbo.users(email);
CREATE INDEX IX_products_name ON dbo.products(name);
CREATE INDEX IX_products_category ON dbo.products(category);
CREATE INDEX IX_orders_user_id ON dbo.orders(user_id);
CREATE INDEX IX_order_items_order_id ON dbo.order_items(order_id);

-- Optional sample inserts (uncomment to use)
-- INSERT INTO dbo.users (email, hashed_password) VALUES (N'alice@example.com', N'hash1');
-- INSERT INTO dbo/products (name, description, price, image_url, category) VALUES (N'Sample', N'Desc', 9.99, N'', N'misc');
-- INSERT INTO dbo.orders (user_id) VALUES (1);
-- INSERT INTO dbo.order_items (order_id, product_id, quantity) VALUES (1, 1, 2);
GO