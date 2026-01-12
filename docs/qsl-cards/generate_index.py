#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QSL Cards Index Generator
扫描 qsl-cards 目录下的图片文件，按年份组织并生成索引JSON
"""

import os
import json
import re
from pathlib import Path

def extract_call_sign_from_filename(filename):
    """
    从文件名中提取呼号
    文件名格式: M5BVP89TO9_5a7v823uoye.jpg
    呼号通常是第一部分
    """
    # 移除扩展名
    name_without_ext = os.path.splitext(filename)[0]
    # 按下划线分割，第一部分可能是呼号
    parts = name_without_ext.split('_')
    if len(parts) > 0:
        return parts[0]
    return name_without_ext

def generate_qsl_index(qsl_dir="docs/qsl-cards"):
    """
    生成QSL卡片索引
    """
    qsl_path = Path(qsl_dir)
    
    if not qsl_path.exists():
        print(f"错误: 目录 {qsl_dir} 不存在")
        return
    
    index = {
        "last_updated": None,
        "years": {}
    }
    
    # 遍历所有年份目录
    for year_dir in sorted(qsl_path.iterdir()):
        if year_dir.is_dir() and year_dir.name.isdigit():
            year = year_dir.name
            index["years"][year] = []
            
            # 攫取该年份目录下的所有图片文件
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
                image_files.extend(year_dir.glob(ext))
            
            # 按文件名排序
            image_files.sort()
            
            for img_file in image_files:
                filename = img_file.name
                file_size = img_file.stat().st_size
                
                # 提取呼号
                call_sign = extract_call_sign_from_filename(filename)
                
                # 构建相对路径（用于HTML中引用）
                relative_path = f"qsl-cards/{year}/{filename}"
                
                # 获取文件修改时间
                mtime = img_file.stat().st_mtime
                
                card_info = {
                    "filename": filename,
                    "path": relative_path,
                    "call_sign": call_sign,
                    "size": file_size,
                    "modified": mtime
                }
                
                index["years"][year].append(card_info)
    
    # 添加统计信息
    total_cards = sum(len(cards) for cards in index["years"].values())
    index["summary"] = {
        "total_cards": total_cards,
        "years": sorted(index["years"].keys()),
        "year_count": len(index["years"])
    }
    
    # 保存索引文件
    index_file = qsl_path / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"索引文件已生成: {index_file}")
    print(f"总计: {total_cards} 张卡片")
    print(f"年份: {', '.join(sorted(index['years'].keys()))}")
    
    return index

if __name__ == "__main__":
    generate_qsl_index()
