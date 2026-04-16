from flask import Blueprint, render_template, request
from app.models.record import Record
import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    HTTP 方法: GET
    處理邏輯: 顯示首頁。包含當月統計與近期清單。
    輸出: 渲染 templates/index.html
    """
    month_param = request.args.get('month')
    if not month_param:
        now = datetime.datetime.now()
        month_param = f"{now.year}-{now.month:02d}"
        
    summary = Record.get_summary_by_month(month_param)
    
    # 這裡過濾出當月份的紀錄以供顯示
    all_records = Record.get_all()
    records = [r for r in all_records if r.record_date.startswith(month_param)]
    
    return render_template('index.html', summary=summary, records=records, current_month=month_param)

@bp.route('/statistics')
def statistics():
    """
    HTTP 方法: GET
    處理邏輯: 顯示統計圖表頁面。根據分類顯示圖表。
    輸出: 渲染 templates/statistics.html
    """
    month_param = request.args.get('month')
    if not month_param:
        now = datetime.datetime.now()
        month_param = f"{now.year}-{now.month:02d}"
        
    summary = Record.get_summary_by_month(month_param)
    all_records = Record.get_all()
    
    expense_categories = {}
    income_categories = {}
    
    for r in all_records:
        if not r.record_date.startswith(month_param):
            continue
            
        if r.type == 'expense':
            expense_categories[r.category] = expense_categories.get(r.category, 0) + r.amount
        elif r.type == 'income':
            income_categories[r.category] = income_categories.get(r.category, 0) + r.amount
            
    return render_template('statistics.html', 
                           current_month=month_param, 
                           summary=summary,
                           expense_categories=expense_categories,
                           income_categories=income_categories)
