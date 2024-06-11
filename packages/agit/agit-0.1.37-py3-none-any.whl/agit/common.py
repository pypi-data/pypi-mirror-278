#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/10 11:04:36
@Author  :   ChenHao
@Description  :   
@Contact :   jerrychen1990@gmail.com
'''

from typing import Any, Dict, Generator, List, Optional
from pydantic import BaseModel, Field


class Usage(BaseModel):
    prompt_tokens: Optional[int] = Field(description="输入token数量", default=None)
    completion_tokens: Optional[int] = Field(description="输出token数量", default=None)
    total_tokens: Optional[int] = Field(description="输入输出token数量总和", default=None)


class Perf(BaseModel):
    first_token_latency: Optional[float] = Field(description="第一个token的延迟,单位s", default=None)
    total_cost: Optional[float] = Field(description="输出所有内容总耗时,单位s", default=None)
    decode_speed: Optional[float] = Field(description="prompt_tokens/encode_cost, tokens/s", default=None)
    encode_speed: Optional[float] = Field(description="completion_tokens/decode_cost, tokens/s", default=None)
    overall_speed: Optional[float] = Field(description="completion_tokens/total_cost, tokens/s", default=None)


class ToolCall(BaseModel):
    tool_call_id: str = Field(description="工具调用ID,用于跟踪调用链")
    name: str = Field(description="工具名称")
    parameters: Dict[str, Any] = Field(description="工具调用的参数")
    extra_info: dict = Field(description="额外的信息", default=dict())
    resp: Any = Field(description="工具执行的返回结果,为执行时为None", default=None)

    def to_markdown(self):
        return f"**[调用工具]**: {self.name} **[参数]**: {self.parameters} **[返回结果]**: {self.resp}"

    def to_assistant_message(self):
        return f"调用工具: {self.name}, 参数: {self.parameters}, 返回结果: {self.resp}"


class LLMResp(BaseModel):
    content: Optional[str | Generator] = Field(description="模型的回复，字符串或者生成器", default=None)
    image: Optional[str] = Field(description="图片URL", default=None)
    tool_calls: Optional[list[ToolCall]] = Field(description="工具调用列表", default=list())
    usage: Optional[Usage] = Field(description="token使用情况", default=None)
    perf: Optional[Perf] = Field(description="性能指标", default=None)
    details: Optional[dict] = Field(description="请求模型的细节信息", default=dict())

    # def get_perf(self) -> Perf:
    #     if not isinstance(self.content, str):
    #         self.content = "".join(self.content)
    #         # print(f"{self.content=}")
    #     assert self.usage is not None, "usage is None, can't get perf"
    #     # print(self.usage)

    #     total_cost = time.time()-self.details["st"]
    #     overall_speed = self.usage.total_tokens / total_cost
    #     perf_dict = dict(total_cost=total_cost, overall_speed=overall_speed)
    #     first_token_latency = self.details.get("first_token_latency")
    #     if first_token_latency:
    #         encode_speed = self.usage.prompt_tokens / first_token_latency
    #         decode_speed = self.usage.completion_tokens / (total_cost - first_token_latency)
    #         perf_dict.update(encode_speed=encode_speed, decode_speed=decode_speed, first_token_latency=first_token_latency)
    #     return Perf(**perf_dict)


class LLMError(Exception):
    status_code: int
    message: str

    def __init__(self, status_code, message: str, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.status_code}, {self.message!r})"


class Parameter(BaseModel):
    name: str = Field(description="参数名称")
    type: str = Field(description="参数类型")
    description: str = Field(description="参数描述")
    required: bool = Field(description="是否必填")


class ToolDesc(BaseModel):

    name: str = Field(..., description="工具名称")
    description: str = Field(..., description="工具描述")
    parameters: List[Parameter] = Field(..., description="工具参数")

    def to_markdown(self):
        tool_info = f"**[名称]**:{self.name}\n\n**[描述]**:{self.description}\n\n"
        param_infos = []
        for parameter in self.parameters:
            param_infos.append(
                f"- **[参数名]**:{parameter.name}\n\n **[类型]**:{parameter.type}\n\n **[描述]**:{parameter.description}\n\n **[必填]**:{parameter.required}")
        param_infos = "\n\n".join(param_infos)
        return tool_info + param_infos
