import factory

from .models import Category, Hero


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")


class HeroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hero

    name = factory.Sequence(lambda n: "カテゴリー%04d" % n)
    category = factory.SubFactory(CategoryFactory)
