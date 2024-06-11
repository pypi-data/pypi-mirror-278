# -*- coding:utf-8 -*- #

import pandas as pd
import time
import ast
from datetime import datetime,timedelta,date
from openpyxl import Workbook as workbook,load_workbook
import xlwings
from copy import copy
import os
from pathlib import Path
from redmail import EmailSender
import configparser
import pkg_resources
from pythonnet import set_runtime
import platform
import inspect

os_type = platform.system()
if os_type == "Windows":
    DLL_FILES = [pkg_resources.resource_filename('reportXlsx', f'resources/windows/{dll_name}') for dll_name in [
        'Spire.XLS.dll','SkiaSharp.dll'
    ]]
    Dll_CLASS = [pkg_resources.resource_filename('reportXlsx',f'resources/windows/{class_name}') for class_name in ['Spire.XLS','SkiaSharp']]
else:
    os.environ['PYTHONNET_PYDLL'] = '/usr/share/dotnet/shared/Microsoft.NETCore.App/6.0.30/System.Private.CoreLib.dll'
    os.environ['PYTHONNET_RUNTIME'] = 'coreclr'
    DLL_FILES = [pkg_resources.resource_filename('reportXlsx', f'resources/linux/{dll_name}') for dll_name in [
        'Spire.XLS.dll','SkiaSharp.dll'
    ]]
    Dll_CLASS = [pkg_resources.resource_filename('reportXlsx',f'resources/linux/{class_name}') for class_name in ['Spire.XLS','SkiaSharp']]

import clr
clr.AddReference(DLL_FILES[0])
clr.AddReference(DLL_FILES[1])

from openpyxl.styles import numbers
from System.IO import *
from SkiaSharp import *
from Spire.Xls import *
from Spire.Xls.Core.Spreadsheet import HTMLOptions
from aspose.cells import HtmlSaveOptions, SaveFormat, Workbook as workbooks
from aspose.cells.drawing import ImageType
from openpyxl.formatting.rule import ColorScaleRule



class EmptyParameterError(Exception):
    """自定义异常类，用于处理参数为空的错误"""
    def __init__(self, parameter_name):
        self.parameter_name = parameter_name
        self.message = f"参数 '{parameter_name}' 不能为空"
        super().__init__(self.message)

class ParameterError(Exception):
    """自定义异常类，用于处理参数类型错误的情况"""
    def __init__(self, message, parameter_name):
        self.parameter_name = parameter_name
        self.message = message
        super().__init__(self.message)

def validate_parameters(params_to_check=None):
    if params_to_check is None:
        params_to_check = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            signature = inspect.signature(func)
            bound_arguments = signature.bind(*args, **kwargs)
            bound_arguments.apply_defaults()
            
            for name, value in bound_arguments.arguments.items():
                if name == 'self':
                    continue
                
                # 只检查指定的参数是否为空
                if name in params_to_check:
                    if value is None or (isinstance(value, str) and not value.strip()):
                        raise EmptyParameterError(name)
                    
                # 参数类型检查
                param = signature.parameters[name]
                if param.annotation is not param.empty and not isinstance(value, param.annotation):
                    raise ParameterError(f"Parameter '{name}' is of type {type(value).__name__}, expected {param.annotation.__name__}", name)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator





