import os
import re
from get_web_content import extract_log_from_web
from datetime import datetime, timedelta
from shutil import copyfile
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import parse_xml

MonthMap = {
    "一月 ": "1-", "二月 ": "2-", "三月 ": "3-", "四月 ": "4-",
    "五月 ": "5-", "六月 ": "6-", "七月 ": "7-", "八月 ": "8-",
    "九月 ": "9-", "十月 ": "10-", "十一月 ": "11-", "十二月 ": "12-"
}

YearList = {
"2026年 ","2027年 ","2028年 ","2029年 ","2030年 ","2031年 ","2032年 ","2033年 ","2034年 "
}

name = "倪丹"

def current_year():
    return datetime.today().year

def last_week_weekly_report_name():
    today = datetime.today()
    last_week_start_date = (today - timedelta(days=today.weekday() + 7)).strftime('%y.%m.%d')
    last_week_end_date = (today - timedelta(days=today.weekday() + 3)).strftime('%m.%d')
    return f"{current_year()}/工作周报（{name}{last_week_start_date}-{last_week_end_date}）.doc"
    
def this_week_weekly_report_name():
    today = datetime.today()
    this_week_start_date = (today - timedelta(days=today.weekday())).strftime('%y.%m.%d')
    this_week_end_date = (today + timedelta(days=4-today.weekday())).strftime('%m.%d')
    return f"{current_year()}/工作周报（{name}{this_week_start_date}-{this_week_end_date}）.doc"

def copy_weekly_report(): 
    last_week_filename = last_week_weekly_report_name()
    this_week_filename = this_week_weekly_report_name()
    
    if os.path.exists(last_week_filename):
        copyfile(last_week_filename, this_week_filename)
    else:
        print(f"未找到上周周报: {last_week_filename}")

def clear_cell_content(row_index, col_index):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    
    table = doc.tables[0]
    cell = table.cell(row_index, col_index)
    cell.text = ""
    doc.save(file_path)

def copy_cell_content(src_row_index, src_col_index, dest_row_index, dest_col_index):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    
    table = doc.tables[0]
    src_cell = table.cell(src_row_index, src_col_index)
    dest_cell = table.cell(dest_row_index, dest_col_index)
    
    dest_cell._element.clear_content()
    
    for paragraph in src_cell.paragraphs:
        if paragraph.text.strip():  # 仅复制非空段落
            dest_paragraph = dest_cell.add_paragraph()
            for run in paragraph.runs:
                dest_run = dest_paragraph.add_run(run.text)
                dest_run.bold = run.bold
                dest_run.italic = run.italic
                dest_run.underline = run.underline
                dest_run.font.name = run.font.name
                dest_run.font.size = run.font.size
                dest_run.font.color.rgb = run.font.color.rgb
            
    doc.save(file_path)

def get_cell_content(row_index, col_index, strip_line=True):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    table = doc.tables[0]
    cell = table.cell(row_index, col_index)

    lines = []
    for para in cell.paragraphs:
        txt = para.text
        if strip_line:
            txt = txt.strip()
        lines.append(txt)
    return lines

def last_week_plan_to_this_week_log(row_index, col_index):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    cell = doc.tables[0].cell(row_index, col_index)
    
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            if "计划进度" in run.text:
                run.text = run.text.replace("计划进度", "进度")

    all_text = []
    for paragraph in cell.paragraphs:
        all_text.append(paragraph.text)
    combined = "".join(all_text)

    # 清空单元格所有段落，新建唯一一段
    cell._element.clear_content()
    cell.add_paragraph(combined)
    
    doc.save(file_path)

def update_weekly_report_date():
    today = datetime.today()
    this_week_start_date = (today - timedelta(days=today.weekday())).strftime('%y.%m.%d')
    this_week_end_date = (today + timedelta(days=4-today.weekday())).strftime('%y.%m.%d')
    new_date_range = f"{this_week_start_date} – {this_week_end_date}"
    
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    
    table = doc.tables[0]
    cell = table.cell(1, 1)
    
    paragraph = cell.paragraphs[0]
    run = paragraph.runs[0]
    
    font_name = run.font.name
    font_size = run.font.size
    font_color = run.font.color.rgb
    
    paragraph.clear()
    new_run = paragraph.add_run(new_date_range)
    
    new_run.font.name = font_name
    new_run.font.size = font_size
    new_run.font.color.rgb = font_color
    
    doc.save(file_path)

def add_progress_to_logs(log_list):
    lst = []

    for log in log_list:
        lst.append(log + "，进度100%")

    return lst

def append_this_week_logs(row_index, col_index, log_list):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    cell = doc.tables[0].cell(row_index, col_index)
    
    for log in log_list:
        cell.add_paragraph(log)
    doc.save(file_path)

def is_date_line(line):
    for month_zh, month_num in MonthMap.items():
        if line.startswith(month_num):
            return True

    return False

def is_month_line(line):
    for month_zh, month_num in MonthMap.items():
        if line.startswith(month_zh):
            return True
            
    return False

