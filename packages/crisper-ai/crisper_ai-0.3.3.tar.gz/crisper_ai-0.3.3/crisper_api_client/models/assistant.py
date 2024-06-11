from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.knowledge_source import KnowledgeSource


T = TypeVar("T", bound="Assistant")


@_attrs_define
class Assistant:
    """
    Attributes:
        knowledge_sources (List['KnowledgeSource']):
        name (str):
    """

    knowledge_sources: List["KnowledgeSource"]
    name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        knowledge_sources = []
        for knowledge_sources_item_data in self.knowledge_sources:
            knowledge_sources_item = knowledge_sources_item_data.to_dict()
            knowledge_sources.append(knowledge_sources_item)

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "knowledge_sources": knowledge_sources,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.knowledge_source import KnowledgeSource

        d = src_dict.copy()
        knowledge_sources = []
        _knowledge_sources = d.pop("knowledge_sources")
        for knowledge_sources_item_data in _knowledge_sources:
            knowledge_sources_item = KnowledgeSource.from_dict(knowledge_sources_item_data)

            knowledge_sources.append(knowledge_sources_item)

        name = d.pop("name")

        assistant = cls(
            knowledge_sources=knowledge_sources,
            name=name,
        )

        assistant.additional_properties = d
        return assistant

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
