# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2023/12/28 11:26
import dns.resolver


def check_domain(domain):
    """
    检测域名是否做了dns解析
    :param domain:      域名
    :return:            bool
    """
    try:
        dns.resolver.query(domain, 'A')
        return True
    except dns.resolver.NXDOMAIN:
        return False