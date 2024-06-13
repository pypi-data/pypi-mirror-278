from typing import Dict, List, Union


class Utils:
    
    class Response:
        
        class ListMessage:
            
            def __init__(self, RESPONSE: Dict[str, str]) -> None:
                self.id: str = RESPONSE.get('id')
                self.threadId: str = RESPONSE.get('threadId')
        
        class ListEmail:
            
            def __init__(self, RESPONSE: Dict[str, Union[List[Dict[str, str]], str]]) -> None:
                self.resultSizeEstimate: int = RESPONSE.get('resultSizeEstimate')
                if self.resultSizeEstimate > 0:
                    self.messages: Union[List[Utils.Response.ListMessage], None]  = [Utils.Response.ListMessage(Message) for Message in RESPONSE.get('messages')]
                else:
                    self.messages: Union[List[Utils.Response.ListMessage], None] = None
        
        class Headers:
            
            def __init__(self, headers: Dict[str, any]) -> None:
                self.name: str   = headers.get('name')
                self.value: str  = headers.get('value')
        
        class Body:
            
            def __init__(self, body: Dict[str, any]) -> None:
                self.size: int = body.get('size')
                self.data: str = body.get('data')
        
        class Parts:
            
            def __init__(self, body: Dict[str, any]) -> None:
                self.body: Utils.Response.Body = Utils.Response.Body(body)
        
        class Payload:
            
            def __init__(self, payload: Dict[str, any]) -> None:
                self.headers: List[Utils.Response.Headers] = [Utils.Response.Headers(headers) for headers in payload.get('headers')]
                try:
                    self.body: Union[Utils.Response.Body, None] = Utils.Response.Body(payload.get('body'))
                except:
                    self.body: Union[Utils.Response.Body, None] = None
                try:
                    self.parts: Union[List[Utils.Response.Parts], None] = [Utils.Response.Parts(parts) for parts in payload.get('parts')]
                except: self.parts: Union[List[Utils.Response.Parts], None] = None

        class Contents:
            
            def __init__(self, RESPONSE: Dict[str, Union[List[Dict[str, str]], str, Dict[str, any]]]) -> None:
                self.labelIds: List[str] = RESPONSE.get('labelIds')
                self.snippet: str = RESPONSE.get('snippet')
                self.payload: Utils.Response.Payload = Utils.Response.Payload(RESPONSE.get('payload'))
        
        class Unread:
            
            def __init__(self, RESPONSE: Dict[str, any]) -> None:
                self.id: str = RESPONSE.get('id')
                self.threadId: str = RESPONSE.get('threadId')
                self.labelIds: List[str] = RESPONSE.get('threadId')