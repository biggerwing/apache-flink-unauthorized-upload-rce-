# apache-flink-unauthorized-upload-rce-
Apache Flink未授权访问上传导致的RCE漏洞 | apache flink unauthorized upload rce

# 简单用法
python3 script.py ip port command

# 漏洞详细信息
1. Apache Flink 控制台默认情况下存在未授权访问
2. 在Submit New Job处可添加上传jar包并在服务端执行
3. 如果上传恶意的jar包，可拿下服务器的权限
4. 该漏洞官方并未承认，官方只说这是其一个功能。但该功能会被坏人利用

# 漏洞修复方案
网络上流传的影响版本只是在1.9.1以下的版本，是因为当时该漏洞刚出来的时候，最新版本为1.9.1，
但现在的新版本已经远远超过了1.9.1，但目前官方并未出相关补丁或解决措施，实际测试中发现影响更多的版本
1. 如果该服务是非必要服务，可以将其停用
2. 如果无法停用受漏洞影响的业务，可尝试添加主机防火墙(iptables/firewalld)，只允许受信任的IP连接Dashboard
3. 如果以上都做不到，可尝试修改其后端代码，禁止用户上传jar包(因需要环境，具体改法以后给出)
