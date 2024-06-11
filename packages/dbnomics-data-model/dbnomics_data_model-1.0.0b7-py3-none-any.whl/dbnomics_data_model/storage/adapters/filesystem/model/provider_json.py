from dataclasses import dataclass

from dbnomics_data_model.model import ProviderMetadata

from .base_json_model import BaseJsonObjectModel


@dataclass(kw_only=True)
class ProviderJson(BaseJsonObjectModel):
    """Model for provider.json.

    Contains provider metadata.
    """

    code: str
    website: str

    attribution: str | None = None
    description: str | None = None
    name: str | None = None
    region: str | None = None
    terms_of_use: str | None = None

    @classmethod
    def from_domain_model(cls, provider_metadata: ProviderMetadata) -> "ProviderJson":
        return cls(
            attribution=provider_metadata.attribution,
            description=provider_metadata.description,
            code=provider_metadata.code,
            name=provider_metadata.name,
            region=provider_metadata.region,
            terms_of_use=provider_metadata.terms_of_use,
            website=provider_metadata.website,
        )

    def to_domain_model(self) -> ProviderMetadata:
        return ProviderMetadata.create(
            self.code,
            attribution=self.attribution,
            description=self.description,
            name=self.name,
            region=self.region,
            terms_of_use=self.terms_of_use,
            website=self.website,
        )
