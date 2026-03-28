#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股骨颈骨折辅助诊断系统 - Web版本
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from fixation_algorithm import ScrewPlacementAlgorithm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'}

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def calculate_angle(x1, y1, x2, y2):
    """
    计算骨折线角度
    
    参数:
        x1, y1: 近端点坐标
        x2, y2: 远端点坐标
    
    返回:
        angle: 骨折线角度（与水平线的夹角）
        slope: 骨折线斜率
    """
    # 计算骨折线向量
    fracture_vector = np.array([x2 - x1, y2 - y1])
    
    # 冠状面法向量（垂直向下）
    coronal_normal = np.array([0, 1])
    
    # 计算夹角
    dot_product = np.dot(fracture_vector, coronal_normal)
    fracture_magnitude = np.linalg.norm(fracture_vector)
    
    if fracture_magnitude == 0:
        return 0, 0
    
    normal_magnitude = np.linalg.norm(coronal_normal)
    
    cos_theta = dot_product / (fracture_magnitude * normal_magnitude)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)
    
    # 调整为与水平线的夹角
    angle_from_horizontal = 90 - angle_deg
    
    # 计算斜率
    if x2 != x1:
        slope = (y2 - y1) / (x2 - x1)
    else:
        slope = float('inf')
    
    return angle_from_horizontal, slope

def generate_suggestion(angle, slope):
    """根据角度和斜率生成固定建议"""
    suggestions = []
    
    # 角度范围判断
    if angle < 30:
        angle_type = "近水平骨折"
        angle_desc = f"骨折线角度: {angle:.1f}°（近水平）"
    elif angle < 60:
        angle_type = "中等角度骨折"
        angle_desc = f"骨折线角度: {angle:.1f}°（中等角度）"
    else:
        angle_type = "陡峭骨折"
        angle_desc = f"骨折线角度: {angle:.1f}°（陡峭）"
    
    # 基于角度的固定建议
    if angle < 30:
        suggestions.append({
            'title': '固定方案建议',
            'content': '倾向：平行三钉固定方案\n理由：骨折线较平缓，平行排列的螺钉可以提供更好的稳定性和抗剪切力。'
        })
        screw_angle = angle + 45
    elif angle < 60:
        suggestions.append({
            'title': '固定方案建议',
            'content': '倾向：交叉固定方案\n理由：骨折线倾斜度适中，交叉排列可以更好地抵抗旋转力矩。'
        })
        screw_angle = angle + 30
    else:
        suggestions.append({
            'title': '固定方案建议',
            'content': '倾向：平行三钉固定方案（加强版）\n理由：骨折线较陡，需要更垂直的螺钉排列来对抗移位风险。'
        })
        screw_angle = angle + 15
    
    # 螺钉入点建议
    suggestions.append({
        'title': '螺钉入点方向建议',
        'content': f'''• 建议螺钉入针角度: {screw_angle:.1f}°（相对于骨折线）
• 螺钉数量建议: 3枚
• 螺钉间距: 保持10-15mm的均匀间距
• 进钉深度: 避免穿透股骨头关节面'''
    })
    
    # 基于斜率的方向建议
    if slope > 0.5:
        direction = "向外上"
    elif slope < -0.5:
        direction = "向内上"
    else:
        direction = "近似垂直"
    
    suggestions.append({
        'title': '进钉方向提示',
        'content': f'骨折线主要趋势: {direction}\n建议主螺钉方向：尽量垂直于骨折线进针，以获得最大把持力。'
    })
    
    return angle_desc, angle_type, suggestions

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """上传图像"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 添加时间戳避免文件名冲突
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': '图像上传成功'
        })
    
    return jsonify({'error': '不支持的文件格式'}), 400

@app.route('/calculate', methods=['POST'])
def calculate():
    """计算角度并生成建议"""
    data = request.json
    
    if not data or 'points' not in data or len(data['points']) != 2:
        return jsonify({'error': '请提供两个标注点'}), 400
    
    try:
        point1 = data['points'][0]
        point2 = data['points'][1]
        
        x1, y1 = point1['x'], point1['y']
        x2, y2 = point2['x'], point2['y']
        
        # 计算角度
        angle, slope = calculate_angle(x1, y1, x2, y2)
        
        # 初始化钉子放置算法（假设图像尺寸，实际应从图像获取）
        image_width = 800  # 默认值，可以从上传的图像获取实际尺寸
        image_height = 600
        algorithm = ScrewPlacementAlgorithm(image_width, image_height)
        
        # 计算三枚螺钉的位置
        screws = algorithm.calculate_screw_positions(
            point1=(x1, y1),
            point2=(x2, y2),
            angle_deg=angle,
            slope=slope
        )
        
        # 生成详细建议
        angle_desc, angle_type = get_angle_description(angle)
        recommendations = algorithm.generate_detailed_recommendations(angle, angle_type, screws)
        
        # 计算两点距离
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        return jsonify({
            'success': True,
            'angle': angle,
            'angle_desc': angle_desc,
            'angle_type': angle_type,
            'slope': slope,
            'distance': distance,
            'points': data['points'],
            'screws': screws,  # 新增：钉子位置和大小信息
            'recommendations': recommendations,  # 新增：详细建议
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': f'计算失败: {str(e)}'}), 500

def get_angle_description(angle):
    """获取角度描述"""
    if angle < 30:
        return f"骨折线角度: {angle:.1f}°（近水平）", "近水平骨折"
    elif angle < 50:
        return f"骨折线角度: {angle:.1f}°（中等角度）", "中等角度骨折"
    else:
        return f"骨折线角度: {angle:.1f}°（陡峭）", "陡峭骨折"

@app.route('/image/<filename>')
def get_image(filename):
    """获取上传的图像"""
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    print("=" * 60)
    print("股骨颈骨折辅助诊断系统 - Web版本")
    print("=" * 60)
    print("\n启动Web服务器...")
    print("访问地址: http://localhost:8080")
    print("\n按 Ctrl+C 停止服务器\n")
    app.run(debug=True, host='0.0.0.0', port=8080)
