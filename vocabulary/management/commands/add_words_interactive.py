import os
import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from vocabulary.models import Topic, Word, StudentWord
from colorama import Fore, Style, init
import sys

# Инициализация colorama для цветного вывода
init(autoreset=True)


class Command(BaseCommand):
    help = 'Интерактивное добавление слов ученику из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument(
            '--json-file',
            type=str,
            help='Путь к JSON файлу со словами (опционально)'
        )

    def handle(self, *args, **options):
        self.stdout.write(Fore.CYAN + '=' * 60)
        self.stdout.write(Fore.CYAN + 'ИНТЕРАКТИВНОЕ ДОБАВЛЕНИЕ СЛОВ УЧЕНИКУ')
        self.stdout.write(Fore.CYAN + '=' * 60)

        # Шаг 1: Выбор ученика
        student = self.select_student()
        if not student:
            self.stdout.write(Fore.RED + 'Отмена операции.')
            return

        # Шаг 2: Выбор или указание JSON файла
        json_file = options.get('json_file')
        if not json_file:
            json_file = self.select_json_file()

        # Шаг 3: Загрузка слов из JSON
        words_data = self.load_words_from_json(json_file)
        if not words_data:
            return

        # Шаг 4: Подтверждение
        self.confirm_operation(student, words_data)

        # Шаг 5: Добавление слов
        added_count = self.add_words_to_student(student, words_data)

        # Шаг 6: Итог
        self.show_summary(student, added_count)

    def select_student(self):
        """Выбор ученика из списка существующих"""
        students = User.objects.filter(role='student').order_by('username')

        if not students.exists():
            self.stdout.write(Fore.YELLOW + 'Нет существующих учеников.')
            create_new = input(Fore.WHITE + 'Создать нового ученика? (y/n): ').lower()

            if create_new == 'y':
                return self.create_new_student()
            return None

        self.stdout.write(Fore.GREEN + '\nСписок существующих учеников:')
        self.stdout.write(Fore.GREEN + '-' * 40)

        for i, student in enumerate(students, 1):
            word_count = StudentWord.objects.filter(student=student).count()
            self.stdout.write(
                f"{Fore.CYAN}{i}. {Fore.WHITE}{student.username} "
                f"({student.get_full_name() or 'Без имени'}) - "
                f"{Fore.YELLOW}{word_count} слов"
            )

        self.stdout.write(Fore.GREEN + '-' * 40)
        self.stdout.write(Fore.CYAN + "0. Создать нового ученика")
        self.stdout.write(Fore.CYAN + "q. Отмена")

        while True:
            choice = input(Fore.WHITE + '\nВыберите ученика (номер): ').strip()

            if choice.lower() == 'q':
                return None
            elif choice == '0':
                return self.create_new_student()

            try:
                index = int(choice) - 1
                if 0 <= index < len(students):
                    selected_student = students[index]
                    self.stdout.write(
                        Fore.GREEN + f'Выбран ученик: {selected_student.username}'
                    )
                    return selected_student
                else:
                    self.stdout.write(Fore.RED + 'Неверный номер. Попробуйте снова.')
            except ValueError:
                self.stdout.write(Fore.RED + 'Введите число, 0, или q для отмены.')

    def create_new_student(self):
        """Создание нового ученика"""
        self.stdout.write(Fore.CYAN + '\nСоздание нового ученика:')

        while True:
            username = input(Fore.WHITE + 'Логин: ').strip()
            if not username:
                self.stdout.write(Fore.RED + 'Логин не может быть пустым.')
                continue

            if User.objects.filter(username=username).exists():
                self.stdout.write(Fore.RED + 'Пользователь с таким логином уже существует.')
                continue

            break

        first_name = input(Fore.WHITE + 'Имя (опционально): ').strip()
        last_name = input(Fore.WHITE + 'Фамилия (опционально): ').strip()
        email = input(Fore.WHITE + 'Email (опционально): ').strip()

        # Пароль по умолчанию
        password = 'password123'  # В реальном приложении попросите ввести пароль

        student = User.objects.create(
            username=username,
            first_name=first_name or '',
            last_name=last_name or '',
            email=email or f'{username}@example.com',
            role='student'
        )
        student.set_password(password)
        student.save()

        self.stdout.write(Fore.GREEN + f'Создан новый ученик: {username} (пароль: {password})')
        self.stdout.write(Fore.YELLOW + '⚠️  Не забудьте изменить пароль при первом входе!')

        return student

    def select_json_file(self):
        """Выбор JSON файла"""
        default_file = 'words.json'
        self.stdout.write(Fore.CYAN + '\nВыбор файла со словами:')

        # Проверяем существующие JSON файлы в корне проекта
        json_files = [f for f in os.listdir('.') if f.endswith('.json')]

        if json_files:
            self.stdout.write(Fore.GREEN + 'Найденные JSON файлы:')
            for i, file in enumerate(json_files, 1):
                self.stdout.write(f"{Fore.CYAN}{i}. {Fore.WHITE}{file}")

            choice = input(
                Fore.WHITE + f'\nВыберите файл (1-{len(json_files)}) или укажите свой путь: '
            ).strip()

            try:
                index = int(choice) - 1
                if 0 <= index < len(json_files):
                    return json_files[index]
            except ValueError:
                pass

            # Если ввели путь
            if choice:
                return choice

        # Если нет файлов или выбрано вручную
        while True:
            file_path = input(
                Fore.WHITE + f'Введите путь к JSON файлу [{default_file}]: '
            ).strip() or default_file

            if os.path.exists(file_path):
                return file_path

            self.stdout.write(Fore.RED + f'Файл не найден: {file_path}')
            create_sample = input(
                Fore.WHITE + 'Создать пример файла? (y/n): '
            ).lower()

            if create_sample == 'y':
                self.create_sample_json(file_path)
                return file_path

    def create_sample_json(self, file_path):
        """Создание примера JSON файла"""
        sample_data = [
            {
                "russian": "яблоко",
                "english": "apple",
                "topic": "Еда",
                "topic_color": "#FF6B6B"
            },
            {
                "russian": "собака",
                "english": "dog",
                "topic": "Животные",
                "topic_color": "#4ECDC4"
            },
            {
                "russian": "мама",
                "english": "mother",
                "topic": "Семья",
                "topic_color": "#FFD166"
            },
            {
                "russian": "красный",
                "english": "red",
                "topic": "Цвета",
                "topic_color": "#06D6A0"
            },
            {
                "russian": "счастье",
                "english": "happiness",
                "topic": "Эмоции",
                "topic_color": "#118AB2"
            }
        ]

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)

        self.stdout.write(Fore.GREEN + f'Создан пример файла: {file_path}')
        self.stdout.write(Fore.YELLOW + 'Отредактируйте его перед использованием.')

    def load_words_from_json(self, json_file):
        """Загрузка слов из JSON файла"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                self.stdout.write(Fore.RED + 'Ошибка: JSON должен содержать массив объектов.')
                return None

            # Валидация структуры
            validated_data = []
            for i, item in enumerate(data, 1):
                if not isinstance(item, dict):
                    self.stdout.write(Fore.RED + f'Ошибка в строке {i}: должен быть объектом')
                    continue

                # Проверяем обязательные поля
                if 'russian' not in item or 'english' not in item:
                    self.stdout.write(Fore.RED + f'Ошибка в строке {i}: отсутствуют russian или english')
                    continue

                validated_item = {
                    'russian': str(item['russian']).strip().lower(),
                    'english': str(item['english']).strip().lower(),
                    'topic': item.get('topic', 'Общее'),
                    'topic_color': item.get('topic_color', '#3B82F6'),
                    'notes': item.get('notes', '')
                }
                validated_data.append(validated_item)

            self.stdout.write(Fore.GREEN + f'Загружено {len(validated_data)} слов из {json_file}')
            return validated_data

        except json.JSONDecodeError as e:
            self.stdout.write(Fore.RED + f'Ошибка парсинга JSON: {e}')
            return None
        except FileNotFoundError:
            self.stdout.write(Fore.RED + f'Файл не найден: {json_file}')
            return None
        except Exception as e:
            self.stdout.write(Fore.RED + f'Ошибка загрузки файла: {e}')
            return None

    def confirm_operation(self, student, words_data):
        """Подтверждение операции"""
        # Группируем слова по темам
        topics_summary = {}
        for word in words_data:
            topic = word['topic']
            if topic not in topics_summary:
                topics_summary[topic] = []
            topics_summary[topic].append(f"{word['russian']} → {word['english']}")

        self.stdout.write(Fore.CYAN + '\n' + '=' * 60)
        self.stdout.write(Fore.CYAN + 'ПОДТВЕРЖДЕНИЕ ОПЕРАЦИИ')
        self.stdout.write(Fore.CYAN + '=' * 60)
        self.stdout.write(Fore.WHITE + f'Ученик: {student.username}')
        self.stdout.write(Fore.WHITE + f'Количество слов: {len(words_data)}')
        self.stdout.write(Fore.WHITE + f'Количество тем: {len(topics_summary)}')

        # Показываем краткую статистику по темам
        for topic, words in topics_summary.items():
            self.stdout.write(Fore.GREEN + f'\nТема "{topic}": {len(words)} слов')
            if len(words) <= 5:  # Показываем слова только если их мало
                for word in words[:5]:
                    self.stdout.write(Fore.YELLOW + f'  • {word}')
            else:
                self.stdout.write(Fore.YELLOW + f'  Первые 5 слов:')
                for word in words[:5]:
                    self.stdout.write(Fore.YELLOW + f'  • {word}')

        confirm = input(Fore.WHITE + '\nПродолжить добавление слов? (y/n): ').lower()
        if confirm != 'y':
            self.stdout.write(Fore.YELLOW + 'Операция отменена.')
            sys.exit(0)

    def add_words_to_student(self, student, words_data):
        """Добавление слов ученику"""
        # Получаем учителя для назначения
        teacher = User.objects.filter(role='teacher').first()
        if not teacher:
            # Используем текущего суперпользователя или создаем
            teacher = User.objects.filter(is_superuser=True).first()
            if not teacher:
                teacher = User.objects.create(
                    username='system_teacher',
                    role='teacher',
                    is_staff=True,
                    is_superuser=True
                )
                teacher.set_password('system123')
                teacher.save()

        added_count = 0
        duplicate_count = 0
        topic_created = set()

        self.stdout.write(Fore.CYAN + '\n' + '=' * 60)
        self.stdout.write(Fore.CYAN + 'ДОБАВЛЕНИЕ СЛОВ')
        self.stdout.write(Fore.CYAN + '=' * 60)

        for i, word_item in enumerate(words_data, 1):
            # Прогресс
            if i % 10 == 0 or i == len(words_data):
                self.stdout.write(Fore.WHITE + f'Обработка: {i}/{len(words_data)}...')

            # Получаем или создаем тему
            topic_name = word_item['topic']
            topic_color = word_item['topic_color']

            topic, created = Topic.objects.get_or_create(
                name=topic_name,
                defaults={'color': topic_color}
            )

            if created and topic_name not in topic_created:
                self.stdout.write(Fore.GREEN + f'Создана тема: {topic_name}')
                topic_created.add(topic_name)

            # Получаем или создаем слово
            word, word_created = Word.objects.get_or_create(
                russian=word_item['russian'],
                english=word_item['english'],
                defaults={'topic': topic}
            )

            # Если слово уже существовало, но без темы - добавляем тему
            if not word_created and not word.topic:
                word.topic = topic
                word.save()

            # Создаем связь с учеником
            student_word, assigned_created = StudentWord.objects.get_or_create(
                student=student,
                word=word,
                defaults={
                    'assigned_by': teacher,
                    'status': 'new',
                    'assigned_at': timezone.now()
                }
            )

            if assigned_created:
                added_count += 1
            else:
                duplicate_count += 1

        return added_count

    def show_summary(self, student, added_count):
        """Показать итоговую статистику"""
        # Получаем актуальную статистику
        total_words = StudentWord.objects.filter(student=student).count()

        # Группировка по темам
        from django.db.models import Count
        topic_stats = StudentWord.objects.filter(
            student=student
        ).select_related('word__topic').values(
            'word__topic__name',
            'word__topic__color'
        ).annotate(count=Count('id')).order_by('-count')

        self.stdout.write(Fore.CYAN + '\n' + '=' * 60)
        self.stdout.write(Fore.CYAN + 'ИТОГОВАЯ СТАТИСТИКА')
        self.stdout.write(Fore.CYAN + '=' * 60)
        self.stdout.write(Fore.GREEN + f'Ученик: {student.username}')
        self.stdout.write(Fore.GREEN + f'Добавлено новых слов: {added_count}')
        self.stdout.write(Fore.GREEN + f'Всего слов у ученика: {total_words}')

        if topic_stats:
            self.stdout.write(Fore.CYAN + '\nРаспределение по темам:')
            for stat in topic_stats:
                topic_name = stat['word__topic__name'] or 'Без темы'
                topic_color = stat['word__topic__color'] or '#6c757d'
                count = stat['count']

                # Создаем цветную полоску прогресса
                bar_length = 20
                filled = int((count / total_words) * bar_length) if total_words > 0 else 0
                bar = '█' * filled + '░' * (bar_length - filled)

                self.stdout.write(
                    f"{Fore.WHITE}{topic_name:15} {Fore.CYAN}{bar} "
                    f"{Fore.YELLOW}{count:3} слов"
                )

        self.stdout.write(Fore.CYAN + '\n' + '=' * 60)
        self.stdout.write(Fore.GREEN + 'Операция успешно завершена! ✓')