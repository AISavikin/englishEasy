# vocabulary/management/commands/export_student_words.py
import json
from django.core.management.base import BaseCommand
from django.db.models import Count
from vocabulary.models import StudentWord, Topic, Word
from users.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Экспорт слов, назначенных ученикам, для импорта в пустую базу'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='student_words_export.json',
            help='Путь к выходному JSON файлу (по умолчанию: student_words_export.json)'
        )
        parser.add_argument(
            '--include-students',
            action='store_true',
            help='Включить данные об учениках в экспорт'
        )
        parser.add_argument(
            '--include-statistics',
            action='store_true',
            help='Включить статистику по словам учеников'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        include_students = options['include_students']
        include_statistics = options['include_statistics']

        self.stdout.write(f'Экспорт данных в файл: {output_file}')
        self.stdout.write('=' * 60)

        # Собираем данные для экспорта
        export_data = self.collect_export_data(include_students, include_statistics)

        # Сохраняем в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f'Экспорт завершен! Файл сохранен: {output_file}'
        ))
        self.stdout.write(f'Тем: {len(export_data.get("topics", []))}')
        self.stdout.write(f'Слов: {len(export_data.get("words", []))}')
        if include_students:
            self.stdout.write(f'Учеников: {len(export_data.get("students", []))}')

    def collect_export_data(self, include_students, include_statistics):
        """Сбор данных для экспорта"""
        export_data = {
            'export_date': timezone.now().isoformat(),
            'export_type': 'student_words',
            'description': 'Экспорт слов, назначенных ученикам, для импорта в пустую базу данных'
        }

        # 1. Получаем все уникальные слова, которые назначены ученикам
        student_words = StudentWord.objects.select_related('word', 'word__topic').all()

        # Получаем уникальные слова
        word_ids = set(sw.word.id for sw in student_words)
        words = Word.objects.filter(id__in=word_ids).select_related('topic')

        # 2. Получаем уникальные темы
        topic_ids = set(w.topic.id for w in words if w.topic)
        topics = Topic.objects.filter(id__in=topic_ids)

        # 3. Экспортируем темы
        export_data['topics'] = [
            {
                'name': topic.name,
                'color': topic.color,
                'created_at': topic.created_at.isoformat() if topic.created_at else None
            }
            for topic in topics
        ]

        # 4. Экспортируем слова
        export_data['words'] = [
            {
                'russian': word.russian,
                'english': word.english,
                'topic': word.topic.name if word.topic else None,
                'created_at': word.created_at.isoformat() if word.created_at else None
            }
            for word in words
        ]

        # 5. Экспортируем учеников (если нужно)
        if include_students:
            student_ids = set(sw.student.id for sw in student_words)
            students = User.objects.filter(id__in=student_ids, role='student')

            export_data['students'] = [
                {
                    'username': student.username,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'email': student.email,
                    'date_joined': student.date_joined.isoformat() if student.date_joined else None
                }
                for student in students
            ]

        # 6. Экспортируем назначения слов (связь ученик-слово)
        export_data['student_word_assignments'] = [
            {
                'student_username': sw.student.username,
                'word_russian': sw.word.russian,
                'word_english': sw.word.english,
                'assigned_by': sw.assigned_by.username if sw.assigned_by else None,
                'assigned_at': sw.assigned_at.isoformat() if sw.assigned_at else None,
                'status': sw.status
            }
            for sw in student_words
        ]

        # 7. Экспортируем статистику (если нужно)
        if include_statistics:
            export_data['student_word_statistics'] = [
                {
                    'student_username': sw.student.username,
                    'word_russian': sw.word.russian,
                    'word_english': sw.word.english,
                    'status': sw.status,
                    'times_seen': sw.times_seen,
                    'times_attempted': sw.times_attempted,
                    'times_correct': sw.times_correct,
                    'times_wrong': sw.times_wrong,
                    'avg_response_time': sw.avg_response_time,
                    'current_streak': sw.current_streak,
                    'longest_streak': sw.longest_streak,
                    'last_correct_date': sw.last_correct_date.isoformat() if sw.last_correct_date else None,
                    'first_seen': sw.first_seen.isoformat() if sw.first_seen else None,
                    'last_interaction': sw.last_interaction.isoformat() if sw.last_interaction else None
                }
                for sw in student_words
            ]

        return export_data