CREATE OR REPLACE PACKAGE proj_bd2 AS

    TYPE myRecord IS RECORD(
        plate_number VARCHAR2(9),
        Brand VARCHAR2(30),
        Model VARCHAR2(30),
        fuel_type VARCHAR2(8),
        number_of_doors VARCHAR2(1),
        car_type VARCHAR2(10),
        price number
       );

    TYPE myTable IS TABLE OF myRecord;

    TYPE tokens IS TABLE of VARCHAR2(30);

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
    RETURN SYS_REFCURSOR;

    PROCEDURE mySplit(
            string_to_split IN VARCHAR2,
            delimiter IN VARCHAR2,
            array_of_tokens OUT tokens
    );

    FUNCTION get_statistics RETURN SYS_REFCURSOR;

    FUNCTION get_car_details RETURN SYS_REFCURSOR;

    PROCEDURE close_cursor(c IN SYS_REFCURSOR);

    FUNCTION checkCredentials(user IN VARCHAR2, pass IN VARCHAR2)
    return NUMBER;

    FUNCTION containsString(list IN tokens, el IN VARCHAR2) return NUMBER;

    function manageReservation(
         choice in varchar2,
         p_start_date in date,
         p_start_city in VARCHAR2,
         p_end_date in date,
         p_end_city in varchar2,
         p_end_street in varchar2,
         p_end_number in number
     ) return varchar2;

    function getRandResID(v_length number) return varchar2;

    PROCEDURE updateStatistics(
        idRes in varchar2,
        intQ in number,
        extQ in number,
        engQ in number
    );

END;