import xlsxwriter
from analytics_sdk.utilities import (
    APP_ID,
    APP_DISPLAY_NAME,
    upload_file
)

class ExcelWriter:

    DATA_PER_SHEET_LIMIT = 1000001
    ROW_START = 3
    CONTENT_ROW_START = 0
    def __init__(self, run_id, file_name, app_id):
        self.run_id = run_id
        self.file_name = file_name
        self.app_id = app_id
        self.wb = xlsxwriter.Workbook(self.file_name, {'constant_memory':True, 'nan_inf_to_errors': True})
        self.total_sheet_row_counts = {}
        self.active_sheet_title = ''
        self.sheet_refs = {}
        self.run_params = None


    def create_sheet(self, sheet_title):
        sheet_title = self.get_page_title(sheet_title, 0)
        if sheet_title in self.sheet_refs:
            return self.sheet_refs[sheet_title]
        ws = self.wb.add_worksheet(sheet_title)
        self.sheet_refs[sheet_title] = ws
        # self.add_headers(ws)
        return ws
    
    def get_page_title(self, title, page_no):
        pg_title = ''
        if page_no > 0:
            pg_title = f'.. {page_no}'
        pg_title_len = len(pg_title)
        # remain_len = 30 - pg_title_len
        # TODO:
        remain_len = 29 - pg_title_len
        title = title[0:remain_len]
        title = title + pg_title
        return title
    

    def write_summary_data(self, summary_data):
        ws = self.create_sheet('SUMMARY')
        self.fill_sheet_bg_colors(ws)
        ws.set_column('B:B', 24)
        ws.set_column('C:C', 24)
        # Rendering Run Summary information
        if summary_data is not None and len(summary_data) > 0:
            cell_no = ExcelWriter.ROW_START
            for entry in summary_data:
                ws.write(f'B{cell_no}', entry, self.wb.add_format({'color':'00598B', 'bg_color' : 'eeeeee'}))
                ws.write(f'C{cell_no}', summary_data[entry], self.wb.add_format({'color':'000000', 'bg_color' : 'eeeeee'}))
                cell_no += 1
            if self.run_params and self.run_params is not None and len(self.run_params) > 0:
                opsql_params = None
                if 'opsql_query' in self.run_params:
                    opsql_params = self.run_params['opsql_query']
                if opsql_params is not None:
                    for key in opsql_params.keys():
                        display_name = self.get_display_name(key)
                        display_value = self.get_display_value(opsql_params[key])

                        ws.write(f'B{cell_no}', display_name, self.wb.add_format({'color':'00598B', 'bg_color' : 'eeeeee'}))
                        ws.write(f'C{cell_no}', display_value, self.wb.add_format({'color':'000000', 'bg_color' : 'eeeeee'}))
                        cell_no += 1
        


    def write_glossary_data(self, glossary_data):
        ws = self.create_sheet('GLOSSARY')
        if ws:
            self.fill_sheet_bg_colors(ws)
            data_len = 30
            if glossary_data is not None and len(glossary_data) >= data_len:
                data_len = len(glossary_data)+5
            
            # self.fill_sheet_bg_colors(ws, start_row=1, end_row=data_len)
            ws.set_column('B:B', 50)
            ws.set_column('C:C', 24)

            cell_no = 3
            if glossary_data is not None:
                data = glossary_data
                for key in data.keys():
                    display_name = key
                    display_value = data[key]

                    ws.write(f'B{cell_no}', display_name, self.wb.add_format({'color':'00598B', 'bg_color' : 'eeeeee'}))
                    ws.write(f'C{cell_no}', display_value, self.wb.add_format({'color':'000000', 'bg_color' : 'eeeeee'}))

                    cell_no += 1
    def get_value(self, value):
        if value:
            try:
                value = float(value)
                return value
            except ValueError:
                return value
            except Exception as e:
                return value
        return value

    def render_table(self, title, headers, data, row_start=1, col_start=1):
        column_widths = {}
        if data:
            sheet_count = 1
            ws = self.create_sheet(title)
            #self.add_headers(ws)
            new_title = title
            self.active_sheet_title = title
            if self.active_sheet_title not in self.total_sheet_row_counts:
                self.total_sheet_row_counts[self.active_sheet_title] = 0
            row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
            if new_title in self.total_sheet_row_counts and self.total_sheet_row_counts[new_title] > 0:
                row_no = self.total_sheet_row_counts[new_title]
            for row_delta, _row in enumerate(data):
                if self.total_sheet_row_counts[new_title] >= ExcelWriter.DATA_PER_SHEET_LIMIT:
                    row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
                    new_title = self.get_page_title(title, sheet_count)
                    sheet_count += 1
                    self.active_sheet_title = new_title
                    ws = self.create_sheet(new_title)
                    self.add_headers(ws)
                    if self.active_sheet_title not in self.total_sheet_row_counts:
                        self.total_sheet_row_counts[self.active_sheet_title] = 0
                if row_no == ExcelWriter.CONTENT_ROW_START:
                    # Adding table title here
                    # ws.write_row(row_no-1, 0, [title], self.wb.add_format({'font_color': '00598B', 'bold':True}))
                    ws.write_row(row_no, 0, headers[0], self.wb.add_format({'bold': True, 'bg_color': '#7D92AF', 'font_color':'#FFFFFF', 'border': 2, 'border_color': '#FFFFFF'}))
                    row_no += 1
                for col_delta, val in enumerate(_row):
                    cell_position = xlsxwriter.utility.xl_rowcol_to_cell(row_no, col_delta)
                    bg_color = '#DCE6F1'
                    try:
                        if APP_ID == 'AVAILABILITY-DETAILS':
                            if isinstance(val, str) and 'COLOR-CODE_' in val:
                                vals = val.split('_') #COLOR-CODE_{color_code}_100.0
                                if len(vals) == 3:
                                    val = vals[2]
                                    if vals[1] is not None and len(vals[1]):
                                        bg_color = vals[1]
                        val = self.get_value(val)
                    except Exception as e:
                        print('ExcelWriter: found exception... value is :: ', val)
                        try:
                            val = str(val)
                        except Exception as ex:
                            val = ''
                    ws.write(cell_position, val, self.wb.add_format({'bg_color': bg_color, 'border': 1, 'border_color': '#FFFFFF'}))
                    if col_delta in column_widths:
                        column_widths[col_delta] = max(len(str(val)), column_widths[col_delta])
                    else:
                        column_widths[col_delta] = max(len(str(val)), 8)
                row_no += 1
                self.total_sheet_row_counts[new_title] = row_no
        for col, column_width in column_widths.items():
            col_name = xlsxwriter.utility.xl_col_to_name(col)
            ws.set_column(f'{col_name}:{col_name}', column_width + 2)

    
    def add_headers(self, ws):
        ws.merge_range('A1:A2', '')
        ws.merge_range('B1:Z2', '')
        ws.write('B1', self.app_id.title(), self.wb.add_format({'font_color': '00598B', 'bg_color': 'eeeeee', 'bold':True, 'align':'vcenter'}))
        ws.write('A1', '', self.wb.add_format({'font_color': '00598B', 'bg_color': 'eeeeee'}))


    def fill_sheet_bg_colors(self, ws, start_row=0, end_row=30, fill_type="solid", color="eeeeee"):
        if ws:
            format=self.wb.add_format({'bg_color': color})
            ws.conditional_format(start_row, 0, end_row, 30, {'type': 'blanks', 'format': format})
            # ws.conditional_format(f'A{start_row}:C{end_row}', {'type': 'no_blanks', 'format': format})
            # ws.set_column(0, 30, None, self.wb.add_format({'bg_color': color}))
            # ws.set_row(0, 30, self.wb.add_format({'bg_color': 'eeeeee'}))

    def generate_excel_file(self, form, resp, report_summary_data, reportname, filepath):
        if resp:
            if 'excel-data' in resp:
                excel_data = []
                excel_data.append(
                    {
                        'title': 'SUMMARY',
                        'summary' : 'true',
                        'header': {},
                        'data': report_summary_data
                    }
                )
                if 'sheets' in resp['excel-data']:
                    for sheet in resp['excel-data']['sheets']:
                        excel_data.append(sheet)
                resp['excel-data']['sheets'] = excel_data
                self.render(resp['excel-data'])
                self.wb.close()
                # saving excel file
                excel_url = upload_file(form.get_run_id(), reportname, filepath)
                resp['excel_url'] = excel_url
        return resp

    
    def client_names_ids(self, customer_name):
        names = ''
        client_id = ''
        if customer_name and customer_name is not None:
            for i in customer_name:
                for j in i.items():
                    names+=j[1]['name']
                    client_id+=j[1]['uniqueId']
                    names+=', '
                    client_id+=', '
            names = names.rstrip(', ')
            client_id = client_id.rstrip(', ')
            return names, client_id
        else:
            return names, client_id
        

    def get_display_name(self, key):
        if key == 'filterCriteria':
            return 'Query'
        if key == 'fields':
            return 'Attributes'
        if key == 'groupBy':
            return 'Group By'
        if key == 'soryBy':
            return 'Sort By'
        if key == 'sortByOrder':
            return 'Sort By Order'
        return key


    def get_display_value(self, value):
        if value is None and len(value) <= 0:
            return '-'
        else:
            if isinstance(value, list):
                all_values = ', '.join([val for val in value])
                return all_values
        return value
    
        
    def prepare_report_summary_data(self, run_id, run_summary, tenant_info, user_params, run_start_time, run_completion_time):
        summary_data = {}
        summary_data['App'] = APP_DISPLAY_NAME.replace('-', ' ').title()
        c_name = ''
        if tenant_info is not None and len(tenant_info) > 0:
            result = self.client_names_ids(tenant_info)
            c_name = result[0]
        summary_data['Tenant Name'] = c_name
        summary_data['Run date'] = run_start_time
        summary_data['Completion date'] = run_completion_time
        first_name = run_summary.json()['analysisRun']['createdBy']['firstName']
        last_name = run_summary.json()['analysisRun']['createdBy']['lastName']
        login_name = run_summary.json()['analysisRun']['createdBy']['loginName']
        summary_data['User'] = f'{first_name} {last_name} ({login_name})'
        if user_params is not None:
            for key in user_params.keys():
                summary_data[self.get_display_name(key)] = self.get_display_value(user_params[key])
        return summary_data
    

    def render_metric_table(self, merge_cells, title, headers, data, row_start=1, col_start=1):
        column_widths = {}
        if data:
            sheet_count = 1
            ws = self.create_sheet(title)
            #self.add_headers(ws)
            if merge_cells:
                for merge_cell in merge_cells:
                    ws.merge_range(merge_cell, '')
            new_title = title
            self.active_sheet_title = title
            if self.active_sheet_title not in self.total_sheet_row_counts:
                self.total_sheet_row_counts[self.active_sheet_title] = 0
            row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
            if new_title in self.total_sheet_row_counts and self.total_sheet_row_counts[new_title] > 0:
                row_no = self.total_sheet_row_counts[new_title]
            for row_delta, _row in enumerate(data):
                if self.total_sheet_row_counts[new_title] >= ExcelWriter.DATA_PER_SHEET_LIMIT:
                    row_no = ExcelWriter.CONTENT_ROW_START - 1 + row_start
                    new_title = self.get_page_title(title, sheet_count)
                    sheet_count += 1
                    self.active_sheet_title = new_title
                    ws = self.create_sheet(new_title)
                    self.add_headers(ws)
                    if self.active_sheet_title not in self.total_sheet_row_counts:
                        self.total_sheet_row_counts[self.active_sheet_title] = 0
                if row_no == ExcelWriter.CONTENT_ROW_START:
                    # Adding table title here
                    # ws.write_row(row_no, 0, headers[0], self.wb.add_format({'bold': True, 'border': 1, 'bg_color': '#4F81BD', 'font_color':'#FFFFFF', 'border': 2, 'border_color': '#FFFFFF'}))
                    for header in headers:
                        for col_delta, val in enumerate(header):
                            cell_position = xlsxwriter.utility.xl_rowcol_to_cell(row_no, col_delta)
                            ws.write(cell_position, self.get_value(val), self.wb.add_format({'align': 'center', 'bold': True, 'bg_color': '#7D92AF', 'font_color':'#FFFFFF', 'border': 0, 'border_color': '#FFFFFF'}))
                            if col_delta in column_widths:
                                column_widths[col_delta] = max(len(str(val)), column_widths[col_delta])
                            else:
                                column_widths[col_delta] = max(len(str(val)), 8)
                        row_no += 1
                for col_delta, val in enumerate(_row):
                    cell_position = xlsxwriter.utility.xl_rowcol_to_cell(row_no, col_delta)
                    bg_color = '#DCE6F1'
                    try:
                        val = self.get_value(val)
                    except Exception as e:
                        print('ExcelWriter: found exception... value is :: ', val)
                        try:
                            val = str(val)
                        except Exception as ex:
                            val = ''
                    ws.write(cell_position, val, self.wb.add_format({'bg_color': bg_color, 'border': 1, 'border_color': '#FFFFFF'}))
                    if col_delta in column_widths:
                        column_widths[col_delta] = max(len(str(val)), column_widths[col_delta])
                    else:
                        column_widths[col_delta] = max(len(str(val)), 8)
                row_no += 1
                self.total_sheet_row_counts[new_title] = row_no
        for col, column_width in column_widths.items():
            col_name = xlsxwriter.utility.xl_col_to_name(col)
            ws.set_column(f'{col_name}:{col_name}', column_width + 2)

            

    def add_component(self, component_data, title):
        if component_data:
            if 'type' in component_data:
                if title is None or len(title) <= 0:
                    if 'title' in component_data and component_data['title'] is not None and len(component_data['title']) > 0:
                        title = component_data['title']
                if component_data['type'] == 'table':
                    if title:
                        start_row = 1
                        start_col = 1
                        if 'data' in component_data and len(component_data['data']) > 0:
                            headers = component_data['data'][0:1]
                            data = component_data['data'][1:len(component_data['data'])]
                        if 'start-row' in component_data and 'start-col' in component_data:
                            start_row = component_data['start-row']
                            start_col = component_data['start-col']
                        if 'merge_cells' in component_data:
                            headers = component_data['data'][0:2]
                            data = component_data['data'][2:len(component_data['data'])]
                            self.render_metric_table(component_data['merge_cells'], title, headers, data, start_row, start_col)
                        else:
                            self.render_table(title, headers, data, start_row, start_col)
    

    def render(self, excel_data):
        if excel_data:
            for sheet in excel_data['sheets']:
                if (('title' in sheet and len(sheet['title']) > 0 and sheet['title'].lower() == 'summary') or ('summary' in sheet and sheet['summary'] == 'true')):
                    self.write_summary_data(sheet['data'])
                elif 'documentation' in sheet and sheet['documentation'] == 'true':
                    self.write_glossary_data(sheet['data'])
                else:
                    title = None
                    if 'title' in sheet:
                        title = sheet['title']
                    for component_data in sheet['components']:
                        self.add_component(component_data, title)
