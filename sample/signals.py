from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Company

@receiver(post_save, sender=Company)
def post_soft_delete_company(sender, **kwargs):
    company = kwargs['instance']
    if company.deleted_at is not None:
        company.goods_set.all().delete()
    print(kwargs)

# pre_delete.connect(pre_delete_company, dispatch_uid="my_unique_identifier")


