from django.db import models


# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()


class Creative(models.Model):
    name = models.CharField(max_length=255, default="")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


"""
# prefetch_relatedの練習
逆参照?を取りに行ってくれる。
一度全部Campaignを引っ張ってきて、campaign.idのリストをwhere inして引っ張ってきている様子

# prefetch_relatedを使わなかった場合
>>> for campaign in Campaign.objects.all():
...     print(campaign.creative_set.all())
... 
(0.001) SELECT `sample3_campaign`.`id`, `sample3_campaign`.`name`, `sample3_campaign`.`created_at` FROM `sample3_campaign`; args=()
(0.003) SELECT `sample3_creative`.`id`, `sample3_creative`.`name`, `sample3_creative`.`campaign_id`, `sample3_creative`.`created_at` FROM `sample3_creative` WHERE `sample3_creative`.`campaign_id` = 1 LIMIT 21; args=(1,)
<QuerySet [<Creative: Creative object (1)>, <Creative: Creative object (2)>, <Creative: Creative object (3)>]>
(0.002) SELECT `sample3_creative`.`id`, `sample3_creative`.`name`, `sample3_creative`.`campaign_id`, `sample3_creative`.`created_at` FROM `sample3_creative` WHERE `sample3_creative`.`campaign_id` = 2 LIMIT 21; args=(2,)
<QuerySet [<Creative: Creative object (4)>, <Creative: Creative object (5)>]>


# prefetch_relatedを使った場合

>>> for campaign in Campaign.objects.all().prefetch_related("creative_set"):
...     print(campaign.creative_set.all())
... 
(0.001) SELECT `sample3_campaign`.`id`, `sample3_campaign`.`name`, `sample3_campaign`.`created_at` FROM `sample3_campaign`; args=()
(0.001) SELECT `sample3_creative`.`id`, `sample3_creative`.`name`, `sample3_creative`.`campaign_id`, `sample3_creative`.`created_at` FROM `sample3_creative` WHERE `sample3_creative`.`campaign_id` IN (1, 2); args=(1, 2)
<QuerySet [<Creative: Creative object (1)>, <Creative: Creative object (2)>, <Creative: Creative object (3)>]>
<QuerySet [<Creative: Creative object (4)>, <Creative: Creative object (5)>]>


# filterも組み合わせて使える。

"""
