#!/usr/bin/env python3
"""
Проверка согласованности весов оценочных средств.

Скрипт проверяет, что сумма весов = 100% на всех уровнях иерархии.
"""

import re
from pathlib import Path

def extract_weights(file_path: str, pattern: str) -> list:
    """
    Извлекает веса из markdown-файла по регулярному выражению.
    
    Args:
        file_path: путь к файлу
        pattern: регулярное выражение для поиска весов
    
    Returns:
        список весов (float)
    """
    weights = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = re.findall(pattern, content)
        for match in matches:
            try:
                weight = float(match.replace('%', '').strip())
                weights.append(weight)
            except ValueError:
                continue
    return weights

def check_weights():
    """Проверяет согласованность весов."""
    print("=" * 70)
    print("ПРОВЕРКА СОГЛАСОВАННОСТИ ВЕСОВ ОЦЕНОЧНЫХ СРЕДСТВ")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # Проверка 1: Итоговая оценка по дисциплине
    print("1. Итоговая оценка по дисциплине:")
    passport_weights = extract_weights(
        "docs/passport.md",
        r'\|\s*(\d+)%\s*\|'
    )
    if passport_weights:
        total = sum(passport_weights[:4])  # LAB, TEST, CP, EXAM
        status = "✅ OK" if abs(total - 100) < 0.01 else "❌ FAIL"
        print(f"   Сумма весов: {total}% {status}")
        if abs(total - 100) >= 0.01:
            all_ok = False
    else:
        print("   ⚠️  Веса не найдены")
    print()
    
    # Проверка 2: Структура курсового проекта
    print("2. Структура курсового проекта:")
    criteria_weights = extract_weights(
        "docs/project_criteria.md",
        r'\|\s*(\d+)%\s*\|'
    )
    if criteria_weights:
        # Первые два веса — это оси MVP и Documentation
        if len(criteria_weights) >= 2:
            total = criteria_weights[0] + criteria_weights[1]
            status = "✅ OK" if abs(total - 100) < 0.01 else "❌ FAIL"
            print(f"   Сумма весов осей: {total}% {status}")
            if abs(total - 100) >= 0.01:
                all_ok = False
    else:
        print("   ⚠️  Веса не найдены")
    print()
    
    # Проверка 3: Мёртвые критерии
    print("3. Проверка мёртвых критериев:")
    files_to_check = [
        "docs/project_criteria.md",
        "src/rubrics/project_ps.md",
        "src/rubrics/project_doc.md",
        "docs/commission_criteria.md"
    ]
    
    dead_criteria_found = False
    for file_path in files_to_check:
        if Path(file_path).exists():
            weights = extract_weights(file_path, r'\|\s*(\d+)%\s*\|')
            dead = [w for w in weights if w == 0]
            if dead:
                print(f"   ❌ {file_path}: обнаружены мёртвые критерии")
                dead_criteria_found = True
    
    if not dead_criteria_found:
        print("   ✅ Мёртвые критерии не обнаружены")
    else:
        all_ok = False
    print()
    
    # Итог
    print("=" * 70)
    if all_ok:
        print("✅ Все проверки пройдены")
    else:
        print("❌ Обнаружены проблемы с весами")
    print("=" * 70)
    
    return all_ok

if __name__ == "__main__":
    success = check_weights()
    exit(0 if success else 1)