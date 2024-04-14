 # Розгортання проєкту локально
   1. Завантажити та запустити [Docker](https://www.docker.com/).
   2. Завантажити репозиторій
   3. Відкрити папку з репозиторієм
   4. Створити .env файл (за приклад можна взяти .env.example файл)
   5. Запустити команду
      ```python
      docker-compose up -d --build
      ```
   6. Потім запустити команди
      
      ``` python
      docker-compose exec web python manage.py makemigrations
      ```

      ```python
      docker-compose exec web python manage.py migrate
      ```

# Сертифікати

Сертифікати були додані спеціально для економії часу у випадку розгортання проєкту локально для економії часу.

