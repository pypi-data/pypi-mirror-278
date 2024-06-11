from pydantic import BaseModel, Field, field_validator
from typing import List, Tuple

class Credentials(BaseModel):
    client_id: str
    client_secret: str

    @field_validator('client_id', 'client_secret')
    def not_empty(cls, v):
        if not v:
            raise ValueError('Must not be empty')
        return v


class Config(BaseModel):
    credentials: List[Credentials]
    region: str
    locale: str

    @field_validator('region')
    def valid_region(cls, v):
        valid_regions = {'us', 'eu', 'kr', 'tw', 'cn'}
        if v not in valid_regions:
            raise ValueError(f'Region must be one of {valid_regions}')
        return v

    @field_validator('locale')
    def valid_locale(cls, v):
        valid_locales = {
            'en_US', 'es_MX', 'pt_BR', 'de_DE', 'en_GB',
            'es_ES', 'fr_FR', 'it_IT', 'ru_RU', 'ko_KR',
            'zh_TW', 'zh_CN'
        }
        if v not in valid_locales:
            raise ValueError(f'Locale must be one of {valid_locales}')
        return v


class RequestParams(BaseModel):
    namespace: str
    locale: str

    @field_validator('namespace')
    def valid_namespace(cls, v):
        valid_namespaces = {
            'static-us', 'static-eu', 'static-kr', 'static-tw', 'static-cn',
            'dynamic-us', 'dynamic-eu', 'dynamic-kr', 'dynamic-tw', 'dynamic-cn',
            'Profile_modules-us', 'Profile_modules-eu', 'Profile_modules-kr', 'Profile_modules-tw', 'Profile_modules-cn'
        }
        if v not in valid_namespaces:
            raise ValueError(f'Namespace must be one of {valid_namespaces}')
        return v

    @field_validator('locale')
    def valid_locale(cls, v):
        valid_locales = {
            'en_US', 'es_MX', 'pt_BR', 'de_DE', 'en_GB',
            'es_ES', 'fr_FR', 'it_IT', 'ru_RU', 'ko_KR',
            'zh_TW', 'zh_CN'
        }
        if v not in valid_locales:
            raise ValueError(f'Locale must be one of {valid_locales}')
        return v
