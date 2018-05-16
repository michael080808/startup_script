import os
import sys
import smtplib
import configparser

from email.header import Header
from email.mime.text import MIMEText

# 设置接收方和发送方邮件地址和名称
send_addr = ''
recv_addr = ''
send_name = ''
recv_name = ''

# 设置用户名和密码
username = ''
password = ''

# 设置POP、IMAP、SMTP服务器
pop_server = ''
imap_server = ''
smtp_server = ''

# 设置POP、IMAP、SMTP服务器端口号
pop_port = 995
imap_port = 993
smtp_port = 25

try:
    import netifaces
except ImportError:
    try:
        os.system('pip install netifaces || easy_install netifaces')
    except OSError:
        print("CANNOT install netifaces, Aborted!")
        sys.exit(1)
    import netifaces


# 获取本地MAC, IP地址, 转化成HTML表格形式
def address():
    table = '<div>At This Moment, Your Network Information is Here!</div>'
    table += '<br><br><br>'
    table += '<div>Basic Network Information is Here!</div>'
    table += '<div style="display:flex; justify-content:flex-start;">'
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)

        table += '<div><table>'
        table += '''<tr style="background-color:black">
                        <td colspan="2">
                            <span style=\'color:white;font-weight:bold;\'>Interface Name: %s</span>
                        </td>
                    </tr>''' % interface

        for addr in addrs:
            if addr is netifaces.AF_PACKET:
                # MAC地址
                table += '''<tr style="background-color:red">
                                <td colspan="2">
                                    <span style=\'font-weight:bold;\'>This Part is MAC Address</span>
                                </td>
                            </tr>'''
                # MAC地址表格
                for infos in addrs[addr]:
                    table += '''<tr>
                                    <th colspan="2">MAC Address %d</th>
                                </tr>''' % (addrs[addr].index(infos) + 1)
                    for info in infos:
                        table += '''<tr>
                                        <th>%s</th>
                                        <td>%s</td>
                                    </tr>''' % (info.upper(), infos[info].upper())
            elif addr is netifaces.AF_INET:
                # IPv4地址
                table += '''<tr style="background-color:yellow">
                                <td colspan="2">
                                    <span style=\'font-weight:bold;\'>This Part is IPv4 Address</span>
                                </td>
                            </tr>'''
                # IPv4表格
                for infos in addrs[addr]:
                    table += '''<tr>
                                    <th colspan="2">IPv4 Address %d</th>
                                </tr>''' % (addrs[addr].index(infos) + 1)
                    for info in infos:
                        table += '''<tr>
                                        <th>%s</th>
                                        <td>%s</td>
                                    </tr>''' % (info.upper(), infos[info].upper())
            elif addr is netifaces.AF_INET6:
                # IPv6地址
                table += '''<tr style="background-color:green">
                                <td colspan="2">
                                    <span style=\'font-weight:bold;\'>This Part is IPv6 Address</span>
                                </td>
                            </tr>'''
                # IPv6表格
                for infos in addrs[addr]:
                    table += '''<tr>
                                    <th colspan="2">IPv6 Address %d</th>
                                </tr>''' % (addrs[addr].index(infos) + 1)
                    for info in infos:
                        table += '''<tr>
                                        <th>%s</th>
                                        <td>%s</td>
                                    </tr>''' % (info.upper(), infos[info].upper())
            else:
                pass

        table += '</table></div>'
    table += '</div>'
    table += '<br><br><br>'
    table += '<div>Gateway Information is Here!</div>'
    table += '<div style="display:flex; justify-content:flex-start;">'
    gateways = netifaces.gateways()
    for gateway in gateways:
        if gateway is 'default':
            table += '<div><table>'

            table += '''<tr style="background-color:black">
                            <td colspan="2">
                                <span style=\'color:white;font-weight:bold;\'>Default Gateway</span>
                            </td>
                        </tr>'''
            for gateway_type in gateways[gateway]:
                if gateway_type is netifaces.AF_INET:
                    table += '''<tr>
                                    <th>Gateway Type</th>
                                    <td>IPv4</td>
                                </tr>'''
                    table += '''<tr>
                                    <th>Gateway Address</th>
                                    <td>%s</td>
                                </tr>''' % gateways[gateway][gateway_type][0]
                    table += '''<tr>
                                    <th>Gateway Interface</th>
                                    <td>%s</td>
                                </tr>''' % gateways[gateway][gateway_type][1]
                elif gateway_type is netifaces.AF_INET6:
                    table += '''<tr>
                                    <th>Gateway Type</th>
                                    <td>IPv6</td>
                                </tr>'''
                    table += '''<tr>
                                    <th>Gateway Address</th>
                                    <td>%s</td>
                                </tr>''' % gateways[gateway][gateway_type][0]
                    table += '''<tr>
                                    <th>Gateway Interface</th>
                                    <td>%s</td>
                                </tr>''' % gateways[gateway][gateway_type][1]
                else:
                    pass

            table += '</table></div>'
        elif gateway is netifaces.AF_INET:
            table += '<div><table>'
            table += '''<tr style="background-color:black">
                            <td colspan="2">
                                <span style=\'color:white;font-weight:bold;\'>IPv4 Gateway</span>
                            </td>
                        </tr>'''
            for gateway_info in gateways[gateway]:
                table += '''<tr>
                                <th colspan="2">IPv4 Gateway %d</th>
                            </tr>''' % (gateways[gateway].index(gateway_info) + 1)
                table += '''<tr>
                                <th>Gateway Address</th>
                                <td>%s</td>
                            </tr>''' % gateway_info[0]
                table += '''<tr>
                                <th>Gateway Interface</th>
                                <td>%s</td>
                            </tr>''' % gateway_info[1]
                table += '''<tr>
                                <th>Default Gateway?</th>
                                <td>%s</td>
                            </tr>''' % gateway_info[2]
            table += '</table></div>'
        elif gateway is netifaces.AF_INET6:
            table += '<div><table>'
            table += '''<tr style="background-color:black">
                            <td colspan="2">
                                <span style=\'color:white;font-weight:bold;\'>IPv6 Gateway</span>
                            </td>
                        </tr>'''
            for gateway_info in gateways[gateway]:
                table += '''<tr>
                                <th colspan="2">IPv6 Gateway %d</th>
                            </tr>''' % (gateways[gateway].index(gateway_info) + 1)
                table += '''<tr>
                                <th>Gateway Address</th>
                                <td>%s</td>
                            </tr>''' % gateway_info[0]
                table += '''<tr>
                                <th>Gateway Interface</th>
                                <td>%s</td>
                            </tr>''' % gateway_info[1]
                table += '''<tr>
                                <th>Default Gateway?</th>
                                <td>%s</td>
                            </tr>''' % gateway_info[2]
            table += '</table></div>'
        else:
            pass
    table += '</div>'

    return table


