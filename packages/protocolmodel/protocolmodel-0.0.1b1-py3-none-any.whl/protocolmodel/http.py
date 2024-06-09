from typing import Union,Any,Dict
import base64
import io
from http.client import LineTooLong,HTTPMessage,HTTPException
from http import HTTPStatus
import http
from urllib.parse import urlparse,parse_qs
from werkzeug.datastructures import FileStorage
from pydantic import BaseModel
from werkzeug.formparser import FormDataParser
from werkzeug.http import parse_options_header
from pydantic import field_validator,HttpUrl,AnyUrl
import json
from io import BytesIO
import typing
from typing import Literal,Optional
from typing import List

def get_mimetype_and_options(headers: dict) -> typing.Tuple[str, dict]:
    """ get mimetype from headers """
    content_type = headers.get('Content-Type')
    if content_type:
        return typing.cast(typing.Tuple[str, dict], parse_options_header(content_type))
    return '', {}

def get_content_length(headers: dict) -> typing.Optional[int]:
    """ get content-length from headers """
    content_length = headers.get('Content-Length',0)
    return max(0, int(content_length))


def json_parser(body: bytes, *args) -> dict:
    return json.loads(body.decode('utf-8'))

def multi_part_parser(body: [bytes|str], headers: Dict = None):
    """ multi part parser """
    headers = headers or {}
    mimetype, options = get_mimetype_and_options(headers)
    content_length = get_content_length(headers)
    parser = FormDataParser()
    return parser.parse(
        BytesIO(body),
        mimetype,
        content_length,
        options
    )


class File(BaseModel):
    data: bytes
    mimetype: str
    filename: str
    name: str

    class Config:
        json_encoders = {
            bytes: lambda v: base64.b64encode(v).decode('utf-8')
        }

    @field_validator('data',mode="before")
    @classmethod
    def base64_decode(cls, v: Union[str,bytes]) -> bytes:
        if isinstance(v, str):
            return base64.b64decode(v)
        return v

class HTTPRequest(BaseModel):
    """
    Attributes:
        method (str): request method
        host(str): request host
        http_version(str): http version
        url (str): request url
        path (str): request path
        headers(dict): request heades
        scheme(str): request shcema
        port(int): request port
        content(bytes):
    """
    http_version: Literal["HTTP/1.1","HTTP/0.9","HTTP/1.0", "HTTP/2","HTTP/2.0"] = "HTTP/1.0"
    scheme: Literal["http","https"] = None
    method: str
    host: str = None
    url: Optional[HttpUrl] = None
    port: int = None
    path: str
    headers: Dict[str,str]
    content: bytes = b''



    @classmethod
    def parse_from(cls,raw: str, url: Optional[str] = None) -> 'HTTPRequest':
        """ parse from raw """
        parser = HTTPRequestParser()
        result = parser.parse_raw(
            http_raw=raw,
            url=url
        )
        return result

    @classmethod
    def prase_from_url(cls, url: str) -> 'HTTPRequest':
        headers = {
            "Host": "www.baidu.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Accept-Language": "en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36",
            "Connection": "close",
            "Cache-Control": "max-age=0",
        }
        parsed = urlparse(url)
        headers["Host"] = parsed.netloc
        return cls(
            method="GET",
            url=url,
            headers=headers,
            path=f"{parsed.path}?{parsed.query}"
        )


    class Config:
        json_encoders = {
            bytes: lambda v: base64.b64encode(v).decode('utf-8')
        }

    @field_validator('content',mode="before")
    @classmethod
    def base64_decode(cls, v: Union[str,bytes]) -> bytes:
        if isinstance(v, str):
            return base64.b64decode(v)
        return v


    @property
    def is_form_data(self) -> bool:
        if "application/x-www-form-urlencoded" in self.content_type or "multipart/form-data" in self.content_type:
            return True

        else:
            return False

    @property
    def hostname(self) -> str:
        if self.port in [443, 80]:
            hostname = f"{self.host}"
        else:
            hostname = f"{self.host}:{self.port}"
        return hostname


    @property
    def form(self) -> Optional[Dict[str,str]]:
        if self.is_form_data:
            _,form,_ = multi_part_parser(self.content,self.headers)
            return dict(form)

    @property
    def files(self) -> List[File]:
        result = []
        if self.is_form_data:
            _,_,files = multi_part_parser(self.content,self.headers)
            for item in files.values():
                item: FileStorage
                result.append(
                    File(
                        data=item.stream.read(),
                        mimetype=item.mimetype,
                        filename=item.filename,
                        name=item.name
                    )
                )

        return result



    @property
    def text(self):
        return bytes.decode(self.content)

    @property
    def cookies(self) -> Dict[str,str]:
        cookie_str = self.headers.get("Cookie", "")
        cookies = {}
        if cookie_str:
            for item in cookie_str.split(";"):
                k = item.split("=")[0].strip()
                v = item.split("=")[1].strip()
                cookies[k] = v
        return cookies

    @property
    def content_length(self):
        return get_content_length(self.headers) or len(self.content)

    @property
    def content_type(self) -> str:
        return self.headers.get("Content-Type","")

    @property
    def query(self) -> Dict[str,str]:
        """ parse query """
        parsed_url = urlparse(self.path)
        query_dict = parse_qs(parsed_url.query)
        query_dict = {k: v[0] for k, v in query_dict.items()}
        return query_dict


    @property
    def raw(self) -> str:
        return http_request_raw(
            method=self.method,
            path=str(self.path),
            body=self.text,
            headers=self.headers,
            http_version=self.http_version
        )


    def init_host_info(self):
        """ shcema, host ,hostname,port """
        if self.url is not None:

            parsed = urlparse(str(self.url))
            self.scheme = parsed.scheme
            self.host = parsed.hostname
            if parsed.port: self.port = parsed.port
        else:
            host: str = self.headers.get("Host")
            if not host: raise HttpRequestRawParseError("not 'Host' found in http headers")
            split_list = host.split(":")
            self.host = split_list[0]
            if len(split_list) == 2:
                self.port = int(split_list[1])
                if not self.scheme:
                    if self.port in [443, 8443]:
                        self.scheme = "https"
                    else:
                        self.scheme = "http"
            else:
                self.scheme = self.schema or "http"  # type: ignore
                if self.scheme == "https":
                    self.port = 443
                else:
                    self.port = 80


    def model_post_init(self, __context: Any) -> None:
        self.init_host_info()
        if self.path.startswith("/"):
            self.url = self.url or f"{self.scheme}://{self.hostname}{self.path}"
        else:
            self.url = self.url or f"{self.scheme}://{self.hostname}/{self.path}"


