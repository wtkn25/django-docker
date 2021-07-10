from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Hero(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    benevolence_factor = models.PositiveSmallIntegerField(
        help_text="How benevolent this hero is?", default=50
    )


"""
hero_qs = Hero.objects.filter(
    category=OuterRef("pk")
).order_by("-benevolence_factor")

Category.objects.all().annotate(
    most_benevolent_hero=Subquery(
        hero_qs.values('name')[:1]
    )
)

SELECT "entities_category"."id",
       "entities_category"."name",

  (SELECT U0."name"
   FROM "entities_hero" U0
   WHERE U0."category_id" = ("entities_category"."id")
   ORDER BY U0."benevolence_factor" DESC
   LIMIT 1) AS "most_benevolent_hero"
FROM "entities_category"
"""
