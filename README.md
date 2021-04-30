# spider-service
爬虫

1. 启动 mongo

1. qidong proxy_pool

1. Make sure that Scrapyd has been installed and started on all of your hosts. 
Note that if you want to visit your Scrapyd server remotely, you have to manually set the bind_address to bind_address = 0.0.0.0 and restart Scrapyd to make it visible externally.
```sh
scrapyd 
```

2. Install ScrapydWeb on one of your hosts via the pip install scrapydweb command.


3. Start ScrapydWeb via command scrapydweb. (a config file would be generated for customizing settings on the first startup.)

Enable HTTP basic auth (optional).

Visit http://127.0.0.1:5000, and log in with the USERNAME/PASSWORD above.

## 工作爬虫
1. 启动mongo
```
rm -rf /data/db/* 
/usr/local/mongodb/bin/mongod --dbpath=/data/db/ --logpath=/logs/mongodb.log --logappend &

### 获取板块列表
- 未完成

### 获取行业列表


```