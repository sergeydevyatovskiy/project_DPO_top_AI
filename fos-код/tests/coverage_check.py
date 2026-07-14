#!/usr/bin/env python3
"""
Проверка покрытия индикаторов КРМ оценочными средствами.

Скрипт читает файл data/competency_map/mapping.csv и проверяет,
что каждый индикатор оценивается не менее чем двумя средствами.
"""

import csv
from collections import defaultdict
from pathlib import Path

def check_coverage(mapping_file: str) -> bool:
    """
    Проверяет покрытие индикаторов оценочными средствами.
    
    Args:
        mapping_file: путь к файлу mapping.csv
    
    Returns:
        True если все индикаторы покрыты >= 2 средствами, False иначе
    """
    # Читаем mapping.csv
    indicators = defaultdict(set)
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            indicator = row['indicator_code']
            assessment = row['assessment_tool_code']
            indicators[indicator].add(assessment)
    
    # Проверяем покрытие
    all_covered = True
    print("=" * 70)
    print("ПРОВЕРКА ПОКРЫТИЯ ИНДИКАТОРОВ КРМ ОЦЕНОЧНЫМИ СРЕДСТВАМИ")
    print("=" * 70)
    print()
    
    for indicator, assessments in sorted(indicators.items()):
        count = len(assessments)
        status = "✅ OK" if count >= 2 else "❌ FAIL"
        print(f"{indicator}: {count} средств {status}")
        print(f"  Средства: {', '.join(sorted(assessments))}")
        if count < 2:
            all_covered = False
    
    print()
    print("=" * 70)
    total = len(indicators)
    covered = sum(1 for a in indicators.values() if len(a) >= 2)
    print(f"Всего индикаторов: {total}")
    print(f"Покрыто >= 2 средствами: {covered} ({covered/total*100:.1f}%)")
    print("=" * 70)
    
    if all_covered:
        print("✅ Все индикаторы покрыты минимум 2 оценочными средствами")
    else:
        print("❌ Обнаружены индикаторы с недостаточным покрытием")
    
    return all_covered

if __name__ == "__main__":
    mapping_file = "data/competency_map/mapping.csv"
    
    if not Path(mapping_file).exists():
        print(f"❌ Файл {mapping_file} не найден")
        exit(1)
    
    success = check_coverage(mapping_file)
    exit(0 if success else 1)