class sqlResult_to_Excel:

    def __init__(self,figure_chart=None,rank_chart=None,
                 left_on=1,
                 right_on=1,
                 sorted_col=6,
                 send_date= datetime.now()-timedelta(days=1),
                 pic_dpi = 180,
                 font_path_for_linux=['/usr/share/fonts/chinese'],
                 *args
                 ):
        self.figure_chart = figure_chart #通报前半部分
        self.rank_chart = rank_chart #通报的后半部分
        self.left_on = left_on #左表join的行
        self.right_on = right_on #右表关联的行
        self.sorted_col = sorted_col #排序列
        self.send_date = send_date
        self.pic_dpi = pic_dpi
        self.font_path = font_path_for_linux
        self.rule1 = ColorScaleRule(
            start_type='min', start_color='FFF46A6A',  # 浅红色
            mid_type='percentile', mid_value=50, mid_color='FFFDEB83',  # 浅黄色
            end_type='max', end_color='FF63BE7B'  # 浅绿色
        )
        self.rule2 = ColorScaleRule(
            start_type='min', start_color='FF63BE7B',  # 浅绿色
            mid_type='percentile', mid_value=50, mid_color='FFFDEB83',  # 浅黄色
            end_type='max', end_color='FFF46A6A'  # 浅红色
        )
    
    def _copy_rows(self, source_ws, target_ws, num_rows):
        for row in source_ws.iter_rows(min_row=1, max_row=num_rows):
            new_row = [cell.value for cell in row]
            target_ws.append(new_row)
            for idx, cell in enumerate(row):
                new_cell = target_ws.cell(row=target_ws.max_row, column=idx + 1)
                self._copy_cell_format(cell, new_cell)
            target_ws.row_dimensions[target_ws.max_row].height = source_ws.row_dimensions[cell.row].height
    
    def _copy_merged_cells(self, source_ws, target_ws):
        # 复制合并单元格
        for merged_cell in source_ws.merged_cells.ranges:
            target_ws.merge_cells(str(merged_cell))
            min_col, min_row, max_col, max_row = merged_cell.bounds
            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    src_cell = source_ws.cell(row=row, column=col)
                    tgt_cell = target_ws.cell(row=row, column=col)
                    self._copy_cell_format(src_cell, tgt_cell)
            target_ws.row_dimensions[min_row].height = source_ws.row_dimensions[min_row].height
    
    def _copy_cell_format(self, source_cell, target_cell):
        if source_cell.has_style:
            target_cell.font = copy(source_cell.font)
            target_cell.border = copy(source_cell.border)
            target_cell.fill = copy(source_cell.fill)
            target_cell.number_format = source_cell.number_format
            target_cell.alignment = copy(source_cell.alignment)
            target_cell.protection = copy(source_cell.protection)

    
    def _replace_text_in_html(self,file_path, old_text, new_text):
        try:
            # 读取HTML文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        
            # 替换指定的文本
            updated_html_content = html_content.replace(old_text, new_text)
        
            
            print("文本替换成功！")
            return updated_html_content
        except Exception as e:
            print(f"出现错误: {e}")

    def _copy_sheet(self,source_ws, target_ws):
    # 复制数据和样式
        for row in source_ws.iter_rows():
            for cell in row:
                new_cell = target_ws.cell(row=cell.row, column=cell.column, value=cell.value)
                if cell.has_style:
                    new_cell.font = copy(cell.font)
                    new_cell.border = copy(cell.border)
                    new_cell.fill = copy(cell.fill)
                    new_cell.number_format = cell.number_format
                    new_cell.protection = copy(cell.protection)
                    new_cell.alignment = copy(cell.alignment)
        # 处理合并单元格
        for merge_cell in source_ws.merged_cells.ranges:
            target_ws.merge_cells(str(merge_cell))

    @validate_parameters(params_to_check=['path'])
    def _solve_cannot_auto_calculate_func(self,path:str)->None:
        excel_app = xlwings.App(visible=False)
        excel_book = excel_app.books.open(path)
        excel_book.save()
        excel_book.close()
        excel_app.quit()
    
    @validate_parameters 
    def deal_with_sql_result(self,need_delete_col_list:list)->pd.DataFrame:
        if len(need_delete_col_list) == 0:
            raise EmptyParameterError(need_delete_col_list)
        figure_chart = pd.DataFrame(self.figure_chart)
        rank_chart = pd.DataFrame(self.rank_chart)
        merge_chart = pd.merge(figure_chart,rank_chart,left_on=self.left_on,right_on=self.right_on,how='left').reindex()
        #针对merge_chart排序
        part1 = merge_chart.iloc[:-1].sort_values(by= self.sorted_col,ascending= False)
        last_row = merge_chart.iloc[-1:]
        df_result = pd.concat([part1,last_row],ignore_index=True)
        df_result.columns = list(range(len(df_result.columns)))
        #替换文字
        df_result[1]=df_result[1].apply(self.replace_value)
        df_result.drop(need_delete_col_list,axis= 1 ,inplace = True)
        df_result = df_result.reset_index(drop = True)
        return df_result

    def to_excel(self,
                df_result,
                 excl_start_row = 4,
                 excl_start_col =1,
                 excl_file_path='',
                 **pos):
        wb = load_workbook(excl_file_path)
        sheet_name = self.sheet_name
        if sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
        else:
            ws = wb.create_sheet(title= self.sheet_name)

        start_row = excl_start_row
        start_col = excl_start_col

        for r_idx,row in df_result.iterrows():
            for c_idx,value in enumerate(row):
                ws.cell(row=start_row+r_idx,column=start_col+c_idx,value = value)
        wb.save(excl_file_path)

    @validate_parameters(params_to_check=['codilist','metalist','path','sheet_name'])
    def update_by_template(self,codilist:list,metalist:list,path='',dis ='',sheet_name = '')->None:
        wb = load_workbook(path)
        sh_name = sheet_name
        if sh_name in wb.sheetnames:
            ws = wb[sheet_name]
        else:
            ws = wb.create_sheet(title= sheet_name)
        for item1,item2 in zip(codilist,metalist):
            start_row = item1[0]
            start_col = item1[1]
            for r_idx,row in enumerate(item2):
                #print(row),print(type(row))
                for c_idx,value in enumerate(ast.literal_eval(row)):
                    #print(value)
                    ws.cell(row=start_row+r_idx,column=start_col+c_idx,value = value)
                    #print(f'row:{start_row+r_idx}',f'column:{start_col+c_idx}')
                    #print(ws.cell(row=start_row+r_idx,column=start_col+c_idx,value = value).value)
        if dis:
            wb.save(dis)
        else:
            wb.save(path)
    
    @validate_parameters(params_to_check=['codilist','metalist','path','target_path','sheet_name'])
    def ajust_and_copy_excel(self,source_codilist:list,target_codilist:list,path='',dis = '',sheet_name = ''):
        self._solve_cannot_auto_calculate_func(path)
        wb = load_workbook(path,data_only=True)
        sheet = wb[sheet_name]
        wb.save('test.xlsx')
        #针对所有坐标开展排序工作
        for s_codi,t_codi in zip(source_codilist,target_codilist):
            source_range = sheet[s_codi]
            target = sheet[t_codi]
            start_row = target.row
            start_col = target.column
            for source_row_index,source_row in enumerate(source_range):
                for source_col_index,source_cell in enumerate(source_row):
                    target_row = start_row + source_row_index
                    target_col = start_col + source_col_index
                    #print(target_row,target_col)
                    target_cell = sheet.cell(row=target_row,column=target_col)
                    target_cell.value = source_cell.value
        if dis:
            wb.save(dis)         
        else:
            wb.save(path)

    @validate_parameters(params_to_check=['sort_range_list','sort_col_index_list','path','sheet_name'])
    def sort_excel(self,sort_range_list:list,sort_col_index_list:list,path='',dis = '',if_reverse = True,sheet_name = ''):
        wb = load_workbook(path,data_only=True)
        sheet = wb[sheet_name]
        true_sort_index_list = [x-1 for x in sort_col_index_list]
        for s_range ,sort_index in zip(sort_range_list,true_sort_index_list):
            sort_range = sheet[s_range]
            data = list(sort_range)
            data_all=[]
            for index,row in enumerate(data):
                data_row =[]
                for item in enumerate(row):
                    data_row.append(item[1].value)
                data_all.append(data_row)
            data_all.sort(key = lambda row:row[sort_index],reverse=if_reverse)
        
            start_row = sort_range[0][0].row  # 范围的起始行号
            start_col = sort_range[0][0].column  # 范围的起始列号

            for row_index, row_data in enumerate(data_all):
                for col_index,value in enumerate(row_data):
                    # 计算目标单元格的行和列位置
                    target_row = start_row + row_index
                    target_col = start_col + col_index
                    # 将排序后的值写入目标单元格
                    sheet.cell(row=target_row, column=target_col).value = value
        if dis:
            wb.save(dis)
        else:
            wb.save(path)

    @validate_parameters(params_to_check=['generate_range','path','sheet_name'])
    def excel_to_html(self,generate_range:tuple,path = '',sheet_name = '')->str:
        wb = Workbook()
        source_wb = Workbook()
        source_wb.LoadFromFile(path)
        old_sheet = source_wb.Worksheets[sheet_name] 
        # 选 
        cell_range = old_sheet.Range[generate_range] 
        sheet = wb.Worksheets[0]
        cell_range.Copy(sheet.Range[generate_range])
        
        stream = MemoryStream()
        options = HTMLOptions()
        options.SavedAsFragment = True
        options.isExportStyle = True
        sheet.SaveToHtml(stream,options)
        
        stream.Position = 0;
        reader = StreamReader(stream);
        htmlString = reader.ReadToEnd();
        wb.Dispose()
        return htmlString



    @validate_parameters(params_to_check=['starting_col_index','need_delete_cols','path','sheet_name'])
    def del_col_excl(self,starting_col_index:int,need_delete_cols:int,path='',dis= '',sheet_name ='')->None:
        wb =load_workbook(path)
        sh_name = sheet_name
        if sh_name in wb.sheetnames:
            ws = wb[sh_name]
        starting_cols_index = starting_col_index
        num_of_cols_to_delete = need_delete_cols
        ws.delete_cols(starting_cols_index,num_of_cols_to_delete)
        if dis:
            wb.save(dis)
        else:
            wb.save(path)

    @validate_parameters(params_to_check=['results_df_list','name_lists','dis'])
    def add_detail(self,results_df_list:list,name_lists:list,path='',dis = ''):
        if not os.path.exists(path) or not path:
            wb = workbook()
            default_sheet = wb.active
            wb.remove(default_sheet)
        else:
            wb = load_workbook(path)
        for item,name in zip(results_df_list,name_lists):
            new_sheet = wb.create_sheet(title=name)
            for row in item:
                str_row = tuple(str(item) for item in row)
                new_sheet.append(str_row)
        if not dis:
            wb.save(path)
        else:
            wb.save(dis)

    @validate_parameters(params_to_check=['sheet_need_change_list','need_set_col_tuple','path'])
    #设置查看参数
    def set_up_style_of_the_workbook(self,sheet_need_change_list:list,need_set_col_tuple:list,path='',dis = ''):
        wb = load_workbook(path)
        for sheet,need_row in zip(sheet_need_change_list,need_set_col_tuple):
            ws = wb[sheet]  
            max_row = ws.max_row
            max_col = ws.max_column

            for row in ws.iter_rows(min_row=1, max_row=max_row, min_col=1, max_col=max_col):
                for cell in row:
                    text_value = cell.value
                    try:
                        numeric_value = float(text_value)
                        cell.value = numeric_value
                    except (ValueError, TypeError):
                        pass
            print(need_row)
            for column in need_row:
                print(need_row)
                for row in range(1, max_row + 1):
                    cell = ws.cell(row=row, column=column)
                    cell.number_format = numbers.FORMAT_PERCENTAGE
        if dis:
            wb.save(dis)
        else:
            wb.save(path)

    @validate_parameters(params_to_check=['target_excel'])
    def split_the_excel(self, target_excel, sheet_options=None, format_setting=None, if_value_only=True):
        wb = load_workbook(target_excel)
        wb_name = target_excel.split('.')[0]
        # 加载带数据的工作簿
        wb_dataonly = load_workbook(target_excel, data_only=if_value_only)
        
        # 如果没有提供 sheet_options，默认处理所有工作表并进行拆分
        if sheet_options is None:
            sheet_options = {sheet: {'should_split': True, 'column_index': 1, 'header_row': 2} for sheet in wb.sheetnames}
        
        # 创建一个字典来存储所有工作表的拆分数据
        split_data = {}

        # 遍历所有工作表，根据需要进行处理
        for sheet_name, options in sheet_options.items():
            should_split = options.get('should_split', True)
            column_index = options.get('column_index', 1)
            header_row = options.get('header_row', 1)
            ws = wb[sheet_name]
            
            if should_split:
                # 遍历每一行，根据指定字段的值进行拆分
                for row in ws.iter_rows(min_row=header_row + 1):
                    key = row[column_index - 1].value  # 由于列索引从1开始，所以需要减1
                    if key is not None and key != 0:
                        if key not in split_data:
                            split_data[key] = {sheet: [] for sheet in wb.sheetnames}
                        split_data[key][sheet_name].append(row)

        print(f'the split data is {split_data.keys()}')

        # 创建新的工作簿并将拆分后的数据写入
        for key, sheets_data in split_data.items():
            # 确保只有在有拆分数据的情况下才创建工作簿
            if not any(sheets_data[sheet] for sheet in sheet_options if sheet_options[sheet]['should_split']):
                continue  # 跳过没有实际拆分数据的项
            
            filename = f"{wb_name}-{key}.xlsx"
            wb_new = workbook()
            
            for sheet_name in wb.sheetnames:
                if sheet_name == 'Sheet':
                    ws_new = wb_new.active
                    ws_new.title = sheet_name
                else:
                    ws_new = wb_new.create_sheet(sheet_name)
                ws = wb[sheet_name]
                
                # 复制表头
                header_row = sheet_options[sheet_name]['header_row']
                self._copy_rows(ws, ws_new, header_row)
                
                # 复制数据
                if sheet_options[sheet_name]['should_split']:
                    for row_data in sheets_data[sheet_name]:
                        ws_new.append([cell.value for cell in row_data])
                        for idx, cell in enumerate(row_data):
                            new_cell = ws_new.cell(row=ws_new.max_row, column=idx + 1)
                            self._copy_cell_format(cell, new_cell)
                        
                else:
                    for row in ws.iter_rows(min_row=header_row + 1):
                        ws_new.append([cell.value for cell in row])
                        if any(cell.value for cell in row):  # 检查是否有数据
                            for idx, cell in enumerate(row):
                                new_cell = ws_new.cell(row=ws_new.max_row, column=idx + 1)
                                self._copy_cell_format(cell, new_cell)
                        
                
                # 复制合并单元格
                self._copy_merged_cells(ws, ws_new)
            
            # 删除默认创建的工作表
            if "Sheet" in wb_new.sheetnames and "Sheet" not in wb.sheetnames:
                del wb_new["Sheet"]
            
            # 设置单元条件格式 {'2级': {'A': 1, 'B': 2}}
            if format_setting:
                for ws_item, solution in format_setting.items():
                    ws_c = wb_new[ws_item]
                    for col, rule_index in solution.items():
                        max_row = ws_c.max_row
                        rule = self.rule1 if rule_index == 1 else self.rule2
                        ws_c.conditional_formatting.add(f'{col}{header_row}:{col}{max_row}', rule)
            wb_new.save(filename)
        

    
    @validate_parameters(params_to_check=['target_wb','need_add_workbook','need_sheet_name'])
    def add_sheet(self,target_wb='',need_add_workbook='',need_sheet_name='',new_sheet_name='new sheet'):
        #添加sheet
        wb = load_workbook(target_wb)
        wb_old = load_workbook(need_add_workbook)
        ws_old = wb_old[need_sheet_name]
        ws_new = wb.create_sheet(new_sheet_name)

        self._copy_sheet(ws_old,ws_new)
        wb.save(target_wb)
    
    @validate_parameters(params_to_check=['target_wb','source_workbook','source_sheet_name'])
    def add_sheet_with_style(self,target_wb='',source_workbook='',source_sheet_name='',new_sheet_name='new sheet'):
        #添加sheet
        wb = Workbook()
        wb.LoadFromFile(target_wb)
        if wb.Worksheets[new_sheet_name]:
            wb.Worksheets.Remove(wb.Worksheets[new_sheet_name])
        source_wb = Workbook()
        source_wb.LoadFromFile(source_workbook)
        old_sheet = source_wb.Worksheets[source_sheet_name] 
        wb.Worksheets.AddCopy(old_sheet)

        wb.Worksheets[source_sheet_name].Name = new_sheet_name
        new_sheet = wb.Worksheets[new_sheet_name]
        wb.ActiveSheetIndex = wb.Worksheets.Count - 1
        wb.SaveToFile(target_wb,FileFormat.Version2013)
    
    @validate_parameters(params_to_check=['source_file'])
    def convert_specific_sheet_to_html(self,source_file, target_file = '1.html'):
        # 加载 Excel 文件
        workbook = workbooks(source_file)
        # 指定转换的工作表
        #sheet_index = workbook.
        #workbook.getWorksheets().setActiveSheetIndex(sheet_index)
        # 创建 HtmlSaveOptions 对象
        options = HtmlSaveOptions()
        # 设置导出的 HTML 为单个页面
        options.export_active_worksheet_only = True
        # 将图像导出为 HTML 中的 base64 编码
        options.export_images_as_base64 = True
        options.exclude_unused_styles =True
        options.image_options.image_type = ImageType.PNG
        options.export_similar_border_style = True
        # 保持所有行和列的原始大小
        # 保存转换的 HTML 文件
        workbook.save(target_file, options)
        # 替换保护字体
        return self._replace_text_in_html(target_file,'Evaluation Only. Created with Aspose.Cells for .NET.Copyright 2003 - 2024 Aspose Pty Ltd.','')
        
    @validate_parameters(params_to_check=['to_pic_generate_range','path'])
    def excel_to_pic(self,to_pic_generate_range,path = '',sheet_name = '通报',pic_name = 'results.png'):
        #生成新xlsx
        wb = Workbook()
        source_wb = Workbook()
        source_wb.LoadFromFile(path)
        old_sheet = source_wb.Worksheets[sheet_name] 
        wb.Worksheets.AddCopy(old_sheet)
        wb.Worksheets.RemoveAt(0)
        wb.Worksheets.RemoveAt(1)
       
        setting = ConverterSetting()
        setting.XDpi = self.pic_dpi
        setting.YDpi = self.pic_dpi
        wb.ConverterSetting =setting
        sheet = wb.Worksheets[sheet_name]
        
        os_type = platform.system()
        if os_type == "Windows":
            sheet.SaveToImage(pic_name,to_pic_generate_range[0],to_pic_generate_range[1],to_pic_generate_range[2],to_pic_generate_range[3] )
            wb.Dispose()
        elif os_type == "Linux":
            wb.CustomFontFileDirectory= self.font_path
            image_stream = sheet.ToImage(to_pic_generate_range[0],to_pic_generate_range[1],to_pic_generate_range[2],to_pic_generate_range[3])
            managedStream = SKManagedStream(image_stream)
            bitmap = SKBitmap.Decode(managedStream)
            image = SKImage.FromBitmap(bitmap)
            data = image.Encode(SKEncodedImageFormat.Png,self.pic_dpi)
            File.WriteAllBytes(pic_name,data.ToArray())
            wb.Dispose()
        else:
            print("不支持当前系统")
    
    

if __name__ =='__main__':
    pass