def http_request_raw(method:str,path:str,body:str,headers:dict,http_version:str = "HTTP/1.1"):
    """
    generate http request raw

    Args:
        method:
        path:
        body:
        headers:
        http_version:

    Returns:

    """
    CRLF = "\r\n"
    http_raw = ""
    http_raw += f"{method} {path} {http_version}{CRLF}"
    for key, value in headers.items():
        http_raw += f"{key}: {value}{CRLF}"
    http_raw += f"{CRLF}"
    if body != None:
        http_raw += f"{body}"
    return http_raw

def http_response_raw(headers:dict,status_code: Union[str,int],text:str,http_version:str = "HTTP/1.1"):
    """
    generate http response raw

    Args:
        headers:
        status_code:
        text:
        http_version:

    Returns:

    """
    CRLF = "\r\n"
    http_raw = ""
    http_raw += f"{http_version} {status_code}{CRLF}"
    for key, value in headers.items():
        http_raw += f"{key}: {value}{CRLF}"
    http_raw += f"{CRLF}"
    http_raw += f"{text}"
    return http_raw


class HttpRequestRawParseError(Exception): pass
class HttpResponseRawParseError(Exception): pass

class HTTPRequestParser:
    """ http raw parser """
    default_request_version = "HTTP/0.9"
    protocol_version = "HTTP/1.0"

    def parse_raw(self,http_raw: Union[bytes, str], url: str = None) -> HTTPRequest:
        """
        parse http raw to `HttpRequest`

        Args:
            http_raw: http request raw
            url: url

        Returns:
            HttpRequest: `HttpRequest` object

        Raises:
            HttpRawParseError: paser error
            HTTPException:

        Examples:
            >>> http_raw = '''GET /static/../../../../etc/passwd HTTP/1.1
            ... Host: 127.0.0.1:8002
            ... Accept-Encoding: gzip, deflate, br
            ... Accept: */*
            ... Accept-Language: en-US;q=0.9,en;q=0.8
            ... User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36
            ... Connection: close
            ... Cache-Control: max-age=0 '''
            >>> http_request_parser = HTTPRequestParser()
            >>> http_request = http_request_parser.parse_raw(http_raw)
            >>> http_request.model_dump()

        """
        if type(http_raw) == str:
            http_raw = http_raw.encode()
        rfile = io.BytesIO(http_raw)
        raw_requestline = rfile.readline()
        request_version = self.default_request_version
        requestline = str(raw_requestline, 'iso-8859-1')
        requestline = requestline.rstrip('\r\n')
        words = requestline.split()
        if len(words) == 0:
            raise HTTPException(f"Invalid HTTP Parse {requestline}")
        if len(words) >= 3:  # Enough to determine protocol version
            version = words[-1]
            if not version.startswith('HTTP/'):
                raise HttpRequestRawParseError("version not startswith HTTP")
            base_version_number = version.split('/', 1)[1]
            version_number = base_version_number.split(".")
            if len(version_number) != 2:
                raise HttpRequestRawParseError("version number != 2")
            version_number = int(version_number[0]), int(version_number[1])
            if version_number >= (2, 0):
                raise HTTPException(HTTPStatus.HTTP_VERSION_NOT_SUPPORTED,"Invalid HTTP version (%s)" % base_version_number)
            request_version = version
        if not 2 <= len(words) <= 3:
            raise HTTPException(HTTPStatus.BAD_REQUEST,"Bad request syntax (%r)" % requestline)
        method, path = words[:2]
        headers = http.client.parse_headers(rfile,_class=HTTPMessage)
        if not headers:
            raise ValueError("没有headers")
        content = rfile.read()
        return HTTPRequest(
            method=method,
            path=path,
            headers=dict(headers),
            content=content,
            url=url,
            http_version=request_version # type: ignore
        )


