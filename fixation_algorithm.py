#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股骨颈骨折固定算法模块
基于股骨颈骨折治疗的最佳实践和临床指南
"""

import numpy as np
import math

class ScrewPlacementAlgorithm:
    """螺钉放置算法"""
    
    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
        # 假设图像比例：根据CT扫描标准，假设1像素 ≈ 0.5mm
        self.pixel_to_mm = 0.5
        
    def calculate_screw_positions(self, point1, point2, angle_deg, slope):
        """
        计算三枚螺钉的位置
        
        参数:
            point1: 近端点 (x, y)
            point2: 远端点 (x, y)
            angle_deg: 骨折线角度
            slope: 骨折线斜率
        
        返回:
            screws: 三枚螺钉的位置和信息
        """
        x1, y1 = point1
        x2, y2 = point2
        
        # 计算骨折线中点（作为参考）
        midpoint_x = (x1 + x2) / 2
        midpoint_y = (y1 + y2) / 2
        
        # 计算骨折线向量
        fracture_vector = np.array([x2 - x1, y2 - y1])
        fracture_magnitude = np.linalg.norm(fracture_vector)
        
        # 归一化骨折线向量
        if fracture_magnitude > 0:
            fracture_unit = fracture_vector / fracture_magnitude
        else:
            fracture_unit = np.array([1, 0])
        
        # 计算垂直于骨折线的向量（用于螺钉方向）
        # 螺钉应该尽量垂直于骨折线进针
        perpendicular_vector = np.array([-fracture_unit[1], fracture_unit[0]])
        
        # 螺钉长度计算（基于骨折线长度和患者体型）
        fracture_length_mm = fracture_magnitude * self.pixel_to_mm
        screw_length = self._calculate_screw_length(fracture_length_mm)
        
        # 螺钉直径（标准6.5mm或7.3mm）
        screw_diameter = self._calculate_screw_diameter(fracture_length_mm)
        
        # 计算三枚螺钉的位置
        screws = []
        
        # 螺钉1：下位螺钉（主要承重螺钉）
        screw1_pos = self._calculate_screw1_position(
            midpoint_x, midpoint_y, perpendicular_vector, screw_length
        )
        screws.append({
            'name': '螺钉1（低位主钉）',
            'entry_point': screw1_pos['entry'],
            'tip_point': screw1_pos['tip'],
            'length': screw1_pos['length'],
            'diameter_mm': screw_diameter,
            'angle': screw1_pos['angle'],
            'description': '低位主承重螺钉，应尽量垂直于骨折线'
        })
        
        # 螺钉2：中位螺钉（辅助稳定螺钉）
        screw2_pos = self._calculate_screw2_position(
            midpoint_x, midpoint_y, perpendicular_vector, screw_length
        )
        screws.append({
            'name': '螺钉2（中位辅助钉）',
            'entry_point': screw2_pos['entry'],
            'tip_point': screw2_pos['tip'],
            'length': screw2_pos['length'],
            'diameter_mm': screw_diameter,
            'angle': screw2_pos['angle'],
            'description': '中位辅助稳定螺钉，提供抗旋转稳定性'
        })
        
        # 螺钉3：上位螺钉（支撑螺钉）
        screw3_pos = self._calculate_screw3_position(
            midpoint_x, midpoint_y, perpendicular_vector, screw_length
        )
        screws.append({
            'name': '螺钉3（高位支撑钉）',
            'entry_point': screw3_pos['entry'],
            'tip_point': screw3_pos['tip'],
            'length': screw3_pos['length'],
            'diameter_mm': screw_diameter,
            'angle': screw3_pos['angle'],
            'description': '高位支撑螺钉，防止股骨颈短缩'
        })
        
        return screws
    
    def _calculate_screw_length(self, fracture_length_mm):
        """
        计算螺钉长度
        
        规则：
        - 螺钉长度应超过骨折线至少20mm
        - 一般长度范围：70-100mm
        - 根据骨折线长度调整
        """
        base_length = 75  # 基础长度
        additional = min(fracture_length_mm * 0.3, 25)  # 最多增加25mm
        length = base_length + additional
        return round(length, 1)
    
    def _calculate_screw_diameter(self, fracture_length_mm):
        """
        计算螺钉直径
        
        规则：
        - 标准直径：6.5mm或7.3mm
        - 骨折线较长或骨质较差时使用7.3mm
        """
        if fracture_length_mm > 40:  # 骨折线较长
            return 7.3
        else:
            return 6.5
    
    def _calculate_screw1_position(self, mx, my, perp_vector, length_mm):
        """
        计算螺钉1位置（低位主钉）
        - 位于骨折线下方
        - 应尽量垂直于骨折线
        """
        # 长度转换为像素
        length_px = length_mm / self.pixel_to_mm
        
        # 进针点：骨折线中点下方30-40px
        offset_entry = 35
        entry_x = mx
        entry_y = my + offset_entry
        
        # 钉尖：沿垂直于骨折线的方向向股骨头延伸
        tip_x = entry_x + perp_vector[0] * length_px * 0.8
        tip_y = entry_y + perp_vector[1] * length_px * 0.8
        
        # 计算螺钉角度（相对于水平线）
        screw_vector = np.array([tip_x - entry_x, tip_y - entry_y])
        angle_rad = math.atan2(screw_vector[1], screw_vector[0])
        angle_deg = math.degrees(angle_rad)
        
        return {
            'entry': (int(entry_x), int(entry_y)),
            'tip': (int(tip_x), int(tip_y)),
            'length': length_mm,
            'angle': round(angle_deg, 1)
        }
    
    def _calculate_screw2_position(self, mx, my, perp_vector, length_mm):
        """
        计算螺钉2位置（中位辅助钉）
        - 位于骨折线中部
        - 与螺钉1形成适当角度（交叉或平行）
        """
        # 长度转换为像素
        length_px = length_mm / self.pixel_to_mm
        
        # 进针点：骨折线中点稍偏内/外
        offset_x = 25
        offset_y = 15
        entry_x = mx + offset_x
        entry_y = my + offset_y
        
        # 钉尖：沿垂直于骨折线的方向向股骨头延伸
        tip_x = entry_x + perp_vector[0] * length_px * 0.75
        tip_y = entry_y + perp_vector[1] * length_px * 0.75
        
        # 计算螺钉角度
        screw_vector = np.array([tip_x - entry_x, tip_y - entry_y])
        angle_rad = math.atan2(screw_vector[1], screw_vector[0])
        angle_deg = math.degrees(angle_rad)
        
        return {
            'entry': (int(entry_x), int(entry_y)),
            'tip': (int(tip_x), int(tip_y)),
            'length': round(length_mm * 0.95, 1),
            'angle': round(angle_deg, 1)
        }
    
    def _calculate_screw3_position(self, mx, my, perp_vector, length_mm):
        """
        计算螺钉3位置（高位支撑钉）
        - 位于骨折线上方
        - 防止股骨颈短缩
        """
        # 长度转换为像素
        length_px = length_mm / self.pixel_to_mm
        
        # 进针点：骨折线中点上方25px
        offset_entry = -20
        offset_x = -20
        entry_x = mx + offset_x
        entry_y = my + offset_entry
        
        # 钉尖：沿垂直于骨折线的方向向股骨头延伸
        tip_x = entry_x + perp_vector[0] * length_px * 0.7
        tip_y = entry_y + perp_vector[1] * length_px * 0.7
        
        # 计算螺钉角度
        screw_vector = np.array([tip_x - entry_x, tip_y - entry_y])
        angle_rad = math.atan2(screw_vector[1], screw_vector[0])
        angle_deg = math.degrees(angle_rad)
        
        return {
            'entry': (int(entry_x), int(entry_y)),
            'tip': (int(tip_x), int(tip_y)),
            'length': round(length_mm * 0.9, 1),
            'angle': round(angle_deg, 1)
        }
    
    def generate_detailed_recommendations(self, angle_deg, fracture_type, screws):
        """
        生成详细的固定建议
        基于股骨颈骨折治疗指南和临床经验
        """
        recommendations = []
        
        # 1. 骨折类型评估
        fracture_assessment = self._assess_fracture_type(angle_deg, fracture_type)
        recommendations.append(fracture_assessment)
        
        # 2. 固定方案选择
        fixation_strategy = self._recommend_fixation_strategy(angle_deg, fracture_type)
        recommendations.append(fixation_strategy)
        
        # 3. 螺钉配置建议
        screw_config = self._recommend_screw_configuration(screws)
        recommendations.append(screw_config)
        
        # 4. 手术技术要点
        surgical_tips = self._surgical_technique_tips(angle_deg)
        recommendations.append(surgical_tips)
        
        # 5. 术后注意事项
        post_op_care = self._post_operation_care()
        recommendations.append(post_op_care)
        
        return recommendations
    
    def _assess_fracture_type(self, angle_deg, fracture_type):
        """评估骨折类型"""
        assessment = {
            'title': '骨折类型评估',
            'content': f'''骨折线角度: {angle_deg:.1f}°
骨折类型: {fracture_type}
Pauwels分型: {self._get_pauwels_classification(angle_deg)}

骨折稳定性评估:
{self._get_stability_assessment(angle_deg)}'''
        }
        return assessment
    
    def _get_pauwels_classification(self, angle_deg):
        """Pauwels分型"""
        if angle_deg < 30:
            return "I型（稳定型）"
        elif angle_deg < 50:
            return "II型（潜在不稳定型）"
        else:
            return "III型（不稳定型）"
    
    def _get_stability_assessment(self, angle_deg):
        """稳定性评估"""
        if angle_deg < 30:
            return "骨折线较平缓，相对稳定，内固定成功率高"
        elif angle_deg < 50:
            return "骨折线中等角度，存在一定剪切力，需注意固定强度"
        else:
            return "骨折线较陡，剪切力大，需坚强固定，建议加用抗旋转措施"
    
    def _recommend_fixation_strategy(self, angle_deg, fracture_type):
        """推荐固定方案"""
        if angle_deg < 30:
            strategy = "推荐：平行三钉固定（倒三角排列）"
            details = '''
理由：Pauwels I型骨折剪切力小，平行三钉可提供足够的稳定性
排列方式：倒三角形排列（低位两钉，高位一钉）
优点：生物力学稳定性好，创伤小，恢复快'''
        elif angle_deg < 50:
            strategy = "推荐：交叉固定（改良型）"
            details = '''
理由：Pauwels II型骨折存在一定剪切力，交叉排列可更好地抵抗剪切力
排列方式：低位两钉交叉，高位一钉支撑
优点：抗剪切能力强，稳定性好'''
        else:
            strategy = "推荐：滑动髋螺钉系统（DHS）或加压螺钉"
            details = '''
理由：Pauwels III型骨折剪切力大，普通螺钉固定失败率高
建议：考虑使用DHS或PCCP（经皮加压钢板）
注意：如使用螺钉固定，需加用抗旋转螺钉'''
        
        return {
            'title': '固定方案建议',
            'content': f'{strategy}\n{details}'
        }
    
    def _recommend_screw_configuration(self, screws):
        """螺钉配置建议"""
        screw1 = screws[0]
        screw2 = screws[1]
        screw3 = screws[2]
        
        return {
            'title': '螺钉配置详情',
            'content': f'''【螺钉1】{screw1['name']}
  • 长度: {screw1['length']}mm
  • 直径: {screw1['diameter_mm']}mm
  • 进针角度: {screw1['angle']}°
  • {screw1['description']}

【螺钉2】{screw2['name']}
  • 长度: {screw2['length']}mm
  • 直径: {screw2['diameter_mm']}mm
  • 进针角度: {screw2['angle']}°
  • {screw2['description']}

【螺钉3】{screw3['name']}
  • 长度: {screw3['length']}mm
  • 直径: {screw3['diameter_mm']}mm
  • 进针角度: {screw3['angle']}°
  • {screw3['description']}

技术要求：
• 螺钉间距：保持10-15mm，避免过近导致骨质破坏
• 螺钉尖端：进入股骨头软骨下骨5-10mm
• 螺钉尾部：平贴股骨外侧皮质'''
        }
    
    def _surgical_technique_tips(self, angle_deg):
        """手术技术要点"""
        return {
            'title': '手术技术要点',
            'content': f'''1. 复位质量要求
   • 解剖复位是成功的关键
   • Garden对线指数应达到I-II级
   • 前倾角恢复至10-15°

2. 进针技术
   • 采用C臂机透视引导
   • 首先打入导针，确认位置后钻孔
   • 使用拉力螺钉技术

3. 特殊注意事项
   • {angle_deg if angle_deg > 50 else ""}对于Pauwels III型骨折，建议内侧支撑（medial support）
   • 避免螺钉穿透关节面
   • 确保螺钉分散排列，避免过度集中'''
        }
    
    def _post_operation_care(self):
        """术后注意事项"""
        return {
            'title': '术后注意事项',
            'content': '''1. 早期活动
   • 术后24-48小时开始被动活动
   • 术后3-5天开始部分负重（根据骨折类型）

2. 康复训练
   • 髋关节屈伸训练
   • 股四头肌等长收缩训练
   • 逐步增加负重

3. 定期复查
   • 术后2周、6周、3个月、6个月复查
   • 观察骨折愈合情况
   • 评估螺钉位置和稳定性

4. 并发症预防
   • 预防深静脉血栓
   • 预防感染
   • 预防股骨头坏死'''
        }