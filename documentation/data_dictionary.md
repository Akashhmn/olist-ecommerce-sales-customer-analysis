# Data Dictionary & Relationship Map

## Core Tables

### Customers
Primary Key: customer_id

### Orders
Primary Key: order_id
Foreign Key: customer_id → Customers

### Order Items
Composite relationship:
order_id → Orders
product_id → Products
seller_id → Sellers

### Products
Primary Key: product_id
Category: product_category_name

### Sellers
Primary Key: seller_id

### Order Payments
Foreign Key: order_id → Orders

### Product Category Translation
Key: product_category_name
Purpose: Translate Portuguese category names into English.

## Main Data Flow

Customers
    ↓
Orders
    ↓
Order Items
    ├── Products
    └── Sellers

Orders
    ↓
Order Payments

Products
    ↓
Category Translation


### Relationship Details  ###

## Primary Key (PK)

A Primary Key uniquely identifies each row in a table.

Examples:
- Customers → `customer_id`
- Orders → `order_id`
- Products → `product_id`
- Sellers → `seller_id`

---

## Foreign Key (FK)

A Foreign Key is a column that references a key in another table and creates a relationship between tables.

Examples:
- Orders.`customer_id` → Customers.`customer_id`
- Order Items.`order_id` → Orders.`order_id`
- Order Items.`product_id` → Products.`product_id`
- Order Items.`seller_id` → Sellers.`seller_id`
- Payments.`order_id` → Orders.`order_id`

---

## Relationship Cardinality

### 1. Customers → Orders
**Cardinality: One-to-Many (1:M)**

One customer can place multiple orders.

`Customers.customer_id` → `Orders.customer_id`

---

### 2. Orders → Order Items
**Cardinality: One-to-Many (1:M)**

One order can contain multiple order items/products.

`Orders.order_id` → `Order Items.order_id`

---

### 3. Products → Order Items
**Cardinality: One-to-Many (1:M)**

One product can appear in many order-item records.

`Products.product_id` → `Order Items.product_id`

---

### 4. Sellers → Order Items
**Cardinality: One-to-Many (1:M)**

One seller can have many order-item records.

`Sellers.seller_id` → `Order Items.seller_id`

---

### 5. Orders → Payments
**Cardinality: One-to-Many (1:M)**

One order can have multiple payment records.

`Orders.order_id` → `Payments.order_id`

This is important because we must not assume that one order always has exactly one payment row.

---

### 6. Products → Category Translation
**Cardinality: Many-to-One (M:1)**

Multiple products can belong to the same product category.

The category translation table provides the English translation for the category name.

---

## Data Grain

Data grain means what **one row represents** in a table.

| Table | One row represents |
|---|---|
| Customers | One customer record |
| Orders | One order |
| Order Items | One item within an order |
| Products | One product |
| Sellers | One seller |
| Payments | One payment record for an order |
| Category Translation | One product category |

Understanding the grain is important before joining tables because different tables can contain multiple rows for the same business entity.