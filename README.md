# Django on Docker
 DjangoをDocker上で開発するためのサンプルプログラム

# uWSGI起動方法
uwsgi.iniファイルを用意したのでそれを指定して実行する
```commandline
uwsgi --ini config/uwsgi.ini
```

 # テスト実行方法
 テスト実行用のtest_settings.pyを指定する。parallelの指定もしたい
```
python manage.py test --settings=config.test_settings
```