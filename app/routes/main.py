from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    HTTP 方法: GET
    處理邏輯: 顯示首頁。包含當月統計與近期清單。
    輸出: 渲染 templates/index.html
    """
    pass

@bp.route('/statistics')
def statistics():
    """
    HTTP 方法: GET
    處理邏輯: 顯示統計圖表頁面。根據分類顯示圓餅圖等。
    輸出: 渲染 templates/statistics.html
    """
    pass
