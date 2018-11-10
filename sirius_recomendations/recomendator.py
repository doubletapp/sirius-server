# -*- coding: utf-8 -*-
import math
import json
import os


# Почистим предметы от трэшака
SUBJECTS = {
    u'английскому языку': (u'английский', u'английскому', u'англискому',),
    u'астронимии': (u'астронимии', u'астронмии', u'астрономии',),
    u'биологии': (u'билогии', u'биолгоии', u'биологи', u'биологии', u'биологиии', u'бологии',),
    u'географии': (u'геогафии', u'географии', u'географиии', u'георгафии',),
    u'геологии': (u'геологии',),
    u'геометрии': (u'геометрии',),
    u'информатике': (u'икт', u'инфогрматике', u'инфоматике', u'информаике', u'информатеке', u'информатике',),
    u'искусству': (u'искусству', u'искусству(мхк)', u'мхк',),
    u'испанскому': (u'испанскому',),
    u'истории': (u'истории',),
    u'краеведению': (u'краеведению',),
    u'кубановедению': (u'кубановедению',),
    u'культуре': (u'культуре',),
    u'литературе': (u'литературе',),
    u'медицине': (u'медицине',),
    u'немецкому': (u'неецкому', u'немецкому',),
    u'обж': (u'обж',),
    u'обществознанию': (u'общесвознанию', u'обществознанию', u'общестовзнанию', u'общестознанию',),
    u'осетинскому': (u'осетинскому',),
    u'праву': (u'праву',),
    u'программированию': (u'программированию',),
    u'психологии': (u'психологии',),
    u'робототехнике': (u'робототехнике',),
    u'русскому': (u'русскому',),
    u'физике': (u'физика', u'физике',),
    u'физической культуре': (u'физической культуре', u'физкультуре',),
    u'филологии': (u'филологии',),
    u'французскому': (u'французскому',),
    u'черчению': (u'черчению',),
    u'экологии': (u'экологии', u'экология', u'экологогии',),
    u'экономике': (u'экономике',),
    u'математике': (u'"математике"', u'матаматике', u'математика', u'математике', u'математики', u'матемитике', u'матиматике',),
    u'химии': (u'"химии"', u'химии', u'химиии', u'химия',),
}


others = {
    u'Публикация',
    u'Другое',
    u'Награда за НИР',
    u'Патент',
    u'Грант',
    u'Дополнительное обучение, выездная школа',
    u'Дополнительное обучение, подготовка к олимпиаде',
}


def get_type(achievement):
    if achievement.startswith('201'):
        return 'win'
    elif achievement.startswith(u'Рекомендация'):
        return 'recomendation'
    elif any(map(achievement.startswith, others)):
        return 'other'
    else:
        return 'grants'  # стипендии и прочая фигня тоже начинается с года, поэтому такого не должно остаться


# Удаляем префикс из достижений
def normalize(achievement):
    if achievement.startswith('201'):
        achievement = achievement[6:]
    elif achievement.startswith(u'Рекомендация'):
        achievement = achievement[14:]
    else:
        for i in others:
            if achievement.startswith(i):
                achievement = achievement[len(i) + 1:]
                break
    achievement = achievement.lstrip()
    achievement = achievement.lower()
    return achievement


# normalize by rules

def find_subject(s):
    r = s.find(u' по ')
    if r == -1:
        return None
    else:
        for subj, variants in SUBJECTS.items():
            for v in variants:
                if v in s[r + 4:r + 4 + len(v) + 15]:
                    return subj

    return find_subject(s[r + 4:])


