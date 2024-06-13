import os
import sys
from datetime import datetime

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.db import connection
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Check if migrations are applied
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app='your_app_name' AND applied >= %s", [datetime.now()])
        row = cursor.fetchone()
        if row[0] == 0:
            execute_from_command_line(['your_project_name', 'migrate'])
    
    # Default to 'runserver'
    execute_from_command_line(sys.argv + ['runserver'])

if __name__ == '__main__':
    main()
