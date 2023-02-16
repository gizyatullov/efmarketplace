from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union, Type

from tortoise import models, Model

__all__ = [
    'BaseDAO',
]


class BaseDAO(ABC):
    """Class for accessing to tortoise model."""

    @abstractmethod
    def get_model(self) -> models.Model:
        raise NotImplementedError

    async def record_exists(self, record_id: int) -> bool:
        obj = await self.get_by_id(record_id)
        return True if obj else False

    async def create(self, data: Dict[str, Any]) -> Any:
        """
        Add single dummy to session.
        """
        model = self.get_model()
        return await model.create(**data)

    async def update_by_models(self, models: list):
        """
        objects: list[model]
        """
        for model in models:
            await model.save()

    async def update(self, id_: int, data: Dict[str, Any]) -> models.Model:
        model = self.get_model()
        obj = await model.get(id=id_)

        for k, v in data.items():
            setattr(obj, k, v)

        await obj.save()
        return obj

    async def get_by_id(self, id: int) -> models.Model:
        model = self.get_model()
        return await model.get(id=id)

    async def get_all(self, limit: int, offset: int, with_count=False) -> Union[
        tuple[list[Model], int], list[Model]]:
        """
        Get all models with limit/offset pagination.
        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :param with_count: count of all records.
        :return: stream of dummies.
        """
        model = self.get_model()
        data = await model.all().offset(offset).limit(limit)
        if with_count:
            count = await model.all().count()
            return data, count

        return data

    async def _get_all_with_prefetch(
        self,
        limit: int,
        offset: int,
        prefetch: str,
        with_count=False,
    ) -> Union[tuple[list[Model], int], list[Model]]:
        model = self.get_model()
        data = await model.all().offset(offset).limit(limit).prefetch_related(prefetch)
        if with_count:
            count = await model.all().count()
            return data, count

        return data

    async def filter(self, data: Dict[str, Any]) -> List[models.Model]:
        """
        Get specific model.
        """
        model = self.get_model()
        query = model.all()
        query = query.filter(**data)
        return await query

    async def filter_with_order(self, filter_data: Dict[str, Any], order_col_name: str):
        model = self.get_model()
        query = model.all().filter(**filter_data).order_by(order_col_name)
        return await query

    async def filter_with_prefetch(
        self,
        data: Dict[str, Any],
        prefetch: str,
    ) -> List[models.Model]:
        """
        Get specific model.
        """
        model = self.get_model()
        query = model.all().filter(**data).prefetch_related(prefetch)
        return await query

    async def delete_by_id(self, id: int) -> Any:
        obj = await self.get_by_id(id)
        return await obj.delete()

    async def exclude(self, data: Dict[str, Any]):
        model = self.get_model()
        return await model.exclude(**data)
