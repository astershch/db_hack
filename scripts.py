import random

from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid


COMPLIMENTS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


def get_schoolkid(full_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    except MultipleObjectsReturned:
        print('Найдено несколько учеников. Пожалуйста, уточните ФИО.')
        raise SystemExit
    except ObjectDoesNotExist:
        print('Не найдено ни одного ученика. Пожалуйста, уточните ФИО.')
        raise SystemExit
    return schoolkid


def fix_marks(full_name):
    schoolkid = get_schoolkid(full_name)
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(full_name):
    schoolkid = get_schoolkid(full_name)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(full_name, subject):
    schoolkid = get_schoolkid(full_name)

    commendations = Commendation.objects.filter(
        schoolkid=schoolkid,
        subject__title=subject,
    )

    dates = set()

    for commendation in commendations:
        dates.add(commendation.created)

    lessons = Lesson.objects.filter(
        ~Q(date__in=dates),
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject,
    )

    if lessons:
        lesson = random.choice(lessons)
    else:
        print('Не найдено ни одного урока для прикрепления похвалы!')
        raise SystemExit

    Commendation.objects.create(
        text=random.choice(COMPLIMENTS),
        subject=lesson.subject,
        teacher=lesson.teacher,
        schoolkid=schoolkid,
        created=lesson.date,
    )
