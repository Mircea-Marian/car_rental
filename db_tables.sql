create table hr.appUsers (
    uname VARCHAR2(15) NOT NULL,
    passwd VARCHAR2(15) NOT NULL,
    credit_card_code VARCHAR2(19) NOT NULL,
    telephone_number VARCHAR2(10) NOT NULL,
    constraint appUsers_pk primary key (uname)
);
insert into APPUSERS (uname, passwd, credit_card_code, telephone_number)
	values ('Alice', '1234', '4556-4479-0709-2848', '0703366589');
insert into APPUSERS (uname, passwd, credit_card_code, telephone_number)
	values ('Bob', '4321', '3793-175381-68940', '0762428779');
insert into APPUSERS (uname, passwd, credit_card_code, telephone_number)
	values ('Eve', 'praduitoare', '5462-0244-1390-1166', '0215720897');

create table hr.cars_details (
	type_id VARCHAR2(3) NOT NULL,
    Brand VARCHAR2(30) NOT NULL,
    Model VARCHAR2(30) NOT NULL,
    fuel_type VARCHAR2(8) NOT NULL,
    number_of_doors VARCHAR2(1) NOT NULL,
    car_type VARCHAR2(10) NOT NULL,
    constraint cars_details_pk primary key (type_id)
);
insert into cars_details (Brand, Model, fuel_type, number_of_doors, car_type, type_id)
	values ('Tesla', 'Model X', 'Electric', '4', 'SUV', 'yMG');
insert into cars_details (Brand, Model, fuel_type, number_of_doors, car_type, type_id)
	values ('Dacia', 'Logan', 'Gas', '4', 'Family', '7hN');
insert into cars_details (Brand, Model, fuel_type, number_of_doors, car_type, type_id)
	values ('Dacia', 'Logan', 'Diesel', '4', 'Family', 'tOi');
insert into cars_details (Brand, Model, fuel_type, number_of_doors, car_type, type_id)
	values ('Smart', 'ForTwo', 'Diesel', '2', 'Two Seater', 'Qw0');
insert into cars_details (Brand, Model, fuel_type, number_of_doors, car_type, type_id)
	values ('Smart', 'ForFour', 'Diesel', '2', 'Family', 'CpO');
insert into cars_details (Brand, Model, fuel_type, number_of_doors, car_type, type_id)
	values ('Smart', 'ForFour', 'Diesel', '4', 'Family', 'vOf');

create table hr.available_cars(
	plate_number VARCHAR2(9) NOT NULL,
    type_id VARCHAR2(3) NOT NULL,
	end_city VARCHAR2(15) DEFAULT 'Bucharest',
	end_street VARCHAR2(30) DEFAULT 'Intrarea Matei Corvin',
	end_number NUMBER DEFAULT 1,
	price_per_hour NUMBER NOT NULL,
	constraint available_cars_pk primary key (plate_number),
	CONSTRAINT available_cars_fk
    	FOREIGN KEY (type_id)
    	REFERENCES hr.cars_details(type_id)
);
insert into available_cars (plate_number, type_id, price_per_hour)
	values ('B 123 GIW', 'Qw0', 17.0); --Smart For Two
insert into available_cars (plate_number, type_id, price_per_hour)
	values ('B 123 BMT', '7hN', 16.7); --Dacia Logan
insert into available_cars (plate_number, type_id, price_per_hour)
	values ('B 123 LTJ', '7hN', 16.7); --Dacia Logan
insert into available_cars (plate_number, type_id, price_per_hour)
	values ('B 123 ATI', 'yMG', 66.7); --Tesla model X
insert into available_cars (plate_number, type_id, price_per_hour)
	values ('B 123 CUH', 'tOi', 16.7); --Dacia Logan
insert into available_cars (plate_number, type_id, price_per_hour)
	values ('B 123 QLC', 'CpO', 18.9); -- Smart for 4
insert into available_cars (plate_number, type_id, price_per_hour)
	values ('B 123 XON', 'vOf', 18.9); -- Smart for 4

create table hr.reservations(
	reservation_id VARCHAR2(20) NOT NULL,
	start_date DATE NOT NULL,
	start_city VARCHAR2(15) NOT NULL,
	end_date DATE NOT NULL,
	end_city VARCHAR2(15) NOT NULL,
	end_street VARCHAR2(30) NOT NULL,
	end_number NUMBER NOT NULL,
	plate_number VARCHAR2(9) NOT NULL,
	constraint reservations_pk primary key (reservation_id),
	CONSTRAINT reservations_fk
    	FOREIGN KEY (plate_number)
    	REFERENCES hr.available_cars(plate_number)
);

create table hr.statistics(
	type_id VARCHAR2(3) NOT NULL,
	last_year number NOT NULL,
	last_year_revenue NUMBER NOT NULL,
    interiorQ number DEFAULT 5,
    exteriorQ number DEFAULT 5,
    engineQ number DEFAULT 5,
    revNo number DEFAULT 1,
	CONSTRAINT statistics_fk
    	FOREIGN KEY (type_id)
    	REFERENCES hr.cars_details(type_id)
);