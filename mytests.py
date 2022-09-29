period = '202201'
year = period[:-2]
created_month = period[-2:]
date_created = '{}-{}-01'.format(year, created_month)
print("year:{} <=> month:{}".format(year, created_month))
print(date_created)
