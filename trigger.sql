create or replace trigger fill_stats
	before insert on reservations for each row
declare
	type_id_var VARCHAR2(3);
	flag number := 0;
	pph number;
	newRevenue number;
begin

	select
		ac.type_id,
		ac.price_per_hour
	into
		type_id_var,
		pph
	from
		available_cars ac
	where
		:new.plate_number = ac.plate_number;

	select
		count(*)
	into
		flag
	from
		statistics st
	where
		st.type_id = type_id_var;

	newRevenue := 24 * (:new.end_date - :new.start_date) * pph;

	if flag = 0 then
		insert into statistics (type_id, last_year, last_year_revenue)
			values(type_id_var, 1, newRevenue);
	else
		update statistics st set st.last_year = st.last_year + 1,
			st.last_year_revenue = st.last_year_revenue + newRevenue where
			st.type_id = type_id_var;
    end if;

end;