create or replace package body proj_bd2 as

    FUNCTION checkCredentials(user IN VARCHAR2, pass IN VARCHAR2)
    return NUMBER
    IS
        no NUMBER(1) := 0;
    begin
        select
            count(*)
        into
            no
        from
            APPUSERS
        where
            UNAME = user
            and PASSWD = pass;
        return no;
    end checkCredentials;

    FUNCTION get_ups(
        p_start_date IN DATE,
        p_start_city In VARCHAR2,
        p_end_date IN DATE,
        p_Brand IN VARCHAR2,
        p_Model IN VARCHAR2,
        p_fuel_type IN VARCHAR2,
        p_number_of_doors IN VARCHAR2,
        p_car_type IN VARCHAR2
        )
        RETURN SYS_REFCURSOR as
            rez myTable := myTable();
            kontor number := 1;
            flag number;
            my_cursor SYS_REFCURSOR;
            brands_list tokens;
            models_list tokens;
            fuels_list tokens;
            car_types tokens;
        begin
            mySplit(p_Brand, ';', brands_list);
            mySplit(p_Model, ';', models_list);
            mySplit(p_fuel_type, ';', fuels_list);
            mySplit(p_car_type, ';', car_types);

            for row in (
                select
                    ac.plate_number pn,
                    cd.Brand br,
                    cd.Model mm,
                    cd.fuel_type ft,
                    cd.number_of_doors nod,
                    cd.car_type ct,
                    ac.price_per_hour pph
                from
                    available_cars ac,
                    cars_details cd
                where
                    ac.type_id = cd.type_id
            ) loop
                    select
                        count(*)
                    into
                        flag
                    from
                        reservations
                    where
                        plate_number = row.pn
                        and p_start_date not between start_date and end_date;

                    if flag = 0 then

                        if
                            (brands_list.count > 0 and containsString(brands_list, row.br) = 0)
                            or (models_list.count > 0 and containsString(models_list, row.mm) = 0)
                            or (fuels_list.count > 0 and containsString(fuels_list, row.ft) = 0)
                            or (car_types.count > 0 and containsString(car_types, row.ct) = 0)
                            or (p_number_of_doors != 'Any' and row.nod != p_number_of_doors)
                        then
                            continue;
                        end if;

                        rez.extend(1);

                        rez(kontor).plate_number := row.pn;
                        rez(kontor).Brand := row.br;
                        rez(kontor).Model := row.mm;
                        rez(kontor).fuel_type := row.ft;
                        rez(kontor).number_of_doors := row.nod;
                        rez(kontor).car_type := row.ct;
                        rez(kontor).price := row.pph;

                        kontor := kontor + 1;
                    end if;
            end loop;
            open my_cursor for select * from table(rez);
            return my_cursor;
        end get_ups;

    PROCEDURE close_cursor(c IN SYS_REFCURSOR) as
    begin
        close c;
    end close_cursor;

    FUNCTION get_statistics
    RETURN SYS_REFCURSOR
    AS
      my_cursor SYS_REFCURSOR;
    BEGIN
      OPEN my_cursor FOR SELECT
        cd.BRAND , cd.model, ST.LAST_YEAR, round(ST.interiorQ/st.revNo, 2),
        round(ST.exteriorQ/st.revNo, 2), round(ST.engineQ/st.revNo, 2)
        FROM STATISTICS ST natural join cars_details cd;
      RETURN my_cursor;
    END get_statistics;

    FUNCTION get_car_details
    RETURN SYS_REFCURSOR
    AS
      my_cursor SYS_REFCURSOR;
    BEGIN
      OPEN my_cursor FOR SELECT Brand, Model, fuel_type, number_of_doors, car_type from cars_details;
      RETURN my_cursor;
    END get_car_details;


    PROCEDURE mySplit(
            string_to_split IN VARCHAR2,
            delimiter IN VARCHAR2,
            array_of_tokens OUT tokens
        ) as
        inputStringLen NUMBER := LENGTH(string_to_split);
        lastMark NUMBER := 0;
        currentPos NUMBER := 1;
        kontor NUMBER := 1;
    begin
        array_of_tokens := tokens();

        if inputStringLen > 0 then
            loop
                currentPos := INSTR(string_to_split, delimiter, lastMark + 1);
                if currentPos = 0 then
                    array_of_tokens.extend(1);
                    array_of_tokens(kontor) := SUBSTR(
                        string_to_split,
                        lastMark + 1,
                        inputStringLen - lastMark
                    );
                    kontor := kontor + 1;
                    EXIT;
                ELSIF currentPos = inputStringLen then
                    array_of_tokens.extend(1);
                    array_of_tokens(kontor) := SUBSTR(
                        string_to_split,
                        lastMark + 1,
                        inputStringLen - lastMark - 1
                    );
                    kontor := kontor + 1;
                    EXIT;
                end if;

                array_of_tokens.extend(1);
                array_of_tokens(kontor) := SUBSTR(
                    string_to_split,
                    lastMark + 1,
                    currentPos - lastMark - 1
                );
                kontor := kontor + 1;

                lastMark := currentPos;

            end loop;
        end if;
    end mySplit;

    FUNCTION containsString(list IN tokens, el IN VARCHAR2) return number
    is
    begin
        if list.count = 0 then
            return 0;
        end if;

        for ind in list.first .. list.last loop
            if list(ind) = el then
                return 1;
            end if;
        end loop;

        return 0;
    end;

    function getRandResID(v_length number) return varchar2
    as
        my_str varchar2(20);
    begin
        for i in 1..v_length loop
        my_str := my_str || dbms_random.string(
            case when dbms_random.value(0, 1) < 0.5 then 'l' else 'x' end, 1);
        end loop;
        return my_str;
    end getRandResID;

    function manageReservation(
         choice in varchar2,
         p_start_date in date,
         p_start_city in VARCHAR2,
         p_end_date in date,
         p_end_city in varchar2,
         p_end_street in varchar2,
         p_end_number in number
     ) return varchar2 as
        resID varchar2(20);
        isUnique number;
        flag number;
     begin

        select
            count(*)
        into
            flag
        from
            reservations r
        where
            r.plate_number = choice
            and p_start_date between r.start_date and r.end_date;

        if flag = 0 then
            LOCK TABLE reservations
                IN EXCLUSIVE MODE;
            loop
                resID := getRandResID(20);

                select count(*)
                into isUnique
                from reservations where reservation_id = resID;

                exit when isUnique = 0;
            end loop;

        insert into reservations (reservation_id, start_date, start_city, end_date, end_city, end_street, end_number, plate_number)
            values (
                resID,
                p_start_date,
                p_start_city,
                p_end_date,
                p_end_city,
                p_end_street,
                p_end_number,
                choice
            );
        commit;
        else
            resID := '0';
        end if;

        return resID;
     end manageReservation;

     PROCEDURE updateStatistics(
        idRes in varchar2,
        intQ in number,
        extQ in number,
        engQ in number
    ) AS
        car_code varchar2(3);
    BEGIN
        select
            ac.type_id
        into
            car_code
        from
            available_cars ac,
            reservations r
        where
            r.reservation_id = idRes
            and r.plate_number = ac.plate_number;

        update statistics st
            set st.interiorQ = st.interiorQ + intQ,
            st.exteriorQ = st.exteriorQ + extQ,
            st.engineQ = st.engineQ + engQ,
            st.revNo = st.revNo + 1
        where st.type_id = car_code;

        commit;

    END updateStatistics;

end proj_bd2;