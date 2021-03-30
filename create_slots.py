# Import from shell
import datetime
from faker import Faker
from random import randint, choice


def create_slots():
    fake = Faker()
    for x in range(30):
        g = Game(
            from_age=randint(8, 20),
            to_age=randint(21, 35),
            gender=choice(["Male", "Female"]),
            game_type=fake.name(),
        )
        g.save()
    for x in range(5):
        d = datetime.date(2021, 4, x + 1)
        ft = 6
        s = 10
        p = Competition(id=x, name=fake.name())
        p.save()
        p.games.set(Game.objects.all()[x * 5 : x * 5 + 6])
        p.save()
        for y in range(3):
            s = Slot(
                from_time=str(ft + y) + ":00:00",
                to_time=str(ft + 1 + y) + ":00:00",
                date=d,
            )
            s.save()
        s = Slot(
            from_time=str(ft + 3) + ":00:00",
            to_time=str(ft + 4) + ":00:00",
            date=d,
            competition=p,
        )
        s.save()
        s.game.set(Game.objects.all()[x * 5 : x * 5 + 6])
        s.save()
        ft = 18
        for y in range(3):
            s = Slot(
                from_time=str(ft + y) + ":00:00",
                to_time=str(ft + 1 + y) + ":00:00",
                date=d,
            )
            s.save()
        f = fake.name()
        c = Course(id=x + 5, name=f)
        c.save()
        age = (
            str(randint(2000, 2020))
            + "-"
            + str(randint(1, 12))
            + "-"
            + str(randint(1, 28))
        )
        d = Coordinator(
            id=x + 5, username=fake.name(), age=age, gender=choice(["Male", "Female"])
        )
        d.save()
        d.course.add(c)
        d.save()


create_slots()


def create_courses():
    fake = Faker()
    for x in range(20):
        f = fake.name()
        c = Course(id=x + 5, name=f)
        c.save()
        age = (
            str(randint(2000, 2020))
            + "-"
            + str(randint(1, 12))
            + "-"
            + str(randint(1, 28))
        )
        d = Coordinator(
            id=x + 5, username=fake.name(), age=age, gender=choice(["Male", "Female"])
        )
        d.save()
        d.course.add(c)
        d.save()
