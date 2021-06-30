from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=255)


class Author(models.Model):
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


class Entry(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


"""
# select_relatedの練習
# クエリを実行したときに、指定された外部キーのオブジェクトも一緒にとってくる。

# select_relatedを使わない場合
>>> entry=Entry.objects.get(id=1)
(0.001) SELECT `sample2_entry`.`id`, `sample2_entry`.`author_id` FROM `sample2_entry` WHERE `sample2_entry`.`id` = 1 LIMIT 21; args=(1,)
>>> entry.author
(0.008) SELECT `sample2_author`.`id`, `sample2_author`.`hometown_id` FROM `sample2_author` WHERE `sample2_author`.`id` = 1 LIMIT 21; args=(1,)
<Author: Author object (1)>
>>> entry.author.hometown
(0.001) SELECT `sample2_city`.`id`, `sample2_city`.`name` FROM `sample2_city` WHERE `sample2_city`.`id` = 1 LIMIT 21; args=(1,)
<City: City object (1)>

# select_relatedを使った場合
>>> entry=Entry.objects.select_related('author__hometown').get(id=1)
(0.001) SELECT `sample2_entry`.`id`, `sample2_entry`.`author_id`, `sample2_author`.`id`, `sample2_author`.`hometown_id`, `sample2_city`.`id`, `sample2_city`.`name` FROM `sample2_entry` INNER JOIN `sample2_author` ON (`sample2_entry`.`author_id` = `sample2_author`.`id`) LEFT OUTER JOIN `sample2_city` ON (`sample2_author`.`hometown_id` = `sample2_city`.`id`) WHERE `sample2_entry`.`id` = 1 LIMIT 21; args=(1,)
>>> entry.author
<Author: Author object (1)>
>>> entry.author.hometown
<City: City object (1)>

"""
