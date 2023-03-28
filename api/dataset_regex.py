from mapping_rules.models import *

# columns to map
#dataset_cols = SeriesColumns.objects.first()
# regex definations

# ageset regex
ageset_pattern = r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})"

# gender regex
female_gender_regex = "[r'('][F][r')']"
male_gender_regex = "[r'('][M][r')']"

# TX_CURR
# datim-khis <15  - <1 1-9 10-14
less_15_regex_m_f = "([<]\d+\s+(\w+))"
# datim-khis 15+
less_15_regex_unknown = "([<]\d+\s+(\w+)\s+(\w+))"


# datim-khis 15+
plus_15_m_f = "(\d+[+]\s+(\w+))"

#25+ M|F
plus_25_m_f = "(\d+[+]\s+(\w+))"

# ....
