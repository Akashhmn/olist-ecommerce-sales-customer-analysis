# Data Cleaning Strategy

## Orders
- Convert timestamp columns to datetime.
- Check order status values.
- Preserve meaningful missing delivery dates.

## Order Items
- Convert shipping date to datetime.
- Validate price and freight values.
- Check for invalid negative values.

## Order Payments
- Do not remove duplicate order_id values.
- Multiple payment records per order can be valid.
- Aggregate at the appropriate level during analysis.

## Products
- Preserve meaningful missing product attributes.
- Do not replace missing dimensions or category values with 0 without justification.

## Order Reviews
- Keep review scores.
- Do not artificially fill missing review comments.

## Geolocation
- Exclude from core analysis because it is large and contains substantial duplicate data.

## General Principle
Missing values will be handled according to their business meaning rather than automatically removed or replaced.