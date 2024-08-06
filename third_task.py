import re



table = [{'Columns View': 'SO Number', 'Sort By': '', 'Highlight By': 'equals=S110=rgba(172,86,86,1),equals=S111', 'Condition': 'equals=S110,equals=S111', 'Row Height': '60', 'Lines per page': '25'},
         {'Columns View': 'Client PO', 'Sort By': '', 'Highlight By': 'equals=P110,equals=P111', 'Condition': 'equals=P110', 'Row Height': '', 'Lines per page': ''},
         {'Columns View': 'Terms of Sale', 'Sort By': 'asc', 'Highlight By': 'equals=S110=rgba(172,86,86,1)', 'Condition': '', 'Row Height': '', 'Lines per page': ''}]

websocket_response = {'Client PO': {'index': 'so_list_client_po', 'filter': 'client_po'},
                      'SO Number': {'index': 'so_list_so_number', 'filter': 'so_no'},
                      'Terms of Sale': {'index': 'so_list_terms_of_sale', 'filter': 'term_sale'}}

result = {'columns': [{'index': 'so_list_so_number', 'sort': 0},
                      {'index': 'so_list_client_po', 'sort': 1},
                      {'index': 'so_list_terms_of_sale', 'sort': 2}],
          'order_by': {'direction': 'asc', 'index': 'so_list_terms_of_sale'},
          'conditions_data': {'so_no': [{'type': 'equals', 'value': 'S110'},
                                        {'type': 'equals', 'value': 'S111'}],
                              'client_po': [{'type': 'equals', 'value': 'P110'}]},
          'page_size': '25',
          'row_height': '60',
          'color_conditions': {'so_no':     [{'type': 'equals', 'value': 'S110', 'color': 'rgba(172,86,86,1)'}],
                               'client_po': [{'type': 'equals', 'value': 'S110', 'color': ''}, {'type': 'equals', 'value': 'S111', 'color': ''}],
                               'term_sale': []},
          'module': 'SO'}

base_ws = {'Columns View': 'columns',
               'Sort By': 'order_by',
               'Condition': 'conditions_data',
               'Lines per page': 'page_size',
               'Row Height': 'row_height',
               'Highlight By': 'color_conditions'}


def split_color_by_comma(condition_str):
    split_regex = re.compile(r',(?![^()]*\))')
    return split_regex.split(condition_str)


def parse_color_data(input_string):
    parts = split_color_by_comma(input_string)
    result = []

    for part in parts:
        subparts = part.split('=')
        item = {'type': subparts[0], 'value': '', 'color': ''}

        if len(subparts) > 1:
            item['value'] = subparts[1]

        if len(subparts) > 2:
            item['color'] = subparts[2]

        result.append(item)

    return result


def parse_table(table):
    res = {}
    color_conditions = {}
    for row in table:
        index = websocket_response[row['Columns View']]['index']
        filter = websocket_response[row['Columns View']]['filter']
        for key, value in row.items():
            if key == 'Columns View':
                ws_value = websocket_response[value]
                if base_ws[key] in res:
                    res[base_ws[key]].append(ws_value)
                else:
                    res[base_ws[key]] = [ws_value]
            elif key == 'Sort By' and value:
                if base_ws[key] in res:
                    res[base_ws[key]].append({'direction': value, 'index': index})
                else:
                    res[base_ws[key]] = [{'direction': value, 'index': index}]
            elif key == 'Condition' and value:
                all_conditions = [x.split('=') for x in value.split(',')]
                if base_ws[key] in res:
                    pass
                    res[base_ws[key]].append({filter: [{'type': data[0], 'value': data[1]} for data in all_conditions]})
                else:
                    res[base_ws[key]] = [{filter: [{'type': data[0], 'value': data[1]} for data in all_conditions]}]
            elif (key == 'Lines per page' or key == 'Row Height') and value:
                res[base_ws[key]] = value
            elif key == 'Highlight By':
                color_conditions[filter] = parse_color_data(value)
                res[key] = color_conditions

    return  res


print(parse_table(table))