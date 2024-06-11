from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.knowledge_source_content_type import KnowledgeSourceContentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="KnowledgeSource")


@_attrs_define
class KnowledgeSource:
    """
    Attributes:
        content_type (KnowledgeSourceContentType): * `pdf` - pdf
            * `csv` - csv
            * `text` - text
        text (Union[Unset, str]):
        url (Union[Unset, str]):
    """

    content_type: KnowledgeSourceContentType
    text: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content_type = self.content_type.value

        text = self.text

        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_type": content_type,
            }
        )
        if text is not UNSET:
            field_dict["text"] = text
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content_type = KnowledgeSourceContentType(d.pop("content_type"))

        text = d.pop("text", UNSET)

        url = d.pop("url", UNSET)

        knowledge_source = cls(
            content_type=content_type,
            text=text,
            url=url,
        )

        knowledge_source.additional_properties = d
        return knowledge_source

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
