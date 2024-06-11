import textwrap
from typing import List
import json
class StringUtil:
    @staticmethod
    def fecth_string(s) -> (str,str):
        if len(s) <= 256:
            return s,None
        else:
            head = s[:256]
            tail = s[256:]
            last_period = head.rfind('.')
            last_newline = head.rfind('\n')
            if last_period != -1 or last_newline != -1:
                end = max(last_period, last_newline)
                tail = head[end + 1:] + tail
                head = head[:end + 1]
            return head,tail
    @staticmethod
    def split_long_str(s) -> list[str]:
        chunks = []
        head, tail = StringUtil.fecth_string(s)
        if (head is not None and head.rstrip() != ''):
            chunks.append(head)
        while tail is not None:
            head, tail = StringUtil.fecth_string(tail)
            if (head is not None and head.rstrip() != ''):
                chunks.append(head)
        return chunks

    @staticmethod
    def is_valid_email(email):
        import re
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(email_regex, email) is not None

    @staticmethod
    def convert_encoding(input_str, input_encoding='iso-8859-1', output_encoding='utf-8'):
        # 将输入字符串从输入编码转换为字节
        byte_str = input_str.encode(input_encoding)

        # 将字节从输入编码转换为输出编码
        output_str = byte_str.decode(output_encoding)

        return output_str
if __name__ == '__main__':
    s="""
    The Zoho SalesIQ REST API uses the OAuth 2.0 protocol to authorize and authenticate calls. OAuth is an industry open standard for authorization. It provides secure access to protected resources, thereby reducing the hassle of asking for a username and a password every time you log in.
    In your request for access, you can request a refresh token to be returned along with the access token. A refresh token provides your app access to Rest APIs even when the user is not logged in. To request a refresh token, add access_type=offline to the authentication request.

The Prompt=consent will always generate the refresh token. The maximum number of refresh tokens is 20. Once the limit is reached, the first refresh token in terms of time will be deleted.

The Access Tokens have limited validity. In most general cases, the access tokens expire in an hour. Until then, the access token has unlimited usage. Once it expires, your app will have to use the refresh token to request a new access token.

For this new request, the parameters to be included are,
    """

    chuncks = StringUtil.split_long_str(s)
    for i, chunk in enumerate(chuncks):
        print(f"Chunk {i+1}:\n{chunk}\n")
