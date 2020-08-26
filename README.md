# Meg-Super-Resolution-Challenge

旷视人工智能开源大赛 视频超分辨率

## TODO

✅ 1.  一次性open太多文件超过linux系统限制

> OSError: [Errno 24] Too many open files

root权限下
```bash
vim /etc/security/limits.conf  
# 在最后加入  
* soft nofile 4096  
* hard nofile 4096
# 或
* - nofile 8192
```
[https://www.cnblogs.com/lenmom/p/9773093.html](https://www.cnblogs.com/lenmom/p/9773093.html)

✅ 2. 需要修改baseline，在任意GPU上运行

3. 修改Test部分代码，生成连续图片并按类分好
