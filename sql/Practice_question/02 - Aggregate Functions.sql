-- ==========================================================
-- Module 02 : Aggregate Functions
-- Topic      : COUNT(), SUM(), AVG(), MIN(), MAX(), DISTINCT
-- Difficulty : Easy
-- Database   : TechMart
-- Questions  : 10
-- ==========================================================

-- Q1. Display the total number of customers.

select count(*) from customers;

-- Q2. Display the total number of products.

select count(*) from products;

-- Q3. Display the total revenue generated from all orders.
-- (Hint: Use total_amount from the orders table.)

select sum(total_amount) from orders;

-- Q4. Display the average selling price of all products.

select avg(selling_price) from products;

-- Q5. Display the highest selling price among all products.

select max(selling_price) from products;

-- Q6. Display the lowest selling price among all products.

select min(selling_price) from products;

-- Q7. Display the total quantity of products sold.
-- (Hint: Use the order_items table.)

select sum(quantity) from order_items;

-- Q8. Display the average product rating.
-- (Hint: Use the reviews table.)

select avg(rating) from reviews;

-- Q9. Display the total number of unique cities where customers live.

select distinct(city) from addresses;

-- Q10. Display the total payment received.

select sum(payment_amount) from payments where payment_status ='success';
