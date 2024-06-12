class ObjectSetupUtil:

    @staticmethod
    def setup_object(body, **kwargs) -> object:
        for k, v in kwargs.items():
            setattr(body, k, v)
        return body

    @staticmethod
    def set_up_query_params(**kwargs) -> str:
        return '?'+'&'.join(f'{k}={v}' for k, v in kwargs.items() if v is not None)
