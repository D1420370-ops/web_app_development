from flask import Blueprint, request, redirect, url_for, render_template

bp = Blueprint('records', __name__)

@bp.route('/expense/new', methods=['GET'])
def new_expense():
    """
    HTTP 方法: GET
    處理邏輯: 顯示新增支出表單。
    輸出: 渲染 templates/expense_form.html
    """
    pass

@bp.route('/expense', methods=['POST'])
def create_expense():
    """
    HTTP 方法: POST
    處理邏輯: 接收並驗證表單，寫入一筆支出紀錄到資料庫，然後重導向到首頁。
    輸出: redirect 到 '/'
    """
    pass

@bp.route('/income/new', methods=['GET'])
def new_income():
    """
    HTTP 方法: GET
    處理邏輯: 顯示新增收入表單。
    輸出: 渲染 templates/income_form.html
    """
    pass

@bp.route('/income', methods=['POST'])
def create_income():
    """
    HTTP 方法: POST
    處理邏輯: 接收並驗證表單，寫入一筆收入紀錄到資料庫，然後重導向到首頁。
    輸出: redirect 到 '/'
    """
    pass

@bp.route('/record/<int:id>/delete', methods=['POST'])
def delete_record(id):
    """
    HTTP 方法: POST
    處理邏輯: 根據 id 刪除指定的收支紀錄，重導向到首頁。
    輸出: redirect 到 '/'
    """
    pass
