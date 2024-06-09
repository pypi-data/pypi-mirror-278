from .whois import whois 
from .whois.parser import WhoisError 


def Whois(domain:str) -> dict: 
    return dict(whois(domain))

    # whois(domain, command=True, executable='whois') # 使用系统的命令行客户端