
class RestAPIResult:
    def __init__(self,error:str=None,error_code:int=None,result:any=None):
        self.error=error
        self.error_code=error_code
        self.result=result
        self.status=error_code if error_code is not None else 200

class BasicResult(RestAPIResult):
    def __init__(self,error:str=None,error_code:int=None,result:any=None):
        super().__init__(error,error_code,result)


class PageResult(RestAPIResult):
    def __init__(self,error:str=None,error_code:int=None,total:int=0,pageNumber:int=1,
                 pageSize:int=None,result:list[dict]=None,stats:dict=None):
        super.__init__(error,error_code,result)

        self.total=total
        self.pageNumber=pageNumber
        self.pageSize=pageSize
        self.stats=stats

class ResultUtil:
    @staticmethod
    def parseBasicResult(result:dict) -> BasicResult:
        return BasicResult(result['error'],result['error_code'],result['result'])

    @staticmethod
    def parsePageResult(result:dict) -> PageResult:
        return PageResult(result['error'],result['error_code'],
                          result['total'],
                          result['pageNumber'] if 'pageNumber' in result.keys() else 1,
                          result['pageSize'] if 'pageSize' in result.keys() else None,
                          result['result'],
                          result['stats'] if 'stats' in result.keys() else None)

    @staticmethod
    def validate(field_value: any, error_msg: str, field_type: str = None):
        from inhand.dto.APIError import APIError
        from inhand.dto.ErrorException import ERR_CODE_400
        from inhand.utils.StringUtil import StringUtil
        if field_value is None:
            raise APIError(ERR_CODE_400, error_msg)
        if field_type == 'str':
            if str(field_value) == '':
                raise APIError(ERR_CODE_400, error_msg)
        elif field_type == 'email':
            if not StringUtil.is_valid_email(field_value):
                raise APIError(ERR_CODE_400, error_msg)

