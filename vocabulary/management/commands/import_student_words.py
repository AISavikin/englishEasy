# vocabulary/management/commands/import_student_words.py
import json
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from vocabulary.models import Topic, Word, StudentWord
from users.models import User


class Command(BaseCommand):
    help = 'Импорт слов, экспортированных из старой базы, в новую базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--input',
            type=str,
            required=True,
            help='Путь к JSON файлу с экспортированными данными'
        )
        parser.add_argument(
            '--create-students',
            action='store_true',
            help='Создать учеников из экспортированных данных'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Пропускать существующие слова и темы'
        )

    def handle(self, *args, **options):
        input_file = options['input']
        create_students = options['create_students']
        skip_existing = options['skip_existing']

        self.stdout.write(f'Импорт данных из файла: {input_file}')
        self.stdout.write('=' * 60)

        # Загружаем данные
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Файл не найден: {input_file}'))
            return
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'Ошибка чтения JSON: {e}'))
            return

        # Импортируем данные в транзакции
        with transaction.atomic():
            # 1. Импортируем темы
            topics_created = self.import_topics(data.get('topics', []), skip_existing)

            # 2. Импортируем слова
            words_created = self.import_words(data.get('words', []), skip_existing)

            # 3. Импортируем учеников (если нужно)
            students_created = 0
            if create_students:
                students_created = self.import_students(data.get('students', []))

            # 4. Импортируем назначения слов
            assignments_created = self.import_assignments(
                data.get('student_word_assignments', []),
                create_students
            )

        self.stdout.write(self.style.SUCCESS('Импорт завершен успешно!'))
        self.stdout.write(f'Тем создано: {topics_created}')
        self.stdout.write(f'Слов создано: {words_created}')
        if create_students:
            self.stdout.write(f'Учеников создано: {students_created}')
        self.stdout.write(f'Назначений создано: {assignments_created}')

    def import_topics(self, topics_data, skip_existing):
        """Импорт тем"""
        created_count = 0

        for topic_data in topics_data:
            name = topic_data.get('name')

            if not name:
                self.stdout.write(self.style.WARNING('Пропущена тема без имени'))
                continue

            if skip_existing and Topic.objects.filter(name=name).exists():
                self.stdout.write(f'Тема уже существует: {name}')
                continue

            # Парсим дату создания
            created_at = None
            if 'created_at' in topic_data:
                try:
                    created_at = timezone.datetime.fromisoformat(topic_data['created_at'])
                except (ValueError, TypeError):
                    created_at = None

            topic, created = Topic.objects.get_or_create(
                name=name,
                defaults={
                    'color': topic_data.get('color', '#3B82F6'),
                    'created_at': created_at or timezone.now()
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'Создана тема: {name}')
            else:
                self.stdout.write(f'Тема уже существует: {name}')

        return created_count

    def import_words(self, words_data, skip_existing):
        """Импорт слов"""
        created_count = 0

        for word_data in words_data:
            russian = word_data.get('russian', '').strip().lower()
            english = word_data.get('english', '').strip().lower()

            if not russian or not english:
                self.stdout.write(self.style.WARNING(f'Пропущено слово с пустым значением: {word_data}'))
                continue

            # Проверяем уникальность
            if skip_existing and Word.objects.filter(russian=russian, english=english).exists():
                self.stdout.write(f'Слово уже существует: {russian} → {english}')
                continue

            # Находим тему
            topic = None
            topic_name = word_data.get('topic')
            if topic_name:
                try:
                    topic = Topic.objects.get(name=topic_name)
                except Topic.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Тема не найдена: {topic_name}'))

            # Парсим дату создания
            created_at = None
            if 'created_at' in word_data:
                try:
                    created_at = timezone.datetime.fromisoformat(word_data['created_at'])
                except (ValueError, TypeError):
                    created_at = None

            word, created = Word.objects.get_or_create(
                russian=russian,
                english=english,
                defaults={
                    'topic': topic,
                    'created_at': created_at or timezone.now()
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'Создано слово: {russian} → {english}')
            else:
                self.stdout.write(f'Слово уже существует: {russian} → {english}')

        return created_count

    def import_students(self, students_data):
        """Импорт учеников"""
        created_count = 0

        # Находим системного учителя для назначений
        teacher = User.objects.filter(role='teacher').first()
        if not teacher:
            teacher = User.objects.filter(is_superuser=True).first()

        for student_data in students_data:
            username = student_data.get('username')

            if not username:
                self.stdout.write(self.style.WARNING('Пропущен ученик без username'))
                continue

            if User.objects.filter(username=username).exists():
                self.stdout.write(f'Ученик уже существует: {username}')
                continue

            # Парсим дату регистрации
            date_joined = None
            if 'date_joined' in student_data:
                try:
                    date_joined = timezone.datetime.fromisoformat(student_data['date_joined'])
                except (ValueError, TypeError):
                    date_joined = None

            # Создаем ученика
            student = User.objects.create(
                username=username,
                first_name=student_data.get('first_name', ''),
                last_name=student_data.get('last_name', ''),
                email=student_data.get('email', f'{username}@example.com'),
                role='student',
                date_joined=date_joined or timezone.now()
            )

            # Устанавливаем временный пароль
            student.set_password('password123')
            student.save()

            created_count += 1
            self.stdout.write(f'Создан ученик: {username}')

        return created_count

    def import_assignments(self, assignments_data, create_students):
        """Импорт назначений слов ученикам"""
        created_count = 0

        # Находим системного учителя для назначений
        teacher = User.objects.filter(role='teacher').first()
        if not teacher:
            teacher = User.objects.filter(is_superuser=True).first()

        for assignment_data in assignments_data:
            student_username = assignment_data.get('student_username')
            word_russian = assignment_data.get('word_russian', '').strip().lower()
            word_english = assignment_data.get('word_english', '').strip().lower()

            if not student_username or not word_russian or not word_english:
                self.stdout.write(self.style.WARNING(f'Пропущено назначение с пустыми данными: {assignment_data}'))
                continue

            # Находим ученика
            try:
                student = User.objects.get(username=student_username, role='student')
            except User.DoesNotExist:
                if not create_students:
                    self.stdout.write(self.style.WARNING(f'Ученик не найден: {student_username}'))
                    continue
                # Пропускаем, если не создаем учеников
                continue

            # Находим слово
            try:
                word = Word.objects.get(russian=word_russian, english=word_english)
            except Word.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Слово не найдено: {word_russian} → {word_english}'))
                continue

            # Проверяем, существует ли уже назначение
            if StudentWord.objects.filter(student=student, word=word).exists():
                self.stdout.write(f'Назначение уже существует: {student_username} ← {word_russian}')
                continue

            # Находим учителя, который назначил слово
            assigned_by_username = assignment_data.get('assigned_by')
            assigned_by = teacher  # по умолчанию
            if assigned_by_username:
                try:
                    assigned_by = User.objects.get(username=assigned_by_username)
                except User.DoesNotExist:
                    assigned_by = teacher

            # Парсим дату назначения
            assigned_at = None
            if 'assigned_at' in assignment_data:
                try:
                    assigned_at = timezone.datetime.fromisoformat(assignment_data['assigned_at'])
                except (ValueError, TypeError):
                    assigned_at = None

            # Создаем назначение
            StudentWord.objects.create(
                student=student,
                word=word,
                assigned_by=assigned_by,
                assigned_at=assigned_at or timezone.now(),
                status=assignment_data.get('status', 'new')
            )

            created_count += 1
            self.stdout.write(f'Создано назначение: {student_username} ← {word_russian}')

        return created_count