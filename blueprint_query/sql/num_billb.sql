select id_billb from ordering_line
join ordering using(id_ordering)
join renter using(id_rent)
where renter.surname = '$input_surname' and month(registration_date) = '$input_month' and year(registration_date) = '$input_year'
group by id_billb