def extract_month_num(line):
    for month_zh, month_num in MonthMap.items():
        if line.startswith(month_zh):
            return month_num
            
    return ""

def remove_useless_content(web_extracted_text):
    web_extracted_text_copy = web_extracted_text
    for year_str in YearList:
        web_extracted_text_copy = web_extracted_text_copy.replace(year_str, "")

    return web_extracted_text_copy


def add_date_info(web_extracted_text):
    logs = []
    current_month_num = ""
    
    #print("web_extracted_text:")
    #print(web_extracted_text)
    for line in web_extracted_text.split('\n'):
        line = line.strip()
        if is_month_line(line):
            current_month_num = extract_month_num(line)
            logs.append(current_month_num + line.split()[1])
        elif line.isdigit() and current_month_num != "":
            logs.append(current_month_num + line)
        elif current_month_num != "":
            logs.append(line)

    #print("add_date_info:")
    #print(logs)
    return logs

def get_current_week_range():
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())  # 本周的第一天
    end_of_week = start_of_week + timedelta(days=6)  # 本周的最后一天
    return start_of_week, end_of_week

def extract_day_range_logs(logs, start_day, end_day):
    current_week_logs = []
    date = None
    for line in logs:
        line = line.strip()
        if is_date_line(line):
            date = datetime(current_year(), int(line.split('-')[0]), int(line.split('-')[1])).date()
        elif date is not None and start_day <= date <= end_day:
            current_week_logs.append(line[:-2].replace("[B]","")) # strip bug log prefix and hour num
            
    current_week_logs = list(set(current_week_logs)) # remove repeated logs
    current_week_logs.sort()
    #print(current_week_logs)
    return current_week_logs

def extract_current_week_logs(logs):
    start_day, end_day = get_current_week_range()
    log_list = extract_day_range_logs(logs, start_day, end_day)
    #print(log_list)
    return log_list

def trim_project_prefix_logs(log_list):
    pattern = re.compile(r"^(.+?：)\s*(.*)$")
    group_prefix = None
    new_logs = []
    for line in log_list:
        line_stripped = line.strip()
        m = pattern.match(line_stripped)
        if m:
            proj_prefix, content = m.groups()
            if group_prefix is None:
                # 新项目组第一条，原样保留
                group_prefix = proj_prefix
                new_logs.append(line)
            else:
                if proj_prefix == group_prefix:
                    # 同项目，去掉前缀
                    new_logs.append(content)
                else:
                    # 切换新项目，保留本条前缀
                    group_prefix = proj_prefix
                    new_logs.append(line)
        else:
            # 非项目行，重置分组
            group_prefix = None
            new_logs.append(line)
    return new_logs


def add_project_title(row_index, col_index):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    cell = doc.tables[0].cell(row_index, col_index)

    line_list = []
    for paragraph in cell.paragraphs:
        line_list.append(paragraph.text)

    line_list = list(set(line_list)) # remove duplicate line

    line_list.sort()
    line_list = trim_project_prefix_logs(line_list)

    combined = "\n".join(line_list)
    combined = combined.replace("：","：\n")
    line_list = combined.split("\n")

    # 清空单元格所有段落，新建唯一一段
    cell._element.clear_content()

    for line in line_list:
        cell.add_paragraph(line)

    doc.save(file_path)


def bold_project_title(row_index, col_index):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    cell = doc.tables[0].cell(row_index, col_index)

    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            if "：" in run.text:
                run.bold = True

    doc.save(file_path)

def add_new_line_before_project_title(row_index, col_index):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    table = doc.tables[0]
    cell = table.cell(row_index, col_index)

    # 注意：遍历要逆序！正序插入会打乱索引
    paras = list(cell.paragraphs)
    for p in reversed(paras):
        # 判断该段落是否加粗：只要任意一个run是bold就算整行加粗
        has_bold = any(run.bold for run in p.runs)
        if has_bold:
            # 在当前段落前面插入空白段落
            p.insert_paragraph_before("")

    doc.save(file_path)

def remove_cell_first_line(row_index, col_index):
    file_path = this_week_weekly_report_name()
    doc = Document(file_path)
    table = doc.tables[0]
    cell = table.cell(row_index, col_index)

    paras = cell.paragraphs
    if len(paras) > 0:
        # 删除第一个段落节点
        cell._element.remove(paras[0]._element)

    doc.save(file_path)

# main()
copy_weekly_report()
update_weekly_report_date()
clear_cell_content(2,1)
clear_cell_content(3,1)
copy_cell_content(5,1,2,1)
copy_cell_content(2,1,3,1)
clear_cell_content(5,1)
last_week_plan_to_this_week_log(3, 1)
append_this_week_logs(3, 1, add_progress_to_logs(extract_current_week_logs(add_date_info(remove_useless_content(extract_log_from_web())))))
add_project_title(3, 1)
bold_project_title(3, 1)
add_new_line_before_project_title(3, 1)
remove_cell_first_line(3,1)