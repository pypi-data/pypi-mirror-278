import abc

from bayesline.api._src.equity.api import AsyncBayeslineEquityApi, BayeslineEquityApi


class BayeslineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def equity(self) -> BayeslineEquityApi: ...


class AsyncBayeslineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def equity(self) -> AsyncBayeslineEquityApi: ...
