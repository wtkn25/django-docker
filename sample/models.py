from django.db import models
from django.utils import timezone

class CompanyQuerySet(models.QuerySet):
    def delete(self)->None:
        self.update(deleted_at=timezone.now())

    def hard_delete(self)->None:
        super(CompanyQuerySet, self).delete()

class CompanyManager(models.Manager):
    def get_queryset(self):
        return CompanyQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class Company(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CompanyManager()
    all_objects = CompanyQuerySet.as_manager()

    def delete(self)->None:
        self.deleted_at=timezone.now()
        self.save()

    def hard_delete(self)->None:
        super().delete()

class GoodsQuerySet(models.QuerySet):
    def delete(self)->None:
        self.update(deleted_at=timezone.now())

    def hard_delete(self)->None:
        super().delete()


class GoodsManager(models.Manager):
    def get_queryset(self):
        return GoodsQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)
        # return super().get_queryset().filter(deleted_at__isnull=True)

    def all_data(self) -> int:
        return super().get_queryset()


class Goods(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = GoodsManager()
    all_objects = models.Manager()

    def delete(self)->None:
        self.deleted_at=timezone.now()
        self.save()

    def hard_delete(self)->None:
        super().delete()
