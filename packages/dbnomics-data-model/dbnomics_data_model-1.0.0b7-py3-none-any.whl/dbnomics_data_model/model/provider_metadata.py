from dataclasses import dataclass
from typing import Self

from dbnomics_data_model.model.identifiers import ProviderCode
from dbnomics_data_model.model.url import PublicUrl

__all__ = ["ProviderMetadata"]


@dataclass(kw_only=True)
class ProviderMetadata:
    attribution: str | None = None
    code: ProviderCode
    description: str | None = None
    name: str | None = None
    region: str | None = None
    terms_of_use: PublicUrl | None = None
    website: PublicUrl

    @classmethod
    def create(
        cls,
        code: str,
        *,
        attribution: str | None = None,
        description: str | None = None,
        name: str | None = None,
        region: str | None = None,
        terms_of_use: str | None = None,
        website: str,
    ) -> Self:
        code = ProviderCode.parse(code)

        if terms_of_use is not None:
            terms_of_use = PublicUrl.parse(terms_of_use)

        website = PublicUrl.parse(website)

        return cls(
            attribution=attribution,
            code=code,
            description=description,
            name=name,
            region=region,
            terms_of_use=terms_of_use,
            website=website,
        )
