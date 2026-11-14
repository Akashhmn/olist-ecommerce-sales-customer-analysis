# Exploratory Data Analysis Notes

## 1. Sales Trends

### Objective
Analyze monthly recorded payment values to identify overall trends, notable changes, and potential patterns over time.

### Metric and Method
- **Date field:** `order_purchase_timestamp`
- **Value field:** `payment_value`
- Payment records were aggregated by `order_id` before being joined with order purchase dates.
- Aggregated payment values were grouped by purchase month.
- The analysis uses recorded payment values; these should not be interpreted as profit.

### Key Observations
1. Monthly payment values generally increased from September 2016 through November 2017.
2. November 2017 recorded the highest monthly payment value in the analyzed output: 1,194,882.80.
3. Monthly payment values remained relatively high during March–May 2018, at approximately 1.15–1.16 million per month.
4. September and October 2018 showed sharply lower recorded values than preceding months.

### Data Limitations
- November 2016 has no monthly record in the analyzed output. It is displayed as a gap rather than being assumed to have zero sales.
- September and October 2018 may represent incomplete periods. Their low values should not be interpreted as a confirmed collapse in sales without further validation.
- The analysis identifies observed patterns but does not establish the causes behind monthly changes.

### Visualization
`visualizations/monthly_sales_trend.png`

### Status
Sales Trends analysis and initial interpretation completed.

## 2. Order Trends

### Objective
Analyze monthly order volume to identify changes and patterns in the number of orders placed over time.

### Method
- *Date field:* order_purchase_timestamp
- *Order identifier:* order_id
- Invalid or missing purchase timestamps were excluded.
- Orders were grouped by purchase month.
- Unique order IDs were counted for each month.

### Key Observations
1. Monthly order volume generally increased from the beginning of the dataset through November 2017.
2. November 2017 recorded the highest observed monthly order count, with 7,544 orders.
3. Order volume fluctuated during 2018 but remained relatively high through August.
4. September 2018 recorded 16 orders and October 2018 recorded 4 orders. These may be incomplete periods and should not be interpreted as confirmed demand declines.
5. November 2016 had no observed monthly record and is displayed as a gap rather than being treated as zero orders.

### Data Limitations
- Missing monthly records are represented as missing values, not zero orders.
- The final months may be incomplete, so direct comparisons with full months may be misleading.
- The analysis identifies observed patterns but does not establish the causes behind changes in order volume.

### Visualization
`visualizations/monthly_order_trend.png`

### Status
Order Trends analysis and initial interpretation completed.

## 3. Category Performance

### Objective
Analyze product categories by total items sold, total orders, total sales value, and average item price to understand differences in category performance.

### Metrics
- **Total Items:** Number of order-item records in each category.
- **Total Orders:** Number of distinct orders containing items from each category.
- **Total Sales Value:** Sum of item prices for each category, excluding freight charges.
- **Average Item Price:** Average item price within each category.

### Key Findings
- Health & Beauty recorded the highest item sales value at 1,258,681.34.
- Watches & Gifts ranked second in sales value at 1,205,005.68.
- Bed & Bath Table recorded the highest number of items sold, with 11,115 items.
- Bed & Bath Table ranked third in sales value at 1,036,988.68.
- Watches & Gifts had the highest average item price among the top 10 sales categories, at 201.14.
- The category with the highest item volume was not the category with the highest sales value.

### Visualizations
1. `visualizations/top_categories_by_sales.png`
2. `visualizations/top_categories_by_items.png`

### Limitations
- Sales value is calculated from item prices and excludes freight charges.
- Sales value is not profit because product costs and other business expenses are not included.
- The analysis describes observed data and does not establish why one category performs better than another.

### Status
Category Performance analysis, visualizations, and initial interpretation completed.

## 4. Customer Behaviour

### Objective
Analyze customer purchasing frequency to understand how many customers placed only one order and how many returned to place additional orders.

### Metrics
- **Total Customers:** Number of distinct customers identified using `customer_unique_id`.
- **One-Time Customers:** Customers who placed exactly one order.
- **Repeat Customers:** Customers who placed more than one order.
- **Average Orders per Customer:** Average number of orders placed by each unique customer.
- **Order Frequency Distribution:** Number and percentage of customers grouped by their total order count.

### Key Findings
- The dataset contains 96,096 unique customers.
- 93,099 customers (96.88%) placed only one order.
- 2,997 customers (3.12%) placed more than one order.
- The average number of orders per customer was approximately 1.03.
- The median and 75th percentile of customer order frequency were both 1.
- The highest observed order frequency was 17 orders by a single customer.
- Among repeat customers, 2,745 customers placed exactly two orders.

### Visualization
- `visualizations/repeat_customer_order_frequency.png`

### Limitations
- Customer purchasing frequency is based on `customer_unique_id`, not `customer_id`, because a customer may have multiple customer records across orders.
- The analysis describes observed purchasing patterns and does not establish why customers did or did not return.
- A low repeat-customer percentage alone does not establish customer dissatisfaction or poor service.

### Status
Customer Behaviour analysis, statistics, visualization, and initial interpretation completed.

## 5. Seller Performance

### Objective
Analyze seller-level performance using order volume, items sold, sales value, and average item price to identify high-performing sellers and understand differences in seller activity.

### Metrics
- **Total Orders:** Number of distinct orders handled by each seller.
- **Total Items:** Number of order-item records associated with each seller.
- **Total Sales Value:** Sum of item prices for each seller.
- **Average Item Price:** Average item price for each seller.

