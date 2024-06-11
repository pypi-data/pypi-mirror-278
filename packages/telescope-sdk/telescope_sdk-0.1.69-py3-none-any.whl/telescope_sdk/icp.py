from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from telescope_sdk.common import TelescopeBaseType
from telescope_sdk.locations import FilterableLocation
from telescope_sdk.company import CompanySizeRange, FoundedYearRange, RevenueRange


class ExampleCompany(BaseModel):
    id: str
    name: str


class TypedCompanyTagType(str, Enum):
    INDUSTRY_TAGS = "industry_tags"
    TARGET_CUSTOMER_INDUSTRY_TAGS = "target_customer_industry_tags"
    TECHNOLOGY_TAGS = "technology_tags"
    COMPANY_TYPE_TAGS = "company_type_tags"
    PRODUCT_SERVICES_TAGS = "products_services_tags"
    BUSINESS_MODEL = "business_model"
    STAGE = "stage"


class TypedCompanyTag(BaseModel):
    keyword: str = Field(description="The keyword, e.g. `b2b`, `saas`, `startup`, `rna-sequencing`")
    type: TypedCompanyTagType = Field(
        description=f"Type of the keyword. Allowed values: [{', '.join([f'{e.value}' for e in TypedCompanyTagType])}]. "
        "Can only be one of those allowed types."
    )


class SpecialCriterionSupportStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTLY_SUPPORTED = "PARTLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"


class SpecialCriterionTargetEntity(str, Enum):
    PERSON = "PERSON"
    COMPANY = "COMPANY"


class SpecialCriterionMappedDataPoint(BaseModel):
    data_point: str
    arguments_json: Optional[str]


class SpecialCriterion(BaseModel):
    original_user_input: Optional[str]
    text: str
    target_entity: SpecialCriterionTargetEntity
    support_status: SpecialCriterionSupportStatus
    unsupported_reason: Optional[str]
    mapped_data_points: list[SpecialCriterionMappedDataPoint]


class ExtractedCompanyProfile(BaseModel):
    company_type_description: str
    structured_keywords: List[TypedCompanyTag]


class IdealCustomerProfile(TelescopeBaseType):
    name: Optional[str] = None
    campaign_id: str
    example_companies: List[ExampleCompany]
    fictive_example_company_descriptions: Optional[List[str]] = []
    full_company_descriptive_info: Optional[str] = None
    summary_company_descriptive_info: Optional[str] = None
    full_contact_descriptive_info: Optional[str] = None
    summary_contact_descriptive_info: Optional[str] = None
    job_titles: List[str]
    keywords: Optional[List[str]] = None
    company_search_typed_keywords: Optional[List[TypedCompanyTag]] = None
    extracted_company_profiles: Optional[List[ExtractedCompanyProfile]] = None
    negative_keywords: Optional[List[str]] = None
    hq_location_filters: Optional[List[FilterableLocation]] = None
    hq_location_excludes: Optional[List[FilterableLocation]] = None
    employee_location_filters: Optional[List[FilterableLocation]] = None
    employee_location_excludes: Optional[List[FilterableLocation]] = None
    industries: Optional[List[str]] = None
    company_size_range: Optional[CompanySizeRange] = None
    company_types: Optional[List[str]] = None
    founded_year_range: Optional[FoundedYearRange] = None
    company_types_description: Optional[List[str]] = []
    special_criteria: Optional[List[SpecialCriterion]] = []
    require_email: Optional[bool] = False
    company_revenue_range: Optional[RevenueRange] = None
    only_show_verified_emails: Optional[bool] = False
    hide_companies_in_another_campaign: Optional[bool] = False
    hide_leads_in_another_campaign: Optional[bool] = False
    deleted_at: Optional[str] = None
