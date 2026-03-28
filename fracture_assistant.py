#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股骨颈骨折辅助诊断系统
功能：
1. 导入医学影像（DICOM/NII导出的二维图像）
2. 手动标注骨折关键点（近端、远端断端点）
3. 计算骨折角度
4. 根据规则给出术前固定建议
"""

import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import os


class FractureAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("股骨颈骨折辅助诊断系统")
        self.root.geometry("1200x800")
        
        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.points = []  # 存储标注点 [(x1, y1), (x2, y2)]
        self.img_width = 0
        self.img_height = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 顶部控制面板
        control_frame = tk.Frame(self.root, bg='#f0f0f0', height=60)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # 按钮样式
        btn_style = {'font': ('Arial', 10), 'padx': 10, 'pady': 5}
        
        tk.Button(control_frame, text="导入图像", command=self.load_image, 
                 bg='#4CAF50', fg='white', **btn_style).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(control_frame, text="清除标注", command=self.clear_points,
                 bg='#f44336', fg='white', **btn_style).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(control_frame, text="计算角度与建议", command=self.calculate_and_suggest,
                 bg='#2196F3', fg='white', **btn_style).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(control_frame, text="保存结果", command=self.save_result,
                 bg='#FF9800', fg='white', **btn_style).pack(side=tk.LEFT, padx=10, pady=10)
        
        # 主内容区域
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧图像显示区域
        left_frame = tk.Frame(main_frame, bg='#e0e0e0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text="图像显示区域（点击标注骨折近端和远端点）", 
                bg='#e0e0e0', font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.canvas = tk.Canvas(left_frame, bg='white', cursor='crosshair')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        
        # 右侧结果显示区域
        right_frame = tk.Frame(main_frame, bg='#e0e0e0', width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        tk.Label(right_frame, text="分析结果", bg='#e0e0e0', 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.result_text = tk.Text(right_frame, bg='white', font=('Arial', 11),
                                  wrap=tk.WORD, padx=10, pady=10)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 底部状态栏
        self.status_bar = tk.Label(self.root, text="就绪 - 请导入图像", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_image(self):
        """加载图像"""
        file_types = [
            ('所有支持的图像', '*.jpg *.jpeg *.png *.bmp *.tiff *.tif'),
            ('JPEG图像', '*.jpg *.jpeg'),
            ('PNG图像', '*.png'),
            ('TIFF图像', '*.tiff *.tif'),
            ('所有文件', '*.*')
        ]
        
        file_path = filedialog.askopenfilename(
            title="选择医学影像",
            filetypes=file_types
        )
        
        if file_path:
            try:
                self.image_path = file_path
                
                # 读取图像
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    messagebox.showerror("错误", "无法读取图像文件")
                    return
                
                # 转换为RGB显示
                image_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                
                # 保持宽高比缩放显示
                self.display_image = self.resize_for_display(image_rgb)
                
                # 在Canvas上显示
                self.update_canvas()
                
                # 清除之前的标注
                self.points = []
                
                self.img_width = self.display_image.shape[1]
                self.img_height = self.display_image.shape[0]
                
                self.status_bar.config(text=f"已加载: {os.path.basename(file_path)} - 请标注骨折关键点")
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "图像已加载\n\n请在图像上点击标注两个点：\n\n1. 第一个点：骨折近端点\n2. 第二个点：骨折远端点\n\n标注完成后点击【计算角度与建议】按钮。")
                
            except Exception as e:
                messagebox.showerror("错误", f"加载图像失败: {str(e)}")
    
    def resize_for_display(self, image, max_size=800):
        """调整图像大小以适应显示"""
        height, width = image.shape[:2]
        
        if max(height, width) <= max_size:
            return image
        
        if width > height:
            new_width = max_size
            new_height = int(height * max_size / width)
        else:
            new_height = max_size
            new_width = int(width * max_size / height)
        
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    def update_canvas(self):
        """更新Canvas显示"""
        if self.display_image is not None:
            # 转换为PIL Image
            pil_image = Image.fromarray(self.display_image)
            photo = ImageTk.PhotoImage(pil_image)
            
            # 清除Canvas
            self.canvas.delete("all")
            
            # 显示图像
            self.canvas.image = photo  # 保持引用
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            
            # 绘制已标注的点
            for i, (x, y) in enumerate(self.points):
                color = ['red', 'blue'][i]
                label = ['近端点', '远端点'][i]
                self.canvas.create_oval(x-6, y-6, x+6, y+6, 
                                       fill=color, outline='white', width=2, tags=f"point{i}")
                self.canvas.create_text(x, y-15, text=label, fill=color, 
                                       font=('Arial', 10, 'bold'), tags=f"label{i}")
            
            # 绘制连接线
            if len(self.points) == 2:
                x1, y1 = self.points[0]
                x2, y2 = self.points[1]
                self.canvas.create_line(x1, y1, x2, y2, fill='yellow', 
                                       width=2, dash=(5, 5), tags="fracture_line")
    
    def on_canvas_click(self, event):
        """处理Canvas点击事件"""
        if self.display_image is None:
            messagebox.showwarning("提示", "请先导入图像")
            return
        
        if len(self.points) >= 2:
            messagebox.showinfo("提示", "已标注2个点，如需重新标注请点击【清除标注】按钮")
            return
        
        # 记录点坐标
        self.points.append((event.x, event.y))
        
        # 更新显示
        self.update_canvas()
        
        # 更新状态栏
        point_names = ['近端点', '远端点']
        self.status_bar.config(text=f"已标注: {', '.join(point_names[:len(self.points)])}")
    
    def clear_points(self):
        """清除标注点"""
        self.points = []
        self.update_canvas()
        self.status_bar.config(text="标注已清除 - 请重新标注")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "标注已清除\n\n请在图像上重新标注骨折关键点。")
    
    def calculate_and_suggest(self):
        """计算角度并给出建议"""
        if len(self.points) != 2:
            messagebox.showwarning("提示", "请先标注两个关键点（骨折近端和远端）")
            return
        
        try:
            # 提取坐标
            (x1, y1), (x2, y2) = self.points
            
            # 计算骨折线向量（从近端到远端）
            fracture_vector = np.array([x2 - x1, y2 - y1])
            
            # 冠状面法向量（垂直向下的方向）
            coronal_normal = np.array([0, 1])
            
            # 计算夹角（骨折线与冠状面法向量的夹角）
            # 使用点积公式: cos(θ) = (a·b) / (|a|*|b|)
            dot_product = np.dot(fracture_vector, coronal_normal)
            fracture_magnitude = np.linalg.norm(fracture_vector)
            normal_magnitude = np.linalg.norm(coronal_normal)
            
            cos_theta = dot_product / (fracture_magnitude * normal_magnitude)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)  # 防止数值误差
            angle_rad = np.arccos(cos_theta)
            angle_deg = np.degrees(angle_rad)
            
            # 调整角度：与水平线的夹角
            angle_from_horizontal = 90 - angle_deg
            
            # 计算骨折线斜率
            if x2 != x1:
                slope = (y2 - y1) / (x2 - x1)
            else:
                slope = float('inf')
            
            # 生成建议
            suggestion = self.generate_suggestion(angle_from_horizontal, slope)
            
            # 显示结果
            self.display_results(angle_from_horizontal, slope, suggestion)
            
        except Exception as e:
            messagebox.showerror("错误", f"计算失败: {str(e)}")
    
    def generate_suggestion(self, angle, slope):
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
            # 近水平骨折
            suggestions.append({
                'title': '固定方案建议',
                'content': '倾向：平行三钉固定方案\n理由：骨折线较平缓，平行排列的螺钉可以提供更好的稳定性和抗剪切力。'
            })
            screw_angle = angle + 45  # 螺钉角度基于骨折线调整
        elif angle < 60:
            # 中等角度骨折
            suggestions.append({
                'title': '固定方案建议',
                'content': '倾向：交叉固定方案\n理由：骨折线倾斜度适中，交叉排列可以更好地抵抗旋转力矩。'
            })
            screw_angle = angle + 30  # 螺钉角度基于骨折线调整
        else:
            # 陡峭骨折
            suggestions.append({
                'title': '固定方案建议',
                'content': '倾向：平行三钉固定方案（加强版）\n理由：骨折线较陡，需要更垂直的螺钉排列来对抗移位风险。'
            })
            screw_angle = angle + 15  # 螺钉角度基于骨折线调整
        
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
    
    def display_results(self, angle, slope, suggestion_data):
        """显示计算结果和建议"""
        angle_desc, angle_type, suggestions = suggestion_data
        
        result = f"═══════════════════════════════════\n"
        result += f"      股骨颈骨折分析报告\n"
        result += f"═══════════════════════════════════\n\n"
        
        result += f"【基本信息】\n"
        result += f"• 图像文件: {os.path.basename(self.image_path) if self.image_path else '未知'}\n"
        result += f"• 分析时间: {self.get_current_time()}\n\n"
        
        result += f"【角度计算结果】\n"
        result += f"• {angle_desc}\n"
        result += f"• 骨折线类型: {angle_type}\n"
        result += f"• 骨折线斜率: {slope:.3f}\n\n"
        
        result += f"【关键点坐标】\n"
        result += f"• 近端点: ({self.points[0][0]}, {self.points[0][1]})\n"
        result += f"• 远端点: ({self.points[1][0]}, {self.points[1][1]})\n"
        result += f"• 两点距离: {np.sqrt((self.points[1][0]-self.points[0][0])**2 + (self.points[1][1]-self.points[0][1])**2):.1f} 像素\n\n"
        
        result += f"【术前固定建议】\n"
        for i, suggestion in enumerate(suggestions, 1):
            result += f"\n{i}. {suggestion['title']}\n"
            result += f"{'─'*40}\n"
            result += f"{suggestion['content']}\n"
        
        result += f"\n【注意事项】\n"
        result += f"• 本分析基于二维图像标注，仅供参考\n"
        result += f"• 实际手术方案应由专业医生根据三维影像和患者具体情况制定\n"
        result += f"• 建议结合健侧对比进行更准确的评估\n"
        result += f"═══════════════════════════════════\n"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        
        self.status_bar.config(text=f"分析完成 - 骨折角度: {angle:.1f}°")
    
    def get_current_time(self):
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def save_result(self):
        """保存分析结果"""
        if not self.points or not self.result_text.get("1.0", "1.1").strip():
            messagebox.showwarning("提示", "没有可保存的分析结果")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存分析结果",
            defaultextension=".txt",
            filetypes=[('文本文件', '*.txt'), ('所有文件', '*.*')]
        )
        
        if file_path:
            try:
                result = self.result_text.get("1.0", tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                messagebox.showinfo("成功", f"结果已保存到:\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def run(self):
        """运行程序"""
        self.root.mainloop()


if __name__ == "__main__":
    app = FractureAssistant()
    app.run()