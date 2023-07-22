import csv


def aggs_list_to_csv(aggs_list, csv_file):
    # csv header
    fieldnames = ['time', 'open', 'close', 'high', 'low', 'volume']

    # csv data
    rows = list(map(lambda agg_i: agg_i.to_csv_map(), aggs_list))

    write_to_csv_file(csv_file, fieldnames, rows)


def create_EPS_announcements_to_price_change_csv(result_map, csv_file):
    fieldnames = ['reported_date', 'surprise_percentage', 'surprise', 'estimated_EPS', 'reported_EPS',
                  'fiscal_date_ending', 'percentage_change']
    # csv data
    rows = []
    for key in result_map.keys():
        csv_map = result_map[key][0].to_csv_map()
        csv_map['percentage_change'] = str(result_map[key][1])
        rows.append(csv_map)
    write_to_csv_file(csv_file, fieldnames, rows)


def write_to_csv_file(csv_file, field_names, rows):
    with open(csv_file, 'w+', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)

