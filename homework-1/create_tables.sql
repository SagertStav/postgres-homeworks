create table customers
    (customer_id varchar(5) primary key,
	   company_name varchar(200) not null,
       contact_name  varchar(200)
		);
	
create table employees
    (employee_id bigserial primary key,
	   first_name varchar(200) not null,
	   last_name  varchar(200),
	   title varchar(200),
	    birth_date date,
		notes text				
		);
	
create table orders
    (order_id  bigserial primary key,
	 customer_id varchar[5] references customers(customer_id)  ON DELETE CASCADE,
	 employee_id int8  references employees(employee_id) ON DELETE CASCADE, 
	 order_date date,
	 ship_city varchar(100)	   
		)	