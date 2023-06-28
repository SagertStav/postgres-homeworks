"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import pathlib
from pathlib import Path
with psycopg2.connect('host=localhost dbname=north user=postgres  password=Sagert') as conn:
    with conn.cursor() as cur:
        conn.autocommit = True
        cur.execute('DROP TABLE customers, employees, orders')

        cur.execute('''
           create table if NOT EXISTS customers 
               (customer_id varchar primary key,
	            company_name varchar(200) not null,
                contact_name  varchar(200));

           create table if NOT EXISTS employees 
               (employee_id bigserial primary key,
	            first_name varchar(200) not null,
	            last_name  varchar(200),
	            title varchar(200),
	            birth_date date,
		        notes text);

           create table if NOT EXISTS orders 
               (order_id  int primary key,
	            customer_id varchar references customers(customer_id),
	            employee_id int8  references employees(employee_id), 
	            order_date date,
	            ship_city varchar(100)	);''')

        cur.execute('TRUNCATE TABLE customers, employees, orders') #полная очистка НЕ УДАЛЕННых таблиц тоже возможна
        for d in ['customers','employees', 'orders']:
            cur.execute(f'DELETE from {d}')  #вариант удаления ВСЕХ ЗАПИСЕЙ ТАБЛИЦЫ тоже работает
            conn.commit()

         #вставим данные из таблиц *_data.csv :
            copy_sql = f"COPY {d} FROM STDIN WITH CSV HEADER DELIMITER ',' QUOTE '\"' ESCAPE '\\' NULL AS 'null'"
            with open(Path(pathlib.Path.cwd(), '', '',
                           f'homework-1\\north_data\{d}_data.csv'), mode='r', encoding='utf-8') as csv_file:  # errors='ignore' ?
                cur.copy_expert(copy_sql, csv_file)
            conn.commit()


            cur.execute(f'select * from {d}')
            for row in cur:
                print(row)
            print(cur.rowcount)

