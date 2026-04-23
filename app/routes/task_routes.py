from flask import Blueprint, request, render_template, redirect, url_for, abort
from app.models.task_model import TaskModel

# 建立 Blueprint，方便管理任務相關的路由，未來可被 app.py 註冊
task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/')
def index():
    """
    任務列表 (首頁)
    HTTP Method: GET
    輸入：無
    處理邏輯：呼叫 TaskModel.get_all() 取得所有任務清單
    輸出：渲染 index.html，並將任務清單傳入模板
    """
    pass

@task_bp.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    """
    新增任務
    HTTP Method: GET, POST
    GET：渲染 task_form.html 顯示空白表單
    POST：接收表單資料 (title, description, due_date)，
          驗證資料後呼叫 TaskModel.create()，成功後重導向至 index 首頁。
    """
    pass

@task_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    """
    編輯任務
    HTTP Method: GET, POST
    GET：呼叫 TaskModel.get_by_id(id) 取得原始資料，渲染 task_form.html 將資料帶入表單。
    POST：接收表單修改後的資料，驗證後呼叫 TaskModel.update() 更新資料庫，重導向至 index 首頁。
    """
    pass

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    切換任務完成狀態
    HTTP Method: POST
    處理邏輯：呼叫 TaskModel.toggle_status(id) 改變任務完成狀態
    輸出：重導向至 index 首頁
    """
    pass

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除任務
    HTTP Method: POST
    處理邏輯：呼叫 TaskModel.delete(id) 將該任務從資料庫中移除
    輸出：重導向至 index 首頁
    """
    pass