class HTTPResponse(BaseModel):
    """
    Attributes:
        status_code(int): http response status code
        mimetype(str): http response mimetype
    """
    status: int
    headers: Dict[str,str]
    data: bytes = b''



    @property
    def content_length(self) -> int:
        return len(self.data)


    @classmethod
    def parse_from(cls, raw: str,verfiy_data_length: bool = False) -> 'HTTPResponse':
        parser = HTTPResponseParser()
        return parser.parse_raw(http_raw=raw, verify_data=verfiy_data_length)


    class Config:
        json_encoders = {
            bytes: lambda v: base64.b64encode(v).decode('utf-8')
        }

    @field_validator('data',mode="before")
    @classmethod
    def base64_decode(cls, v: Union[str,bytes]) -> bytes:
        if isinstance(v, str):
            return base64.b64decode(v)
        return v



    @property
    def mime_type(self) -> Optional[str]:
        content_type = self.headers.get('Content-Type') or ""
        mimetype = content_type.split(";", maxsplit=2)[0]
        if mimetype: return mimetype

    @property
    def text(self):
        return bytes.decode(self.data)
    @property
    def raw(self) -> str:
        return http_response_raw(
            headers=self.headers,
            status_code=self.status,
            text=self.text
        )


class _HttpResponseHanlder(http.client.HTTPResponse):
    def __init__(self,http_raw: bytes): # type: ignore
        self.fp  = io.BufferedReader(io.BytesIO(http_raw)) #type: ignore
        _UNKNOWN = "_UNKNOWN"
        self.debuglevel = 0
        self._method = None
        self.headers = self.msg = None # type: ignore
        self.version = _UNKNOWN  # type: ignore
        self.status = _UNKNOWN  # type: ignore
        self.reason = _UNKNOWN  # Reason-Phrase
        self.chunked = _UNKNOWN  # type: ignore
        self.chunk_left = _UNKNOWN  # type: ignore
        self.length = _UNKNOWN  # type: ignore
        self.will_close = _UNKNOWN  # type: ignore

class HTTPResponseParser:
    def parse_raw(self, http_raw: Union[bytes, str], verify_data: bool = False) -> HTTPResponse:
        """
        parse http raw

        Args:
            http_raw:
            verify_data(bool): Whether to verify data length

        Returns:
            HTTPResponse: http response

        Raises:
            HttpRequestRawParseError:

        """
        r = _HttpResponseHanlder(http_raw.encode())
        try:
            r.begin()
            if verify_data:
                data = r.read()
            else:
                data = r.fp.read()
            result = HTTPResponse(
                status=r.status,
                content_length=r.length or len(data),
                headers=dict(r.headers),
                data=data
            )
            return result
        except http.client.HTTPException as e:
            raise HttpRequestRawParseError(e)


def build_http_reqeust(method: str, path: str,headers: dict,content: bytes, url: Optional[str] = None) -> HTTPRequest:
    return HTTPRequest(
        method=method,
        path=path,
        headers=headers,
        content=content,
        url=url
    )

def build_http_response(status_code: int, data: bytes, headers: dict) -> HTTPResponse:
    result = HTTPResponse(
        status=status_code,
        headers=headers,
        data=data
    )
    return result