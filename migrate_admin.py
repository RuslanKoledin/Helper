#!/usr/bin/env python3
"""
Скрипт миграции учетных записей администраторов
Переносит учетную запись из .env в admins.json
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def migrate_admin_from_env():
    """Миграция администратора из .env в admins.json"""

    print("=" * 60)
    print("Миграция учетной записи администратора")
    print("=" * 60)
    print()

    # Получаем данные из .env
    admin_username = os.getenv('ADMIN_USERNAME', '')
    admin_password_hash = os.getenv('ADMIN_PASSWORD_HASH', '')

    if not admin_username or not admin_password_hash:
        print("❌ ОШИБКА: ADMIN_USERNAME или ADMIN_PASSWORD_HASH не найдены в .env файле")
        print("Миграция невозможна.")
        return

    print(f"✓ Найдена учетная запись: {admin_username}")
    print()

    # Проверяем, существует ли уже admins.json
    admins_file = 'admins.json'

    if os.path.exists(admins_file):
        print(f"⚠️  Файл {admins_file} уже существует")

        # Проверяем, есть ли уже этот пользователь
        try:
            with open(admins_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                admins = data.get('admins', [])

                for admin in admins:
                    if admin.get('username') == admin_username:
                        print(f"ℹ️  Администратор {admin_username} уже существует в {admins_file}")
                        print("Миграция не требуется.")
                        return
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Ошибка при чтении {admins_file}: {e}")
            return
    else:
        print(f"✓ Создаём новый файл {admins_file}")
        # Создаем пустой файл
        with open(admins_file, 'w', encoding='utf-8') as f:
            json.dump({"admins": []}, f, ensure_ascii=False, indent=2)

    # Загружаем текущие данные
    with open(admins_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        admins = data.get('admins', [])

    # Создаем новую учетную запись
    new_admin = {
        'username': admin_username,
        'password_hash': admin_password_hash,
        'role': 'super_admin',  # По умолчанию супер-админ
        'created_by': 'migration_script',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'active': True
    }

    admins.append(new_admin)

    # Сохраняем
    with open(admins_file, 'w', encoding='utf-8') as f:
        json.dump({"admins": admins}, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 60)
    print("✅ МИГРАЦИЯ УСПЕШНО ЗАВЕРШЕНА!")
    print("=" * 60)
    print()
    print(f"Учетная запись '{admin_username}' добавлена в {admins_file}")
    print(f"Роль: Супер-администратор")
    print()
    print("Теперь вы можете:")
    print("1. Войти в админ-панель используя существующие учетные данные")
    print("2. Добавить новых администраторов через меню 'Администраторы'")
    print("3. (Опционально) Удалить ADMIN_USERNAME и ADMIN_PASSWORD_HASH из .env")
    print()
    print("ВАЖНО: Система поддерживает обратную совместимость.")
    print("Если учетная запись не найдена в admins.json, она будет")
    print("проверяться в переменных окружения .env")
    print()


if __name__ == '__main__':
    try:
        migrate_admin_from_env()
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")
        import traceback
        traceback.print_exc()