# 递送电子邮件
def deliver():
    message = MIMEText(address(), 'html', 'utf-8')
    message['From'] = Header('%s <%s>' % (send_name, send_addr), 'utf-8')
    message['To'] = Header('%s <%s>' % (recv_name, recv_addr), 'utf-8')
    message['Subject'] = Header('IP Monitor Notice', 'utf-8')

    smtp_poster = smtplib.SMTP(smtp_server, smtp_port)
    try:
        smtp_poster.ehlo_or_helo_if_needed()
        smtp_poster.starttls()
        smtp_poster.login(username, password)
        smtp_poster.sendmail(send_addr, recv_addr, message.as_string())
        print('Success to Send IP Address!')
    except smtplib.SMTPException as e:
        print('Fail to Send IP Address! Error Information: \n')
        raise e
    finally:
        smtp_poster.close()


if __name__ == '__main__':
    cf = configparser.ConfigParser()
    cf.read('e-mail.conf')

    pop_server = cf.get('e-mail server', 'pop_server')
    imap_server = cf.get('e-mail server', 'imap_server')
    smtp_server = cf.get('e-mail server', 'smtp_server')

    pop_port = int(cf.get('e-mail port', 'pop_port'))
    imap_port = int(cf.get('e-mail port', 'imap_port'))
    smtp_port = int(cf.get('e-mail port', 'smtp_port'))

    username = cf.get('e-mail user', 'username')
    password = cf.get('e-mail user', 'password')

    send_addr = cf.get('e-mail sender', 'send_addr')
    send_name = cf.get('e-mail sender', 'send_name')
    recv_addr = cf.get('e-mail recver', 'recv_addr')
    recv_name = cf.get('e-mail recver', 'recv_name')

    deliver()
