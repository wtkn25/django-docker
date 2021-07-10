from django.db.models import Subquery
from django.test import TestCase

from sample5.models import Category, Hero

from .factories import CategoryFactory, HeroFactory


class SampleTestCase(TestCase):
    def test_query1(self):
        category = CategoryFactory.create()
        HeroFactory.create(category=category)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Hero.objects.count(), 1)

    def test_query2(self):
        category = CategoryFactory.create()
        HeroFactory.create()
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Hero.objects.count(), 1)

    def test_Nplus1であることを確認する(self):
        # N+1を確認したかったけど、1がなかった
        c1 = CategoryFactory.create()
        c2 = CategoryFactory.create()
        HeroFactory.create(category=c1)
        HeroFactory.create(category=c1)
        HeroFactory.create(category=c2)
        with self.assertNumQueries(3):
            categories = Category.objects.all()  # ここではまだ評価されない
            for category in categories:
                print(category.name)
                category.hero_set.all().first()
        # AssertionError: 3 != 1 : 3 queries executed, 1 expected
        # Captured queries were:
        # 1. SELECT "sample5_category"."id", "sample5_category"."name" FROM "sample5_category"
        # 2. SELECT "sample5_hero"."id", "sample5_hero"."name", "sample5_hero"."category_id", "sample5_hero"."benevolence_factor" FROM "sample5_hero" WHERE "sample5_hero"."category_id" = 1 LIMIT 21
        # 3. SELECT "sample5_hero"."id", "sample5_hero"."name", "sample5_hero"."category_id", "sample5_hero"."benevolence_factor" FROM "sample5_hero" WHERE "sample5_hero"."category_id" = 2 LIMIT 21

    def test_prefetch_relatedが有効であることを確認する(self):
        c1 = CategoryFactory.create()
        c2 = CategoryFactory.create()
        HeroFactory.create(category=c1)
        HeroFactory.create(category=c1)
        HeroFactory.create(category=c2)
        with self.assertNumQueries(2):
            categories = Category.objects.all().prefetch_related(
                "hero_set"
            )  # ここではまだ評価されない
            for category in categories:
                category.hero_set.all()

    def test_select_relatedを使わなかった場合(self):
        hero = HeroFactory.create()
        with self.assertNumQueries(2):
            hero = Hero.objects.first()
            hero.category

    def test_select_relatedを使った場合(self):
        hero = HeroFactory.create()
        with self.assertNumQueries(1):
            hero = Hero.objects.select_related().first()
            hero.category

    def test_スライスした場合の評価(self):
        CategoryFactory.create()
        CategoryFactory.create()
        with self.assertNumQueries(1):
            Category.objects.all()[0]  # 特定されたので、評価が入る

    def test_遅延評価の使い方次第でSubqueryは使わなくても良いらしい(self):
        c1 = CategoryFactory.create()
        c2 = CategoryFactory.create()
        HeroFactory.create(category=c1)
        HeroFactory.create(category=c1)
        HeroFactory.create(category=c2)
        with self.assertNumQueries(0):
            # これは、
            categories = Category.objects.all()
            heros = Hero.objects.filter(category__in=categories)
            # print(heros.query)  # 勝手にSubqueryにしてくれるっぽい
            # SELECT "sample5_hero"."id", "sample5_hero"."name", "sample5_hero"."category_id", "sample5_hero"."benevolence_factor" FROM "sample5_hero" WHERE "sample5_hero"."category_id" IN (SELECT "sample5_category"."id" FROM "sample5_category")

    def test_遅延評価してもらうように頑張る(self):
        c1 = CategoryFactory.create()
        HeroFactory.create(category=c1)
        HeroFactory.create(category=c1)
        with self.assertNumQueries(1):
            heros = Hero.objects.filter(
                category=Category.objects.all().first()
            )
            # print(heros.query)  # 勝手にSubqueryにしてくれるっぽい
            # print(heros)

            # category = Subquery(Category.objects.first())
            # heros = Hero.objects.filter(category=category)
            # print(heros.query)  # 勝手にSubqueryにしてくれるっぽい
            # print(heros)


"""
ここまででわかったクエリの評価

QuerySetを求める段階では、評価されない。
ただ、print(queryset)など、結果が必要な場合は、その段階で評価される

get()やfirst()など、一つのインスタンスが特定された段階。
そこから、関連を辿ると、さらにクエリが飛ぶ
"""
