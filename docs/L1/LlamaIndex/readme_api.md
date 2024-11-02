
# llamaindex+Internlm2 RAG实践

本文将分为以下几个部分来介绍，如何使用 LlamaIndex 来使用浦语API（以 InternStudio 的环境为例）
- 前置知识
- 环境、模型准备
- LlamaIndex HuggingFaceLLM
- LlamaIndex RAG

## 1. 前置知识
正式介绍检索增强生成（Retrieval Augmented Generation，RAG）技术以前，大家不妨想想为什么会出现这样一个技术。
给模型注入新知识的方式，可以简单分为两种方式，一种是内部的，即更新模型的权重，另一个就是外部的方式，给模型注入格外的上下文或者说外部信息，不改变它的的权重。
第一种方式，改变了模型的权重即进行模型训练，这是一件代价比较大的事情，大语言模型具体的训练过程，可以参考[InternLM2](https://arxiv.org/abs/2403.17297)技术报告。第二种方式，并不改变模型的权重，只是给模型引入格外的信息。类比人类编程的过程，第一种方式相当于你记住了某个函数的用法，第二种方式相当于你阅读函数文档然后短暂的记住了某个函数的用法。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/5a72331f-1726-4e4e-9a69-75141cfd313e)
对比两种注入知识方式，第二种更容易实现。RAG正是这种方式。它能够让基础模型实现非参数知识更新，无需训练就可以掌握新领域的知识。本次课程选用了LlamaIndex框架。LlamaIndex 是一个上下文增强的 LLM 框架，旨在通过将其与特定上下文数据集集成，增强大型语言模型（LLMs）的能力。它允许您构建应用程序，既利用 LLMs 的优势，又融入您的私有或领域特定信息。

### RAG 效果比对

如图所示，由于`xtuner`是一款比较新的框架， `浦语 API ` 训练数据库中并没有收录到它的相关信息。左图中问答均未给出准确的答案。右图未对 `浦语 API ` 进行任何增训的情况下，通过 RAG 技术实现的新增知识问答。
![image](https://github.com/user-attachments/assets/690c4b5a-aec0-480f-9bf7-42c110645ce3)

## 2. 环境、模型准备
### 2.1 配置基础环境
这里以在 [Intern Studio](https://studio.intern-ai.org.cn/) 服务器上部署LlamaIndex为例。


首先，打开 `Intern Studio` 界面，点击 **创建开发机** 配置开发机系统。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/e325d0c1-6816-4ea5-ba4a-f509bdd42323)

填写 `开发机名称` 后，点击 选择镜像 使用 `Cuda11.7-conda` 镜像，然后在资源配置中，使用 `30% A100 * 1` 的选项，然后立即创建开发机器。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/8c25b923-fda8-4af2-a4dc-2f4cf44845c9)

点击 `进入开发机` 选项。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/6bc3cde2-6309-4e14-9278-a65cd74d4a3a)

进入开发机后，创建新的conda环境，命名为 `llamaindex`，在命令行模式下运行：
```bash
conda create -n llamaindex python=3.10
```
复制完成后，在本地查看环境。
```bash
conda env list
```
结果如下所示。
```bash
# conda environments:
#
base                  *  /root/.conda
llamaindex               /root/.conda/envs/llamaindex
```

运行 `conda` 命令，激活 `llamaindex` 然后安装相关基础依赖
**python** 虚拟环境:
```bash
conda activate llamaindex
```
**安装python 依赖包**
```bash
pip install einops==0.7.0 protobuf==5.26.1
```

环境激活后，命令行左边会显示当前（也就是 `llamaindex` ）的环境名称，如下图所示:
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/bcfedc90-0d9d-4679-b1e9-4709b05711f3)

### 2.2 安装 Llamaindex
安装 Llamaindex和相关的包
```bash
conda activate llamaindex
pip install llama-index-core
pip install llama-index-llms-openai
pip install llama-index-llms-replicate
pip install llama-index-embeddings-huggingface
```

### 2.3 下载 Sentence Transformer 模型

源词向量模型 [Sentence Transformer](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2):（我们也可以选用别的开源词向量模型来进行 Embedding，目前选用这个模型是相对轻量、支持中文且效果较好的，同学们可以自由尝试别的开源词向量模型）
运行以下指令，新建一个python文件
```bash
cd ~
mkdir llamaindex_demo
mkdir model
cd ~/llamaindex_demo
touch download_hf.py
```
打开`download_hf.py` 贴入以下代码
```bash
import os

# 设置环境变量
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 下载模型
os.system('huggingface-cli download --resume-download sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 --local-dir /root/model/sentence-transformer')
```

