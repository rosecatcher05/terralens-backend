from pydantic import BaseModel, EmailStr
from datetime import datetime

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    subject: str | None = None
    message: str


class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    department: str
    location: str
    employment_type: str
    description: str
    requirements: str


class JobResponse(JobCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class SiteSettingsBase(BaseModel):
    company_name: str | None = None
    tagline: str | None = None

    logo: str | None = None
    favicon: str | None = None

    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None

    address: str | None = None
    google_maps: str | None = None

    linkedin: str | None = None
    instagram: str | None = None
    facebook: str | None = None
    youtube: str | None = None
    twitter: str | None = None

    hero_title: str | None = None
    hero_subtitle: str | None = None

    hero_button_text: str | None = None
    hero_button_link: str | None = None

    # =====================================================
    # ABOUT
    # =====================================================

    about_label: str | None = None
    about_title: str | None = None
    about_description: str | None = None

    about_expertise_label: str | None = None
    about_expertise_title: str | None = None
    about_expertise_description: str | None = None

    about_projects_count: str | None = None
    about_projects_label: str | None = None

    about_clients_count: str | None = None
    about_clients_label: str | None = None

    footer_text: str | None = None

    seo_title: str | None = None
    seo_description: str | None = None
    seo_keywords: str | None = None

    hero_video: str | None = None
    statement_image: str | None = None

    about_video: str | None = None
    about_videos: list[str] | None = None
    
    services_video: str | None = None

    products_video: str | None = None

    showcase_video: str | None = None
    showcase_label: str | None = None
    showcase_title: str | None = None
    showcase_subtitle: str | None = None
    showcase_button_text: str | None = None

    careers_video: str | None = None
    contact_video: str | None = None

    contact_label: str | None = None
    contact_title: str | None = None
    contact_subtitle: str | None = None
    contact_button_text: str | None = None
    business_hours: str | None = None


class SiteSettingsUpdate(SiteSettingsBase):
    pass


class SiteSettingsResponse(SiteSettingsBase):
    id: int

    class Config:
        from_attributes = True

class ServiceCreate(BaseModel):
    name: str
    slug: str
    category: str
    description: str | None = None
    image: str | None = None
    is_active: bool = True


class ServiceResponse(ServiceCreate):
    id: int

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    category: str
    title: str
    subtitle: str | None = None

    client: str | None = None
    location: str | None = None
    year: str | None = None
    duration: str | None = None
    team: str | None = None

    description: str | None = None
    challenge: str | None = None
    solution: str | None = None

    results: str | None = None
    technologies: str | None = None

    image: str | None = None
    is_active: bool = True


class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    job_id: int
    full_name: str
    email: str
    phone: str | None = None
    resume: str | None = None
    cover_letter: str | None = None


class ApplicationResponse(ApplicationCreate):
    id: int
    job_title: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class PartnerCreate(BaseModel):
    name: str
    logo: str | None = None
    type: str
    is_active: bool = True


class PartnerResponse(PartnerCreate):
    id: int

    class Config:
        from_attributes = True

class BlogCreate(BaseModel):
    category: str
    date: str
    author: str
    read_time: str

    title: str
    excerpt: str | None = None
    content: str | None = None

    image: str | None = None
    is_active: bool = True


class BlogResponse(BlogCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class GalleryCreate(BaseModel):
    title: str
    category: str
    image: str
    is_active: bool = True


class GalleryResponse(GalleryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True