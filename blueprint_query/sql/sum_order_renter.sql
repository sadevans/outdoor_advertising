select id_rent, sum(total_cost) from ordering
where year(registration_date) = '$input_year'
group by id_rent;