def normalize_by_rules(s):
    # Ищем слово "школьный этап" или "школьная олимпиада" или "школьный тур" и трансформируем в
    if (
            u'школьный этап' in s or u'школьная олимпиада' in s or u'школьный тур' in s
    ):
        subj = find_subject(s)
        if subj is not None:
            prefix = u'школьный этап всероссийской олимпиады школьников по '
            return prefix + subj
    if (
            (u'муницип' in s and (
                    u'олимп' in s or u'вош' in s or u'всош' in s))
            or u'городская олимп' in s or u'городской олимп' in s
    ):
        subj = find_subject(s)
        if subj is not None:
            prefix = u'муниципальный этап всероссийской олимпиады школьников по '
            return prefix + subj

    # Ищем слово "регион" или "республик" и трансформируем в
    if (
            (u'регион' in s or u'республик' in s)
            and (u'олимп' in s or u'вош' in s or u'всош' in s)
    ):
        subj = find_subject(s)
        if subj is not None:
            prefix = u'региональный этап всероссийской олимпиады школьников по '
            return prefix + subj

    # Ищем слова ("финал всерос" и "олимп") или "финал всош" трансформируем в
    if (
            (u'финал всерос' in s and u'олимп' in s)
            or (u'финал' in s and (u'всош' in s or u'вош' in s))

    ):
        subj = find_subject(s)
        if subj is not None:
            prefix = u'финальный этап всероссийской олимпиады школьников по '
            return prefix + subj

    # После обработки предыдущих случаев ищем
    if (
            u'всероссийская олимпиада школьников' in s
            or u'всероссийская олимпиада по' in s
            or u'вош' in s
            or u'всош' in s
    ):
        subj = find_subject(s)
        if subj is not None:
            prefix = u'неизвестный этап всероссийской олимпиады школьников по '
            return prefix + subj
        else:
            return u'неизвестный этап всероссийской олимпиады школьников'

    if (u'кенгур' in s):
        return u'международный математический конкурс-игра "кенгуру"'

    if (
            (
                    u'кит' in s and u'компьютеры' in s and u'информатика' in s and u'технологии' in s)
            or (u'всероссийск' in s and u'конкурс' in s and u'кит' in s)
    ):
        return u'всероссийский конкурс "кит - компьютеры, информатика, технологии"'

    if (
            u'турнир городов' in s
            and (
            u'художественн' not in s
            or u'премия' not in s
            or u'плаванью' not in s
            or u'конференция' not in s
    )
    ):
        return u'международный математический турнир городов'

    if u'фоксфорд' in s:
        subj = find_subject(s)
        if subj is not None:
            prefix = u'международная онлайн-олимпиада "фоксфорда" по '
            return prefix + subj
        else:
            if u'олимп' in s:
                return u'международная онлайн-олимпиада "фоксфорда"'
    # Ищем слово "выездная" и "олимпиада" и "мфти" и трансформируем в
    if (u'выездн' in s and u'олимп' in s and u'мфти' in s):
        return u'выездная физико-математическая олимпиада мфти'

    # Ищем слова "олимпиада" и "ломоносов" трансформируем в
    if (u'ломонос' in s and u'олимп' in s):
        subj = find_subject(s)
        if subj is not None:
            prefix = u'олимпиада школьников "ломоносов" по '
            return prefix + subj

    # Ищем слово "турнир" и "ломоносова" трансформируем в
    if (u'ломонос' in s and u'турнир' in s):
        return u'Турнир имени М.В. Ломоносова'  # тут вроде как есть и предметы, обобщим для простоты

    # Ищем слова "олимпиада" и "ломоносов" трансформируем в
    if (u'онлайн' in s and u'физтех' in s):
        subj = find_subject(s)
        if subj is not None:
            prefix = u'онлайн-этап олимпиады "физтех" по '
            return prefix + subj
        else:
            return u'онлайн-этап олимпиады "физтех"'

    # Ищем слово "физтех" и трансформируем в
    if (u'физтех' in s):
        return u'олимпиада "физтех"'

    # Ищем слово "кубок" и "колмогоров" и  трансформируем в
    if (u'кубок' in s and u'колмогоров' in s):
        return u'Международный Математический турнир старшеклассников "Кубок памяти А.Н. Колмогорова"'

    # Собираем оставшиеся олимпиады
    if (u'олимп' in s):
        subj = find_subject(s)
        if subj is not None:
            prefix = u'олимпиада по '
            return prefix + subj
    return s


def distCosine(vecA, vecB):
    def dotProduct(vecA, vecB):
        d = 0.0
        for dim in vecA:
            if dim in vecB:
                d += vecA[dim]*vecB[dim]
        return d
    return dotProduct(vecA, vecB) / math.sqrt(dotProduct(vecA, vecA)) / math.sqrt(dotProduct(vecB, vecB))


def makeRecommendation(userID, userRates, nBestUsers, nBestProducts):
    matches = [(u, distCosine(userRates[userID], userRates[u])) for u in userRates if u != userID]
    bestMatches = sorted(matches, key=lambda x: (x[1], x[0]), reverse=True)[:nBestUsers]
    sim = dict()
    sim_all = sum([x[1] for x in bestMatches])
    bestMatches = dict([x for x in bestMatches if x[1] > 0.0])
    for relatedUser in bestMatches:
        for product in userRates[relatedUser]:
            if not product in userRates[userID]:
                if not product in sim:
                    sim[product] = 0.0
                sim[product] += userRates[relatedUser][product] * bestMatches[relatedUser]
    for product in sim:
        sim[product] /= sim_all
    bestProducts = sorted(sim.items(), key=lambda x: (x[1], x[0]), reverse=True)[:nBestProducts]
    return [(x[0], x[1]) for x in bestProducts]


dir_path = os.path.dirname(__file__)
with open(os.path.join(dir_path, 'transformed_recomendations.json'), 'r') as f:
    transformed_recomendations = json.load(f)
transformed_recomendations = {int(k): v for k, v in transformed_recomendations.items()}
with open(os.path.join(dir_path, 'users.json'), 'r') as f:
    USERS = json.load(f)
USERS = {int(k): v for k, v in USERS.items()}


def recommend(user_id, achievements):
    """

    :param user_id: id пользователя из сириуса
    :param achievements:
    :return:
    """
    user_id = user_id

    achievements = list(map(
        normalize_by_rules,
        map(normalize, achievements)
    ))

    if user_id not in USERS:
        transformed_recomendations[len(USERS)] = dict.fromkeys(achievements, 1)
        USERS[user_id] = len(USERS)

    recomendations = []
    n_users = 5
    while not recomendations:
        recomendations = makeRecommendation(
            USERS[user_id], transformed_recomendations, n_users, 5
        )
        n_users *= 2

    return recomendations


"""
from sirius_recomendations.recomendator import *

test_user_id = 1345713645817 
achievements = [
    u'городская олимпиада по физике-математике ололол',
    u'региональный этап олимпиады по математике ололо',
    u'гбу до ко центр развития одаренных детей',
]
recommend(test_user_id, achievements)
"""

if __name__ == "__main__":
    import sys

    user_id = sys.argv[-2]
    achievements = json.loads(sys.argv[-1])

    # python sirius_recomendations/recomendator.py 123 '["городская олимпиада по физике-математике ололол","региональный этап олимпиады по математике ололо","гбу до ко центр развития одаренных детей"]'
    # for i, coeff in recommend(int(user_id), achievements):
    #
    #     print(i.encode('utf-8'))

    print(json.dumps([i for i, _ in recommend(int(user_id), achievements)]).encode('utf-8'))
