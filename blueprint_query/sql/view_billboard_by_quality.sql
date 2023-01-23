select id_billboard, billb_size, direction, address, cost
from billboard
where quality_indicator = '$input_quality'