select * from billboard bill
join (select bill.id_billboard as id_b, ak.kolvo - count(id_ordering_line) as razn from billboard bill
        join ordering_line ol on ol.id_billb = bill.id_billboard
        join (select id_billb as id_b, count(id_billb) as kolvo
                from ordering_line
                group by id_billb) ak on bill.id_billboard=ak.id_b
        where ('$year_e' < year_beg_rent)
        or ('$year_b' > year_end_rent)
        or ('$year_e' = year_beg_rent and '$month_e' < month_beg_rent)
        or ('$year_b' = year_end_rent and '$month_b' > month_end_rent)
        group by bill.id_billboard) vd on vd.id_b = bill.id_billboard
where razn = 0;
and bill.city='$city'
and bill.direction='$direction'