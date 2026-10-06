DROP TABLE IF EXISTS orders;
CREATE TABLE orders (order_id UInt64, customer String, total Float64, day Date) ENGINE = MergeTree PARTITION BY toYYYYMM(day) ORDER BY (customer, day);
INSERT INTO orders VALUES (1,'ana',10,'2026-01-05'),(2,'ana',20,'2026-01-06'),(3,'bo',5,'2026-02-01');
DROP TABLE IF EXISTS revenue_by_customer;
CREATE TABLE revenue_by_customer (customer String, revenue AggregateFunction(sum, Float64)) ENGINE = AggregatingMergeTree ORDER BY customer;
INSERT INTO revenue_by_customer SELECT customer, sumState(total) FROM orders GROUP BY customer;
SELECT customer, sumMerge(revenue) AS revenue FROM revenue_by_customer GROUP BY customer ORDER BY customer FORMAT TSV;
