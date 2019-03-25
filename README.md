Big Data Audit
==============

By [Shou C](https://github.com/shouc/)

[![Build Status](https://camo.githubusercontent.com/f8bbfdc05d49bbdad27dba5693bccade8cd36e12/68747470733a2f2f7472617669732d63692e6f72672f6a696d656e6269616e2f446174614d696e696e672e7376673f6272616e63683d6d6173746572)](https://travis-ci.org/kotobukki/BDA)
[![Support](https://camo.githubusercontent.com/4a42460f88f172b10e916fec11857648a8a2f2c8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f706c6174666f726d2d6f73782532466c696e757825324677696e646f77732d677265656e2e737667)](https://travis-ci.org/kotobukki/BDA)
[![Supportpython](https://camo.githubusercontent.com/352488c0cbba0e8f6da11ae0761444dd0c93489c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d322e372d626c75652e737667)](https://travis-ci.org/kotobukki/BDA)

Installation
-----
```
git clone https://github.com/shouc/BDA.git
pip install -r requirements.txt
```

If you want to use MySQL, you should install MySQLdb

Usage
-----
The entrance file of the program is main.py

You can use the following command to see the usage
```
$python main.py -h
usage: main.py [-h] {Hadoop,Spark, MySQL} ...

This is a tool for detectiong the security problem of hadoop!

positional arguments:
  {Hadoop,Spark,MySQL}  commands
    Hadoop        Check the security of Hadoop
    Spark         Check the security of Spark
    MySQL         Check MySQL database setting

optional arguments:
  -h, --help      show this help message and exit
```


MySQL
-----
```
python main.py MySQL -h
usage: main.py MySQL [-h] [--host [HOST]] [--port [PORT]] username password

positional arguments:
  username       the username of MySQL
  password       the password of MySQL

optional arguments:
  -h, --help     show this help message and exit
  --host [HOST]  the host of MySQL, default: 127.0.0.1
  --port [PORT]  the port of MySQL, default: 3306
```

An example of MySQL database with credential root:root
```
python main.py MySQL root root
[Info]: Checking password...
[Warning]: Password is weak
[Info]: Checking useless databases...
[Warning]: Have useless DB information_schema
[Warning]: Have useless DB mysql
[Info]: Checking useless or abandoned users...
[Pass]: Have no obsolete account
[Info]: Checking if --secure-file-priv is enabled...
[Pass]: --secure-file-priv is enabled
[Info]: Check selected user privilege (1/2)...
[Pass]: All the settings are approriate!
[Info]: Check selected user privilege (2/2)...
[Pass]: All the settings are appropriate!
```
Checks:
* weak password
* useless database
* abandoned users
* --secure-file-priv option
* 'test' user privilege

Hadoop
------
You could still use `-h` to see the usage
```
python main.py Hadoop -h
usage: main.py Hadoop [-h] confFolder

positional arguments:
  confFolder  the dir of Hadoop configuration files

optional arguments:
  -h, --help  show this help message and exit
```

`confFolder`is the folder for config files of Hadoop. It could be the `conf` folder when installing(like `/usr/local/hadoop/conf/hadoop/`), you can also copy these files to the specific folder but remind that filename should be the same as in hadoop.json, for example, the following content is system default file for checking known security factor's file in JSON.

```json
{
  "authentication": {
    "core-site": [
      {
        "hadoop.security.authentication": "kerberos",
        "reason": "Suggest to authenticate user by using kerberos!"
      }
    ]
  },
  "authorization": {
    "core-site": [
      {
        "fs.permissions.enabled": "true",
        "reason": "Suggest to enable the permission control for fs!"
      },
      {
        "hadoop.security.authorization": "true",
        "reason": "Suggest to enable authorization for every user!"
      }
    ]
  },
  "acl": {
    "hdfs-site": [
      {
        "dfs.namenode.acls.enabled": "true",
        "reason": "Suggest to enable acl for user!"
      }
    ]
  },
  "encry": {
    "hdfs-site": [
      {
        "dfs.encryption.key.provider.uri": "*",
        "reason": "Suggest to encrypt data!"
      }
    ]
  }
}
```
Core-site is the checking filename, next level is the setting, it 's father level like `encry`means chacking encrypted security questions. 

This file users could add or delet by themselves

With this setting and run the script
```
$ python main.py Hadoop ./hadoop
[Info]: Begining to check security: authentication
[Info]: >> Check file: core-site.xml
[Pass]: Your hadoop.security.authentication setting is safe!
[Info]: Begining to check security: encry
[Info]: >> Check file: hdfs-site.xml
[Warning]: Suggest to encrypt data! Set: dfs.encryption.key.provider.uri=*
[Info]: Begining to check security: authorization
[Info]: >> Check file: core-site.xml
[Warning]: Suggest to enable authorization for every user! Set: hadoop.security.authorization=true
[Info]: Begining to check security: acl
[Info]: >> Check file: hdfs-site.xml
[Warning]: Suggest to enable acl for user! Set: dfs.namenode.acls.enabled=true
```

Spark
-----
It's much as same as Hadoop, you need to point to the setting folder, but difference is that Spark's defalt setting file has only one `spark-defaults.conf`, DO NOT copy to other folder.

As same as Hadoop checking , it provides a setting that can be configured. It's in the root directory of Spark and named `security.ini`.

Example：
```
$ python main.py Spark ./spark/
[Info]: Start to check the security of spark...
[Warning]: Suggest to add option spark.authenticate = true if your spark runs on standalone mode
[Warning]: Suggest to add option spark.authenticate.secret if your spark runs on yarn mode
[Warning]: Suggest to set option spark.ssl.enable = true
[Warning]: Suggest to set option spark.eventlog.enabled = true

```
