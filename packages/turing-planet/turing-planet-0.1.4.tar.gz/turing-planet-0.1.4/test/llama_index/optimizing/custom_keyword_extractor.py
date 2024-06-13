from typing import Any, Dict, List, Optional, Sequence, cast

from llama_index.core import PromptTemplate
from llama_index.core.async_utils import DEFAULT_NUM_WORKERS, run_jobs
from llama_index.core.extractors import BaseExtractor
from llama_index.core.llms import LLM
from llama_index.core.schema import BaseNode, TextNode
from llama_index.core.service_context_elements.llm_predictor import LLMPredictor
from pydantic import Field

DEFAULT_KEYWORD_GEN_TMPL = """
根据给出的文档内容，提取唯一的标题，最多不超过{keywords}个，每个标题使用空格隔开。

文档内容
{context_str}

"""


class MyKeywordExtractor(BaseExtractor):
    """Keyword extractor. Node-level extractor. Extracts
    `excerpt_keywords` metadata field.

    Args:
        llm_predictor (Optional[LLMPredictor]): LLM predictor
        keywords (int): number of keywords to extract
    """

    llm_predictor: LLMPredictor = Field(
        description="The LLMPredictor to use for generation."
    )
    prompt_template: str = Field(
        default=DEFAULT_KEYWORD_GEN_TMPL,
        description="Prompt template to use when generating keyword.",
    )
    keywords: int = Field(
        default=5, description="The number of keywords to extract.", gt=0
    )

    def __init__(
            self,
            llm: Optional[LLM] = None,
            # TODO: llm_predictor arg is deprecated
            llm_predictor: Optional[LLMPredictor] = None,
            prompt_template: str = DEFAULT_KEYWORD_GEN_TMPL,
            keywords: int = 5,
            num_workers: int = DEFAULT_NUM_WORKERS,
            **kwargs: Any,
    ) -> None:
        """Init params."""
        if keywords < 1:
            raise ValueError("num_keywords must be >= 1")

        if llm is not None:
            llm_predictor = LLMPredictor(llm=llm)
        elif llm_predictor is None and llm is None:
            llm_predictor = LLMPredictor()

        super().__init__(
            llm_predictor=llm_predictor,
            prompt_template=prompt_template,
            keywords=keywords,
            num_workers=num_workers,
            **kwargs,
        )

    @classmethod
    def class_name(cls) -> str:
        return "KeywordExtractor"

    async def _aextract_keywords_from_node(self, node: BaseNode) -> Dict[str, str]:
        """Extract keywords from a node and return it's metadata dict."""
        if self.is_text_node_only and not isinstance(node, TextNode):
            return {}

        # TODO: figure out a good way to allow users to customize keyword template
        prompt = PromptTemplate(template=self.prompt_template)
        keywords = await self.llm_predictor.apredict(prompt, context_str=cast(TextNode, node).text,
                                                     keywords=self.keywords)

        return {"excerpt_keywords": keywords.strip()}

    async def aextract(self, nodes: Sequence[BaseNode]) -> List[Dict]:
        keyword_jobs = []
        for node in nodes:
            keyword_jobs.append(self._aextract_keywords_from_node(node))

        metadata_list: List[Dict] = await run_jobs(
            keyword_jobs, show_progress=self.show_progress, workers=self.num_workers
        )

        return metadata_list
