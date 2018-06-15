# -*- coding: utf-8 -*-
from django.conf.urls import url
from temperature import views as views_cmp_host
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

# existing serializer, viewset, router registrations code
...

# Create our schema's view w/ the get_schema_view() helper method. Pass in
# the proper Renderers for swagger
schema_view = get_schema_view(
    title='Users API',
    renderer_classes=[
        OpenAPIRenderer,
        SwaggerUIRenderer])


urlpatterns = [
    url(r'doc$', schema_view, name="docs"),
    url(r'templist$', views_cmp_host.temperatureList.as_view()),
    url(r'templist/(?P<temperature_id>[^/]+)$', views_cmp_host.temperatureDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