### Key Findings
- The dataset contains 3,095 sellers.
- The highest sales value was recorded by seller `4869f7a5...`, with 229,472.63.
- Seller `4a3ca931...` handled the highest number of orders (1,806) and items (1,987).
- The seller with the highest sales value was not the seller with the highest order or item volume.
- Average seller sales value was 4,391.48, while the median was 821.48.
- Average seller order count was 32.31, while the median was 6.
- These differences indicate that seller performance is unevenly distributed, with a relatively small number of sellers handling substantially higher sales and order volumes.

### Visualization
- `visualizations/top_sellers_by_sales.png`

### Limitations
- Sales value is calculated using item prices and excludes freight charges.
- Sales value is not profit because product costs and other business expenses are not included.
- Seller IDs are used to identify sellers; the analysis does not establish the reasons behind differences in seller performance.
- High sales value does not necessarily indicate higher profitability.

### Status
Seller Performance analysis, descriptive statistics, visualization, and initial interpretation completed.

## 6. Delivery Time Analysis

### Objective
Analyze the time taken to deliver orders and compare actual delivery duration with estimated delivery duration across purchase months.

### Metrics
- **Actual Delivery Days:** Time between purchase timestamp and actual customer delivery timestamp.
- **Estimated Delivery Days:** Time between purchase timestamp and estimated delivery timestamp.
- **Total Orders:** Number of delivered orders with valid purchase, actual delivery, and estimated delivery timestamps.
- **Delivery Difference:** Difference between actual and estimated delivery duration.

### Key Findings
- The analysis included 96,470 delivered orders with valid date information.
- Average actual delivery duration was approximately 12.56 days.
- Average estimated delivery duration was approximately 23.74 days.
- The overall late-delivery rate was 8.11%, based on the delivery status analysis.
- Actual delivery duration was generally lower than estimated delivery duration across most analyzed months.
- February and March 2018 recorded comparatively high average actual delivery durations of 16.95 and 16.30 days, respectively.
- Average actual delivery duration decreased from 11.50 days in April 2018 to 7.73 days in August 2018.
- September 2016 contained only one valid order, making its average actual delivery duration of 54.81 days unsuitable for interpreting a broader monthly trend.
- October 2016 recorded an unusually high average estimated delivery duration of 55.68 days across 265 valid orders.
- November 2016 had no valid observations for this analysis and was therefore absent from the monthly summary.

### Visualization
- `visualizations/monthly_delivery_time_comparison.png`

### Limitations
- Only delivered orders with valid purchase, actual delivery, and estimated delivery timestamps were included.
- Monthly averages should be interpreted alongside the number of valid orders in each month.
- Months with very few observations may not represent typical delivery performance.
- The analysis identifies differences and trends but does not establish the operational reasons behind delivery delays.
- Delivery duration is calculated using elapsed time in fractional days; SQL results using calendar-day differences may vary slightly.

### Status
Delivery Time analysis, descriptive statistics, monthly comparison, visualization, and initial interpretation completed.

## 7. Review Scores Analysis

### Objective
Analyze customer review scores to understand the overall distribution of ratings and identify the proportion of positive and low ratings.

### Metrics
- **Total Reviews:** Number of non-null review scores.
- **Average Review Score:** Mean rating on a scale of 1 to 5.
- **Median Review Score:** Middle value of the review score distribution.
- **Review Score Distribution:** Count and percentage of reviews for each score from 1 to 5.
- **Positive Ratings:** Percentage of reviews with scores of 4 or 5.
- **Low Ratings:** Percentage of reviews with scores of 1 or 2.

### Key Findings
- A total of 99,224 non-null review scores were analyzed.
- The average review score was 4.09 out of 5.
- The median review score was 5.
- Five-star reviews represented the largest share, at 57.78%.
- Four-star reviews accounted for 19.29%.
- Positive ratings (4–5) represented 77.07% of reviews.
- Low ratings (1–2) represented 14.69% of reviews.
- Three-star reviews accounted for 8.24%.

### Visualization
- `visualizations/review_score_distribution.png`

### Limitations
- The analysis includes only non-null review scores.
- Review scores describe submitted customer feedback and do not explain the reasons behind the ratings.
- A high average score does not mean that all customers had a positive experience.
- The analysis does not establish causal relationships between delivery performance and review scores.

### Status
Review Scores analysis, descriptive statistics, visualization, and initial interpretation completed.
## 8. Payment Behaviour Analysis

### Objective
Analyze payment methods to understand transaction volume, recorded payment value, average payment value, and the contribution of each payment method to total payment value.

### Metrics
- **Transaction Count:** Number of payment records for each payment method.
- **Total Payment Value:** Sum of recorded payment values for each payment method.
- **Average Payment Value:** Average recorded payment value per payment record.
- **Payment Value Percentage:** Percentage contribution of each payment method to total recorded payment value.

### Key Findings
- A total of 103,886 payment records were analyzed.
- Credit card accounted for 78.34% of total recorded payment value.
- Boleto accounted for 17.92%.
- Credit card and boleto together represented 96.26% of total payment value.
- Voucher accounted for 2.37%, while debit card accounted for 1.36%.
- Credit card had the highest transaction count, with 76,795 payment records.
- The average payment value was 154.10, while the median was 100.00.
- Three records had an undefined payment type and a recorded payment value of zero.

### Visualization
- `visualizations/payment_method_value_share.png`

### Limitations
- Transaction count represents payment records, not necessarily unique orders.
- One order may contain multiple payment records.
- Payment value represents recorded payment amounts and should not be interpreted as profit.
- The analysis describes recorded payment patterns and does not establish why customers selected a particular payment method.

### Status
Payment Behaviour analysis, descriptive statistics, visualization, and initial interpretation completed.