然后，在 /root/llamaindex_demo 目录下执行该脚本即可自动开始下载：
```bash
cd /root/llamaindex_demo
conda activate llamaindex
python download_hf.py

在modelscope使用git下载词向量模型（推荐使用这个）
git clone https://www.modelscope.cn/Ceceliachenen/paraphrase-multilingual-MiniLM-L12-v2.git
```
更多关于镜像使用可以移步至 [HF Mirror](https://hf-mirror.com/) 查看。

### 2.4 下载 NLTK 相关资源
我们在使用开源词向量模型构建开源词向量的时候，需要用到第三方库 `nltk` 的一些资源。正常情况下，其会自动从互联网上下载，但可能由于网络原因会导致下载中断，此处我们可以从国内仓库镜像地址下载相关资源，保存到服务器上。
我们用以下命令下载 nltk 资源并解压到服务器上：
```bash
cd /root
git clone https://gitee.com/yzy0612/nltk_data.git  --branch gh-pages
cd nltk_data
mv packages/*  ./
cd tokenizers
unzip punkt.zip
cd ../taggers
unzip averaged_perceptron_tagger.zip
```
之后使用时服务器即会自动使用已有资源，无需再次下载

## 3. LlamaIndex 
运行以下指令，新建一个python文件
```bash
cd ~/llamaindex_demo
touch openai_llm.py
touch openai_Internlm.py
touch llamaindex_internlm.py
```
由于LlamaIndex不支持浦语API，需要自己编写浦语API代码
打开openai_llm.py 贴入以下代码
```python
import functools
from typing import (
    TYPE_CHECKING,
    Any,
    Generator,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Sequence,
    Union,
    cast,
    get_args,
    runtime_checkable,
)

import httpx
import tiktoken
from llama_index.core.base.llms.generic_utils import (
    achat_to_completion_decorator,
    acompletion_to_chat_decorator,
    astream_chat_to_completion_decorator,
    astream_completion_to_chat_decorator,
    chat_to_completion_decorator,
    completion_to_chat_decorator,
    stream_chat_to_completion_decorator,
    stream_completion_to_chat_decorator,
)
from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseAsyncGen,
    CompletionResponseGen,
    LLMMetadata,
    MessageRole,
)
from llama_index.core.bridge.pydantic import Field, PrivateAttr
from llama_index.core.callbacks import CallbackManager
from llama_index.core.constants import (
    DEFAULT_TEMPERATURE,
)
from llama_index.core.llms.callbacks import (
    llm_chat_callback,
    llm_completion_callback,
)
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.llms.llm import ToolSelection
from llama_index.core.types import BaseOutputParser, PydanticProgramMode, Model
from llama_index.llms.openai.utils import (
    O1_MODELS,
    OpenAIToolCall,
    create_retry_decorator,
    from_openai_completion_logprobs,
    from_openai_message,
    from_openai_token_logprobs,
    is_chat_model,
    is_function_calling_model,
    openai_modelname_to_contextsize,
    resolve_openai_credentials,
    to_openai_message_dicts,
    resolve_tool_choice,
    update_tool_calls,
)
from llama_index.core.bridge.pydantic import (
    BaseModel,
)

from openai import AsyncOpenAI, AzureOpenAI
from openai import OpenAI as SyncOpenAI
from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk,
    ChoiceDelta,
    ChoiceDeltaToolCall,
)
from llama_index.core.llms.utils import parse_partial_json

import llama_index.core.instrumentation as instrument

dispatcher = instrument.get_dispatcher(__name__)

if TYPE_CHECKING:
    from llama_index.core.tools.types import BaseTool

DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"


def llm_retry_decorator(f: Callable[[Any], Any]) -> Callable[[Any], Any]:
    @functools.wraps(f)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        max_retries = getattr(self, "max_retries", 0)
        if max_retries <= 0:
            return f(self, *args, **kwargs)

        retry = create_retry_decorator(
            max_retries=max_retries,
            random_exponential=True,
            stop_after_delay_seconds=60,
            min_seconds=1,
            max_seconds=20,
        )
        return retry(f)(self, *args, **kwargs)

    return wrapper


@runtime_checkable
class Tokenizer(Protocol):
    """Tokenizers support an encode function that returns a list of ints."""

    def encode(self, text: str) -> List[int]:
        ...


def force_single_tool_call(response: ChatResponse) -> None:
    tool_calls = response.message.additional_kwargs.get("tool_calls", [])
    if len(tool_calls) > 1:
        response.message.additional_kwargs["tool_calls"] = [tool_calls[0]]


class OpenAILLM(FunctionCallingLLM):
    """
    OpenAI LLM.

    Args:
        model: name of the OpenAI model to use.
        temperature: a float from 0 to 1 controlling randomness in generation; higher will lead to more creative, less deterministic responses.
        max_tokens: the maximum number of tokens to generate.
        additional_kwargs: Add additional parameters to OpenAI request body.
        max_retries: How many times to retry the API call if it fails.
        timeout: How long to wait, in seconds, for an API call before failing.
        reuse_client: Reuse the OpenAI client between requests. When doing anything with large volumes of async API calls, setting this to false can improve stability.
        api_key: Your OpenAI api key
        api_base: The base URL of the API to call
        api_version: the version of the API to call
        callback_manager: the callback manager is used for observability.
        default_headers: override the default headers for API requests.
        http_client: pass in your own httpx.Client instance.
        async_http_client: pass in your own httpx.AsyncClient instance.

    Examples:
        `pip install llama-index-llms-openai`

        ```python
        import os
        import openai

        os.environ["OPENAI_API_KEY"] = "sk-..."
        openai.api_key = os.environ["OPENAI_API_KEY"]

        from llama_index.llms.openai import OpenAI

        llm = OpenAI(model="gpt-3.5-turbo")

        stream = llm.stream("Hi, write a short story")

        for r in stream:
            print(r.delta, end="")
        ```
    """

    model: str = Field(
        default=DEFAULT_OPENAI_MODEL, description="The OpenAI model to use."
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
        ge=0.0,
        le=1.0,
    )
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate.",
        gt=0,
    )
    logprobs: Optional[bool] = Field(
        description="Whether to return logprobs per token.",
        default=None,
    )
    top_logprobs: int = Field(
        description="The number of top token log probs to return.",
        default=0,
        ge=0,
        le=20,
    )
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the OpenAI API."
    )
    max_retries: int = Field(
        default=3,
        description="The maximum number of API retries.",
        ge=0,
    )
    timeout: float = Field(
        default=60.0,
        description="The timeout, in seconds, for API requests.",
        ge=0,
    )
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="The default headers for API requests."
    )
    reuse_client: bool = Field(
        default=True,
        description=(
            "Reuse the OpenAI client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )

    api_key: str = Field(default=None, description="The OpenAI API key.")
    api_base: str = Field(description="The base URL for OpenAI API.")
    api_version: str = Field(description="The API version for OpenAI API.")
    strict: bool = Field(
        default=False,
        description="Whether to use strict mode for invoking tools/using schemas.",
    )

    _client: Optional[SyncOpenAI] = PrivateAttr()
    _aclient: Optional[AsyncOpenAI] = PrivateAttr()
    _http_client: Optional[httpx.Client] = PrivateAttr()
    _async_http_client: Optional[httpx.AsyncClient] = PrivateAttr()

    def __init__(
        self,
        model: str = DEFAULT_OPENAI_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = None,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
        reuse_client: bool = True,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        openai_client: Optional[SyncOpenAI] = None,
        async_openai_client: Optional[AsyncOpenAI] = None,
        # base class
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
        strict: bool = False,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_key, api_base, api_version = resolve_openai_credentials(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
        )

        # TODO: Temp forced to 1.0 for o1
        if model in O1_MODELS:
            temperature = 1.0

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            callback_manager=callback_manager,
            api_key=api_key,
            api_version=api_version,
            api_base=api_base,
            timeout=timeout,
            reuse_client=reuse_client,
            default_headers=default_headers,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
            strict=strict,
            **kwargs,
        )

        self._client = openai_client
        self._aclient = async_openai_client
        self._http_client = http_client
        self._async_http_client = async_http_client

    def _get_client(self) -> SyncOpenAI:
        if not self.reuse_client:
            return SyncOpenAI(**self._get_credential_kwargs())

        if self._client is None:
            self._client = SyncOpenAI(**self._get_credential_kwargs())
        return self._client

    def _get_aclient(self) -> AsyncOpenAI:
        if not self.reuse_client:
            return AsyncOpenAI(**self._get_credential_kwargs(is_async=True))

        if self._aclient is None:
            self._aclient = AsyncOpenAI(**self._get_credential_kwargs(is_async=True))
        return self._aclient

    def _get_model_name(self) -> str:
        model_name = self.model
        if "ft-" in model_name:  # legacy fine-tuning
            model_name = model_name.split(":")[0]
        elif model_name.startswith("ft:"):
            model_name = model_name.split(":")[1]
        return model_name

    def _is_azure_client(self) -> bool:
        return isinstance(self._get_client(), AzureOpenAI)

    @classmethod
    def class_name(cls) -> str:
        return "openai_llm"

    @property
    def _tokenizer(self) -> Optional[Tokenizer]:
        """
        Get a tokenizer for this model, or None if a tokenizing method is unknown.

        OpenAI can do this using the tiktoken package, subclasses may not have
        this convenience.
        """
        return tiktoken.encoding_for_model(self._get_model_name())

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=openai_modelname_to_contextsize(self._get_model_name()),
            num_output=self.max_tokens or -1,
            is_chat_model=is_chat_model(model=self._get_model_name()),
            is_function_calling_model=is_function_calling_model(
                model=self._get_model_name()
            ),
            model_name=self.model,
            # TODO: Temp for O1 beta
            system_role=MessageRole.USER
            if self.model in O1_MODELS
            else MessageRole.SYSTEM,
        )

    @llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if self._use_chat_completions(kwargs):
            chat_fn = self._chat
        else:
            chat_fn = completion_to_chat_decorator(self._complete)
        return chat_fn(messages, **kwargs)

    @llm_chat_callback()
    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self._use_chat_completions(kwargs):
            stream_chat_fn = self._stream_chat
        else:
            stream_chat_fn = stream_completion_to_chat_decorator(self._stream_complete)
        return stream_chat_fn(messages, **kwargs)

    @llm_completion_callback()
    def complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self._use_chat_completions(kwargs):
            complete_fn = chat_to_completion_decorator(self._chat)
        else:
            complete_fn = self._complete
        return complete_fn(prompt, **kwargs)

    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if self._use_chat_completions(kwargs):
            stream_complete_fn = stream_chat_to_completion_decorator(self._stream_chat)
        else:
            stream_complete_fn = self._stream_complete
        return stream_complete_fn(prompt, **kwargs)

    def _use_chat_completions(self, kwargs: Dict[str, Any]) -> bool:
        if "use_chat_completions" in kwargs:
            return kwargs["use_chat_completions"]
        return self.metadata.is_chat_model

    def _get_credential_kwargs(self, is_async: bool = False) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "base_url": self.api_base,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "http_client": self._async_http_client if is_async else self._http_client,
        }

    def _get_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        base_kwargs = {"model": self.model, "temperature": self.temperature, **kwargs}
        if self.max_tokens is not None:
            # If max_tokens is None, don't include in the payload:
            # https://platform.openai.com/docs/api-reference/chat
            # https://platform.openai.com/docs/api-reference/completions
            base_kwargs["max_tokens"] = self.max_tokens
        if self.logprobs is not None and self.logprobs is True:
            if self.metadata.is_chat_model:
                base_kwargs["logprobs"] = self.logprobs
                base_kwargs["top_logprobs"] = self.top_logprobs
            else:
                base_kwargs["logprobs"] = self.top_logprobs  # int in this case

        # can't send stream_options to the API when not streaming
        all_kwargs = {**base_kwargs, **self.additional_kwargs}
        if "stream" not in all_kwargs and "stream_options" in all_kwargs:
            del all_kwargs["stream_options"]

        return all_kwargs

    @llm_retry_decorator
    def _chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        client = self._get_client()
        message_dicts = to_openai_message_dicts(messages, model=self.model)

        if self.reuse_client:
            response = client.chat.completions.create(
                messages=message_dicts,
                stream=False,
                **self._get_model_kwargs(**kwargs),
            )
        else:
            with client:
                response = client.chat.completions.create(
                    messages=message_dicts,
                    stream=False,
                    **self._get_model_kwargs(**kwargs),
                )

        openai_message = response.choices[0].message
        role = openai_message.role
        if  not role:
            openai_message.role = MessageRole.ASSISTANT 
        message = from_openai_message(openai_message)
        openai_token_logprobs = response.choices[0].logprobs
        logprobs = None
        if openai_token_logprobs and openai_token_logprobs.content:
            logprobs = from_openai_token_logprobs(openai_token_logprobs.content)

        return ChatResponse(
            message=message,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=self._get_response_token_counts(response),
        )

    @llm_retry_decorator
    def _stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        client = self._get_client()
        message_dicts = to_openai_message_dicts(messages, model=self.model)

        def gen() -> ChatResponseGen:
            content = ""
            tool_calls: List[ChoiceDeltaToolCall] = []

            is_function = False
            for response in client.chat.completions.create(
                messages=message_dicts,
                **self._get_model_kwargs(stream=True, **kwargs),
            ):
                response = cast(ChatCompletionChunk, response)
                if len(response.choices) > 0:
                    delta = response.choices[0].delta
                else:
                    if self._is_azure_client():
                        continue
                    else:
                        delta = ChoiceDelta()

                if delta is None:
                    continue

                # check if this chunk is the start of a function call
                if delta.tool_calls:
                    is_function = True

                # update using deltas
                role = delta.role or MessageRole.ASSISTANT
                content_delta = delta.content or ""
                content += content_delta

                additional_kwargs = {}
                if is_function:
                    tool_calls = update_tool_calls(tool_calls, delta.tool_calls)
                    if tool_calls:
                        additional_kwargs["tool_calls"] = tool_calls

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    @llm_retry_decorator
    def _complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        client = self._get_client()
        all_kwargs = self._get_model_kwargs(**kwargs)
        self._update_max_tokens(all_kwargs, prompt)

        if self.reuse_client:
            response = client.completions.create(
                prompt=prompt,
                stream=False,
                **all_kwargs,
            )
        else:
            with client:
                response = client.completions.create(
                    prompt=prompt,
                    stream=False,
                    **all_kwargs,
                )
        text = response.choices[0].text

        openai_completion_logprobs = response.choices[0].logprobs
        logprobs = None
        if openai_completion_logprobs:
            logprobs = from_openai_completion_logprobs(openai_completion_logprobs)

        return CompletionResponse(
            text=text,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=self._get_response_token_counts(response),
        )

    @llm_retry_decorator
    def _stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        client = self._get_client()
        all_kwargs = self._get_model_kwargs(stream=True, **kwargs)
        self._update_max_tokens(all_kwargs, prompt)

        def gen() -> CompletionResponseGen:
            text = ""
            for response in client.completions.create(
                prompt=prompt,
                **all_kwargs,
            ):
                if len(response.choices) > 0:
                    delta = response.choices[0].text
                    if delta is None:
                        delta = ""
                else:
                    delta = ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    def _update_max_tokens(self, all_kwargs: Dict[str, Any], prompt: str) -> None:
        """Infer max_tokens for the payload, if possible."""
        if self.max_tokens is not None or self._tokenizer is None:
            return
        # NOTE: non-chat completion endpoint requires max_tokens to be set
        num_tokens = len(self._tokenizer.encode(prompt))
        max_tokens = self.metadata.context_window - num_tokens
        if max_tokens <= 0:
            raise ValueError(
                f"The prompt has {num_tokens} tokens, which is too long for"
                " the model. Please use a prompt that fits within"
                f" {self.metadata.context_window} tokens."
            )
        all_kwargs["max_tokens"] = max_tokens

    def _get_response_token_counts(self, raw_response: Any) -> dict:
        """Get the token usage reported by the response."""
        if hasattr(raw_response, "usage"):
            try:
                prompt_tokens = raw_response.usage.prompt_tokens
                completion_tokens = raw_response.usage.completion_tokens
                total_tokens = raw_response.usage.total_tokens
            except AttributeError:
                return {}
        elif isinstance(raw_response, dict):
            usage = raw_response.get("usage", {})
            # NOTE: other model providers that use the OpenAI client may not report usage
            if usage is None:
                return {}
            # Backwards compatibility with old dict type
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
        else:
            return {}

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        }

    # ===== Async Endpoints =====
    @llm_chat_callback()
    async def achat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        achat_fn: Callable[..., Awaitable[ChatResponse]]
        if self._use_chat_completions(kwargs):
            achat_fn = self._achat
        else:
            achat_fn = acompletion_to_chat_decorator(self._acomplete)
        return await achat_fn(messages, **kwargs)

    @llm_chat_callback()
    async def astream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        astream_chat_fn: Callable[..., Awaitable[ChatResponseAsyncGen]]
        if self._use_chat_completions(kwargs):
            astream_chat_fn = self._astream_chat
        else:
            astream_chat_fn = astream_completion_to_chat_decorator(
                self._astream_complete
            )
        return await astream_chat_fn(messages, **kwargs)

    @llm_completion_callback()
    async def acomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self._use_chat_completions(kwargs):
            acomplete_fn = achat_to_completion_decorator(self._achat)
        else:
            acomplete_fn = self._acomplete
        return await acomplete_fn(prompt, **kwargs)

    @llm_completion_callback()
    async def astream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        if self._use_chat_completions(kwargs):
            astream_complete_fn = astream_chat_to_completion_decorator(
                self._astream_chat
            )
        else:
            astream_complete_fn = self._astream_complete
        return await astream_complete_fn(prompt, **kwargs)

    @llm_retry_decorator
    async def _achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        aclient = self._get_aclient()
        message_dicts = to_openai_message_dicts(messages, model=self.model)

        if self.reuse_client:
            response = await aclient.chat.completions.create(
                messages=message_dicts, stream=False, **self._get_model_kwargs(**kwargs)
            )
        else:
            async with aclient:
                response = await aclient.chat.completions.create(
                    messages=message_dicts,
                    stream=False,
                    **self._get_model_kwargs(**kwargs),
                )

        openai_message = response.choices[0].message
        message = from_openai_message(openai_message)
        openai_token_logprobs = response.choices[0].logprobs
        logprobs = None
        if openai_token_logprobs and openai_token_logprobs.content:
            logprobs = from_openai_token_logprobs(openai_token_logprobs.content)

        return ChatResponse(
            message=message,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=self._get_response_token_counts(response),
        )

    @llm_retry_decorator
    async def _astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        aclient = self._get_aclient()
        message_dicts = to_openai_message_dicts(messages, model=self.model)

        async def gen() -> ChatResponseAsyncGen:
            content = ""
            tool_calls: List[ChoiceDeltaToolCall] = []

            is_function = False
            first_chat_chunk = True
            async for response in await aclient.chat.completions.create(
                messages=message_dicts,
                **self._get_model_kwargs(stream=True, **kwargs),
            ):
                response = cast(ChatCompletionChunk, response)
                if len(response.choices) > 0:
                    # check if the first chunk has neither content nor tool_calls
                    # this happens when 1106 models end up calling multiple tools
                    if (
                        first_chat_chunk
                        and response.choices[0].delta.content is None
                        and response.choices[0].delta.tool_calls is None
                    ):
                        first_chat_chunk = False
                        continue
                    delta = response.choices[0].delta
                else:
                    if self._is_azure_client():
                        continue
                    else:
                        delta = ChoiceDelta()
                first_chat_chunk = False

                if delta is None:
                    continue

                # check if this chunk is the start of a function call
                if delta.tool_calls:
                    is_function = True

                # update using deltas
                role = delta.role or MessageRole.ASSISTANT
                content_delta = delta.content or ""
                content += content_delta

                additional_kwargs = {}
                if is_function:
                    tool_calls = update_tool_calls(tool_calls, delta.tool_calls)
                    if tool_calls:
                        additional_kwargs["tool_calls"] = tool_calls

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    @llm_retry_decorator
    async def _acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        aclient = self._get_aclient()
        all_kwargs = self._get_model_kwargs(**kwargs)
        self._update_max_tokens(all_kwargs, prompt)

        if self.reuse_client:
            response = await aclient.completions.create(
                prompt=prompt,
                stream=False,
                **all_kwargs,
            )
        else:
            async with aclient:
                response = await aclient.completions.create(
                    prompt=prompt,
                    stream=False,
                    **all_kwargs,
                )

        text = response.choices[0].text
        openai_completion_logprobs = response.choices[0].logprobs
        logprobs = None
        if openai_completion_logprobs:
            logprobs = from_openai_completion_logprobs(openai_completion_logprobs)

        return CompletionResponse(
            text=text,
            raw=response,
            logprobs=logprobs,
            additional_kwargs=self._get_response_token_counts(response),
        )

    @llm_retry_decorator
    async def _astream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        aclient = self._get_aclient()
        all_kwargs = self._get_model_kwargs(stream=True, **kwargs)
        self._update_max_tokens(all_kwargs, prompt)

        async def gen() -> CompletionResponseAsyncGen:
            text = ""
            async for response in await aclient.completions.create(
                prompt=prompt,
                **all_kwargs,
            ):
                if len(response.choices) > 0:
                    delta = response.choices[0].text
                    if delta is None:
                        delta = ""
                else:
                    delta = ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()

    def _prepare_chat_with_tools(
        self,
        tools: List["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_choice: Union[str, dict] = "auto",
        strict: Optional[bool] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Predict and call the tool."""
        tool_specs = [tool.metadata.to_openai_tool() for tool in tools]

        # if strict is passed in, use, else default to the class-level attribute, else default to True`
        if strict is not None:
            strict = strict
        else:
            strict = self.strict

        if self.metadata.is_function_calling_model:
            for tool_spec in tool_specs:
                if tool_spec["type"] == "function":
                    tool_spec["function"]["strict"] = strict
                    tool_spec["function"]["parameters"][
                        "additionalProperties"
                    ] = False  # in current openai 1.40.0 it is always false.

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        messages = chat_history or []
        if user_msg:
            messages.append(user_msg)

        return {
            "messages": messages,
            "tools": tool_specs or None,
            "tool_choice": resolve_tool_choice(tool_choice) if tool_specs else None,
            **kwargs,
        }

    def _validate_chat_with_tools_response(
        self,
        response: ChatResponse,
        tools: List["BaseTool"],
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
        """Validate the response from chat_with_tools."""
        if not allow_parallel_tool_calls:
            force_single_tool_call(response)
        return response

    def get_tool_calls_from_response(
        self,
        response: "ChatResponse",
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
        """Predict and call the tool."""
        tool_calls = response.message.additional_kwargs.get("tool_calls", [])

        if len(tool_calls) < 1:
            if error_on_no_tool_call:
                raise ValueError(
                    f"Expected at least one tool call, but got {len(tool_calls)} tool calls."
                )
            else:
                return []

        tool_selections = []
        for tool_call in tool_calls:
            if not isinstance(tool_call, get_args(OpenAIToolCall)):
                raise ValueError("Invalid tool_call object")
            if tool_call.type != "function":
                raise ValueError("Invalid tool type. Unsupported by OpenAI")

            # this should handle both complete and partial jsons
            try:
                argument_dict = parse_partial_json(tool_call.function.arguments)
            except ValueError:
                argument_dict = {}

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.id,
                    tool_name=tool_call.function.name,
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections

    @dispatcher.span
    def structured_predict(
        self, *args: Any, llm_kwargs: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> BaseModel:
        """Structured predict."""
        llm_kwargs = llm_kwargs or {}
        llm_kwargs["tool_choice"] = (
            "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
        )
        # by default structured prediction uses function calling to extract structured outputs
        # here we force tool_choice to be required
        return super().structured_predict(*args, llm_kwargs=llm_kwargs, **kwargs)

    @dispatcher.span
    async def astructured_predict(
        self, *args: Any, llm_kwargs: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> BaseModel:
        """Structured predict."""
        llm_kwargs = llm_kwargs or {}
        llm_kwargs["tool_choice"] = (
            "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
        )
        # by default structured prediction uses function calling to extract structured outputs
        # here we force tool_choice to be required
        return await super().astructured_predict(*args, llm_kwargs=llm_kwargs, **kwargs)

    @dispatcher.span
    def stream_structured_predict(
        self, *args: Any, llm_kwargs: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Generator[Union[Model, List[Model]], None, None]:
        """Stream structured predict."""
        llm_kwargs = llm_kwargs or {}
        llm_kwargs["tool_choice"] = (
            "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
        )
        # by default structured prediction uses function calling to extract structured outputs
        # here we force tool_choice to be required
        return super().stream_structured_predict(*args, llm_kwargs=llm_kwargs, **kwargs)

    @dispatcher.span
    def stream_structured_predict(
        self, *args: Any, llm_kwargs: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Generator[Union[Model, List[Model]], None, None]:
        """Stream structured predict."""
        llm_kwargs = llm_kwargs or {}
        llm_kwargs["tool_choice"] = (
            "required" if "tool_choice" not in llm_kwargs else llm_kwargs["tool_choice"]
        )
        # by default structured prediction uses function calling to extract structured outputs
        # here we force tool_choice to be required
        return super().stream_structured_predict(*args, llm_kwargs=llm_kwargs, **kwargs)

```

打开openai_Internlm.py 贴入以下代码
```python
from typing import Any, Optional, Sequence, Union

from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseAsyncGen,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.bridge.pydantic import Field
from llama_index.core.constants import DEFAULT_CONTEXT_WINDOW
from llama_index.core.base.llms.generic_utils import (
    async_stream_completion_response_to_chat_response,
    completion_response_to_chat_response,
    stream_completion_response_to_chat_response,
)
from llama_index.llms.openai.base import OpenAI, Tokenizer
from transformers import AutoTokenizer
from openai_llm import OpenAILLM

class OpenAIInternlm(OpenAILLM):
    """OpenaAILike LLM.

    OpenAILike is a thin wrapper around the OpenAI model that makes it compatible with
    3rd party tools that provide an openai-compatible api.

    Currently, llama_index prevents using custom models with their OpenAI class
    because they need to be able to infer some metadata from the model name.

    NOTE: You still need to set the OPENAI_BASE_API and OPENAI_API_KEY environment
    variables or the api_key and api_base constructor arguments.
    OPENAI_API_KEY/api_key can normally be set to anything in this case,
    but will depend on the tool you're using.

    Examples:
        `pip install llama-index-llms-openai-like`

        ```python
        from llama_index.llms.openai_like import OpenAILike

        llm = OpenAILike(model="my model", api_base="https://hostname.com/v1", api_key="fake")

        response = llm.complete("Hello World!")
        print(str(response))
        ```
    """

    context_window: int = Field(
        default=32768,
        description=LLMMetadata.model_fields["context_window"].description,
    )
    is_chat_model: bool = Field(
        default=False,
        description=LLMMetadata.model_fields["is_chat_model"].description,
    )
    is_function_calling_model: bool = Field(
        default=False,
        description=LLMMetadata.model_fields["is_function_calling_model"].description,
    )
    tokenizer: Union[Tokenizer, str, None] = Field(
        default=None,
        description=(
            "An instance of a tokenizer object that has an encode method, or the name"
            " of a tokenizer model from Hugging Face. If left as None, then this"
            " disables inference of max_tokens."
        ),
    )

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens or -1,
            is_chat_model=self.is_chat_model,
            is_function_calling_model=self.is_function_calling_model,
            model_name=self.model,
        )

    @property
    def _tokenizer(self) -> Optional[Tokenizer]:
        if isinstance(self.tokenizer, str):
            return AutoTokenizer.from_pretrained(self.tokenizer)
        return self.tokenizer

    @classmethod
    def class_name(cls) -> str:
        return "OpenAILike"

    def complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        """Complete the prompt."""
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return super().complete(prompt, **kwargs)

    def stream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        """Stream complete the prompt."""
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return super().stream_complete(prompt, **kwargs)

    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        """Chat with the model."""
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = self.complete(prompt, formatted=True, **kwargs)
            return completion_response_to_chat_response(completion_response)

        return super().chat(messages, **kwargs)

    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = self.stream_complete(prompt, formatted=True, **kwargs)
            return stream_completion_response_to_chat_response(completion_response)

        return super().stream_chat(messages, **kwargs)

    # -- Async methods --

    async def acomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        """Complete the prompt."""
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return await super().acomplete(prompt, **kwargs)

    async def astream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        """Stream complete the prompt."""
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        return await super().astream_complete(prompt, **kwargs)

    async def achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        """Chat with the model."""
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = await self.acomplete(prompt, formatted=True, **kwargs)
            return completion_response_to_chat_response(completion_response)

        return await super().achat(messages, **kwargs)

    async def astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = await self.astream_complete(
                prompt, formatted=True, **kwargs
            )
            return async_stream_completion_response_to_chat_response(
                completion_response
            )

        return await super().astream_chat(messages, **kwargs)

```


打开llamaindex_internlm.py 贴入以下代码
```python
url =  "https://internlm-chat.intern-ai.org.cn/puyu/api/v1/"
key = "eyJ0eXBlIjoiSl...请填写准确的 token！"

# https://internlm.intern-ai.org.cn/api/document  获取api key的地址

from llama_index.core.llms import ChatMessage
from openai_Internlm import OpenAIInternlm
from llama_index.legacy.callbacks import CallbackManager

# Create an instance of CallbackManager
callback_manager = CallbackManager()

# llm = InternlmChat(model="internlm2.5-latest",api_key=key,callback_manager=callback_manager)
llm = OpenAIInternlm(api_base=url, api_key=key, model="internlm2.5-latest", is_chat_model=True,callback_manager=callback_manager)

rsp = llm.chat(messages=[ChatMessage(content="xtuner是什么？")])
print(rsp)
```
之后运行
```bash
conda activate llamaindex
cd ~/llamaindex_demo/
python llamaindex_internlm.py
```
结果为：
<img width="370" alt="image" src="https://github.com/user-attachments/assets/d892f5c9-1243-4b2d-8551-8aa483d2f986">

回答的效果并不好，并不是我们想要的xtuner。
## 4. LlamaIndex RAG
安装 `LlamaIndex` 词嵌入向量依赖
```bash
conda activate llamaindex
pip install llama-index-embeddings-huggingface llama-index-embeddings-instructor
```
运行以下命令，获取知识库
```bash
cd ~/llamaindex_demo
mkdir data
cd data
git clone https://github.com/InternLM/xtuner.git
mv xtuner/README_zh-CN.md ./
```
运行以下指令，新建一个python文件
```bash
cd ~/llamaindex_demo
touch llamaindex_RAG.py
```
打开`llamaindex_RAG.py`贴入以下代码
```python

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.legacy.callbacks import CallbackManager

from openai_Internlm import OpenAIInternlm

url =  "https://internlm-chat.intern-ai.org.cn/puyu/api/v1/"
key = "eyJ0eXBlIjoiSl...请填写准确的 token！"

# Create an instance of CallbackManager
callback_manager = CallbackManager()

#初始化一个HuggingFaceEmbedding对象，用于将文本转换为向量表示
embed_model = HuggingFaceEmbedding(
#指定了一个预训练的sentence-transformer模型的路径
    model_name="/root/model/paraphrase-multilingual-MiniLM-L12-v2"
)
#将创建的嵌入模型赋值给全局设置的embed_model属性，
#这样在后续的索引构建过程中就会使用这个模型。
Settings.embed_model = embed_model

llm = OpenAIInternlm(api_base=url, api_key=key, model="internlm2.5-latest", is_chat_model=True,callback_manager=callback_manager)
Settings.llm = llm

#从指定目录读取所有文档，并加载数据到内存中
documents = SimpleDirectoryReader("/root/llamaindex_demo/data").load_data()
#创建一个VectorStoreIndex，并使用之前加载的文档来构建索引。
# 此索引将文档转换为向量，并存储这些向量以便于快速检索。
index = VectorStoreIndex.from_documents(documents)
# 创建一个查询引擎，这个引擎可以接收查询并返回相关文档的响应。
query_engine = index.as_query_engine()
response = query_engine.query("xtuner是什么?")

print(response)
```
之后运行
```bash
conda activate llamaindex
cd ~/llamaindex_demo/
python llamaindex_RAG.py
```
结果为：
<img width="518" alt="image" src="https://github.com/user-attachments/assets/7a976178-2301-47eb-b53b-168cb0ef90a3">


借助RAG技术后，就能获得我们想要的答案了。

## 5. LlamaIndex web
运行之前首先安装依赖

```shell
pip install streamlit
```

运行以下指令，新建一个python文件

```bash
cd ~/llamaindex_demo
touch app.py
```

打开`app.py`贴入以下代码
```python
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from openai_Internlm import OpenAIInternlm
from llama_index.legacy.callbacks import CallbackManager

url =  "https://internlm-chat.intern-ai.org.cn/puyu/api/v1/"
key = "eyJ0eXBlIjoiSl...请填写准确的 token！"

# Create an instance of CallbackManager
callback_manager = CallbackManager()

st.set_page_config(page_title="llama_index_demo", page_icon="🦜🔗")
st.title("llama_index_demo")

# 初始化模型
@st.cache_resource
def init_models():
    embed_model = HuggingFaceEmbedding(
        model_name="/root/model/paraphrase-multilingual-MiniLM-L12-v2"
    )
    Settings.embed_model = embed_model

    llm = OpenAIInternlm(api_base=url, api_key=key, model="internlm2.5-latest", is_chat_model=True,callback_manager=callback_manager)
    
    Settings.llm = llm

    documents = SimpleDirectoryReader("/root/llamaindex_demo/data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    return query_engine

# 检查是否需要初始化模型
if 'query_engine' not in st.session_state:
    st.session_state['query_engine'] = init_models()

def greet2(question):
    response = st.session_state['query_engine'].query(question)
    return response

      
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的助手，有什么我可以帮助你的吗？"}]    

    # Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的助手，有什么我可以帮助你的吗？"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama_index_response(prompt_input):
    return greet2(prompt_input)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Gegenerate_llama_index_response last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama_index_response(prompt)
            placeholder = st.empty()
            placeholder.markdown(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
```

之后运行
```bash
streamlit run app.py
```

然后在命令行点击，红框里的url。

![image](https://github.com/user-attachments/assets/15625b3b-ef47-4848-b448-de0b7668b9fc)


即可进入以下网页，然后就可以开始尝试问问题了。

![image](https://github.com/user-attachments/assets/ff270976-cd2f-4b75-bc83-4bad0060ff86)


询问结果为：

![image](https://github.com/user-attachments/assets/04df06bd-d7ec-45aa-b4fc-83e37cd896c1)


## 6. 小结
恭喜你，成功通关本关卡！继续加油！你成功使用 LlamaIndex 运行了浦语API，并实现了知识库的构建与检索。这为管理和利用大规模知识库提供了强大的工具和方法。接下来，可以进一步优化和扩展功能，以满足更复杂的需求。

## 7. 作业
作业请访问[作业](./task.md)。
