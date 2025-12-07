from django.core.management.base import BaseCommand
from users.models import User
from vocabulary.models import StudentWord
from django.db.models import Count


class Command(BaseCommand):
    help = 'Показать список учеников со статистикой слов'

    def handle(self, *args, **kwargs):
        students = User.objects.filter(role='student').annotate(
            word_count=Count('assigned_words')
        ).order_by('-word_count')

        print("=" * 60)
        print(f"{'Ученик':20} {'Имя':20} {'Слов':5} {'Темы':10}")
        print("=" * 60)

        for student in students:
            # Получаем статистику по темам
            topic_stats = StudentWord.objects.filter(
                student=student
            ).select_related('word__topic').values(
                'word__topic__name'
            ).annotate(count=Count('id')).order_by('-count')[:3]

            topics_str = ", ".join([f"{stat['word__topic__name'] or 'Без темы'}"
                                    for stat in topic_stats[:2]])
            if topic_stats.count() > 2:
                topics_str += f" (+{topic_stats.count() - 2})"

            print(f"{student.username:20} "
                  f"{student.get_full_name()[:18]:20} "
                  f"{student.word_count:5} "
                  f"{topics_str[:30]:30}")