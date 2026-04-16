from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.models.record import Record

bp = Blueprint('records', __name__)

@bp.route('/expense/new', methods=['GET'])
def new_expense():
    """
    HTTP 方法: GET
    處理邏輯: 顯示新增支出表單。
    輸出: 渲染 templates/expense_form.html
    """
    return render_template('expense_form.html')

@bp.route('/expense', methods=['POST'])
def create_expense():
    """
    HTTP 方法: POST
    處理邏輯: 接收並驗證表單，寫入一筆支出紀錄到資料庫，然後重導向到首頁。
    輸出: redirect 到 '/'
    """
    amount = request.form.get('amount')
    category = request.form.get('category')
    record_date = request.form.get('record_date')
    note = request.form.get('note', '')

    if not amount or not category or not record_date:
        flash('請填寫所有必填欄位', 'danger')
        return redirect(url_for('records.new_expense'))
        
    try:
        amount_int = int(amount)
        if amount_int <= 0:
            flash('金額必須大於零', 'danger')
            return redirect(url_for('records.new_expense'))
    except ValueError:
        flash('金額必須為整數', 'danger')
        return redirect(url_for('records.new_expense'))

    data = {
        'type': 'expense',
        'amount': amount_int,
        'category': category,
        'record_date': record_date,
        'note': note
    }
    
    record_id = Record.create(data)
    if record_id:
        flash('新增支出成功！', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('資料庫發生錯誤，請重試！', 'danger')
        return redirect(url_for('records.new_expense'))

@bp.route('/income/new', methods=['GET'])
def new_income():
    """
    HTTP 方法: GET
    處理邏輯: 顯示新增收入表單。
    輸出: 渲染 templates/income_form.html
    """
    return render_template('income_form.html')

@bp.route('/income', methods=['POST'])
def create_income():
    """
    HTTP 方法: POST
    處理邏輯: 接收並驗證表單，寫入一筆收入紀錄到資料庫，然後重導向到首頁。
    輸出: redirect 到 '/'
    """
    amount = request.form.get('amount')
    category = request.form.get('category')
    record_date = request.form.get('record_date')
    note = request.form.get('note', '')

    if not amount or not category or not record_date:
        flash('請填寫所有必填欄位', 'danger')
        return redirect(url_for('records.new_income'))
        
    try:
        amount_int = int(amount)
        if amount_int <= 0:
            flash('金額必須大於零', 'danger')
            return redirect(url_for('records.new_income'))
    except ValueError:
        flash('金額必須為整數', 'danger')
        return redirect(url_for('records.new_income'))

    data = {
        'type': 'income',
        'amount': amount_int,
        'category': category,
        'record_date': record_date,
        'note': note
    }
    
    record_id = Record.create(data)
    if record_id:
        flash('新增收入成功！', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('資料庫發生錯誤，請重試！', 'danger')
        return redirect(url_for('records.new_income'))

@bp.route('/record/<int:id>/delete', methods=['POST'])
def delete_record(id):
    """
    HTTP 方法: POST
    處理邏輯: 根據 id 刪除指定的收支紀錄，重導向到首頁。
    輸出: redirect 到 '/'
    """
    record = Record.get_by_id(id)
    if not record:
        flash('找不到該筆紀錄', 'danger')
        return redirect(url_for('main.index'))
        
    if Record.delete(id):
        flash('紀錄刪除成功！', 'success')
    else:
        flash('刪除失敗！', 'danger')
        
    return redirect(url_for('main.index'))

