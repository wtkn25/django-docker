from django.test import TestCase
import factory
from .models import Company, Goods

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
        
    name = "会社名"

class GoodsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goods

    name = "商品名"
    company = factory.SubFactory(CompanyFactory)


class CompanyTestCase(TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_company_factory(self):
        CompanyFactory.create()
        self.assertEqual(Company.objects.count(), 1)

        self.assertEqual(Company.objects.first().name, "会社名")


class GoodsTestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_goods_factory(self):
        company = CompanyFactory.create(name="会社A")
        goods = GoodsFactory.create(company=company)
        self.assertEqual(Goods.objects.count(), 1)
        self.assertEqual(Goods.objects.first().company.name, "会社A")
        self.assertEqual(goods.name, "商品名")

    def test_Companyが削除された時にGoodsも削除されることを確認する(self):
        company = CompanyFactory.create(name="会社A")
        GoodsFactory.create(company=company)
        self.assertEqual(Goods.objects.count(), 1)
        company.delete()
        self.assertEqual(Goods.all_objects.count(), 1)


class GoodsManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.goods = GoodsFactory.create()

    def test_論理削除されているデータが取得されないことを確認する(self):
        self.goods.delete()
        self.assertEqual(Goods.objects.count(), 0)

    def test_論理削除したデータを取得できることを確認する(self):
        self.goods.delete()
        self.assertEqual(Goods.all_objects.count(), 1)

class GoodsQuerySetTestCase(TestCase):
    def test_QuerySetのdeleteが論理削除になることを確認する(self):
        Goods.objects.all().delete()
        self.assertEqual(Goods.objects.count(), 0)
        self.assertEqual(Goods.all_objects.count(), 1)


class SignalsTestCase(TestCase):
    def test_post_soft_delete_companyが正常に動作することを確認する(self):
        company = CompanyFactory.create(name="会社A")
        GoodsFactory.create(name="商品A",company=company)
        GoodsFactory.create(name="商品B",company=company)
        self.assertEqual(company.goods_set.count(), 2)
        company.delete()
        self.assertEqual(Goods.objects.count(), 0)
        self.assertEqual(Goods.all_objects.count(), 2)
