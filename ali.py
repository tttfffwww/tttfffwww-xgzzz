import requests
import sys
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

# pip3 install aliyun-python-sdk-core
# pip3 install aliyun-python-sdk-alidns


# 阿里云相关参数
AccessKeyID = ""
AccessKeySecret = ""
DomainName = ""
ziyvming = ""

proxies = {
    "http": None,
    "https": None,
}


def printf(text):
    print(text)
    sys.stdout.flush()


def getip():
    try:
        url = "http://members.3322.org/dyndns/getip"
        r = requests.get(url, proxies=proxies)
        return r.text
    except:
        url="http://ifconfig.me/"
        r=requests.get(url,proxies=proxies)
        return r.text


def ddns(ip):
    try:
        print("正在修改%s.%s的域名解析" % (ziyvming, DomainName))
        client = AcsClient(AccessKeyID, AccessKeySecret, "cn-hangzhou")
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        request.set_PageSize("500")
        request.set_KeyWord(ziyvming)
        request.set_SearchMode("EXACT")
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))
        # print(json_data)
        OldIp = json_data["DomainRecords"]["Record"][0]["Value"]
        print("%s.%s当前解析的IP为" % (ziyvming, DomainName), OldIp)
        if OldIp == ip:
            print("IP未更改 无需更新！")
            return 0
        RecordId = json_data["DomainRecords"]["Record"][0]["RecordId"]
        print("成功查询到域名解析ID", RecordId)
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RR(ziyvming)
        request.set_RecordId(RecordId)
        request.set_Type("A")
        request.set_Value(ip)
        request.set_TTL("600")
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))
        if "RecordId" in json_data:
            print("解析修改成功！")
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        request.set_PageSize("500")
        request.set_KeyWord(ziyvming)
        request.set_SearchMode("EXACT")
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))
        # print(json_data)
        RecordIp = json_data["DomainRecords"]["Record"][0]["Value"]
        print("%s.%s当前解析的IP为" % (ziyvming, DomainName), RecordIp)
        print("IP解析更改路径： %s -> %s" % (OldIp, RecordIp))
    except:
        print("err")


if __name__ == '__main__':
    ip = getip()
    printf("当前ip为:%s" % ip)
    ddns(ip)