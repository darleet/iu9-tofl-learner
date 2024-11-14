from pydantic import BaseModel


class MembershipRequest(BaseModel):
    word: str


class MembershipResponse(BaseModel):
    response: bool


class EquivalenceRequest(BaseModel):
    main_prefixes: str
    non_main_prefixes: str
    suffixes: str
    table: str


class EquivalenceResponse(BaseModel):
    type: bool | None
    response: str | None
