from datetime import datetime

from django.contrib import admin
from django.utils.html import format_html

from config.config import JConfig
from .models import Thread, ThreadStatistic
from .models import ThreadMainExtendField
from .models import ThreadExtendData
from .models import ThreadExtendField
# from .models import ThreadImageAuth
from .models import ThreadShow, ThreadClassify, ThreadCategory
from .models import ThreadTag, ThreadTagMapping
from .utils.custom_paginator import CustomPaginator

config = JConfig()


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    paginator = CustomPaginator
    fieldsets = [
        ('主要信息', {'classes': 'collapse', 'fields': (
            'id', ('category', 'classify', 'show'), ('user_id', 'user_name_query', 'with_user_id'),
            ('group_id', 'thread_no'), ('title', 'subtitle'), 'summary', 'content', 'content_coding',
        )}),
        ('版权信息', {'classes': 'collapse', 'fields': (
            'access_level', 'author', ('region_code', 'ip'),
            ('has_enroll', 'has_fee', 'has_comment', 'has_location'),
        )}),
        ('媒体信息', {'classes': 'collapse', 'fields': (
            ('cover', 'photos'), ('video', 'files'), 'price', 'is_original', 'link',
        )}),
        ('更多设置', {'classes': 'collapse', 'fields': (
            ('logs', 'more'), ('sort', 'language_code'), ('is_subitem_thread', 'main_thread'), 'remark',
            ('create_time', 'update_time'), 'is_deleted',
        )}),
        ('扩展数据', {'classes': 'collapse', 'fields': (
            ('field_1', 'field_2', 'field_3'), ('field_4', 'field_5'), ('field_6', 'field_7'), ('field_8', 'field_9'),
            ('field_10', 'field_11'), ('field_12', 'field_13'), ('field_14', 'field_15'),
        )}),
    ]
    list_display = (
        'id', 'category', 'classify', 'show', 'user_id', 'user_name_query', 'with_user_id', 'group_id', 'thread_no',
        'title_short', 'subtitle_short', 'summary_short', 'content_short', 'access_level', 'author', 'region_code',
        'ip',
        'has_enroll', 'has_fee', 'has_comment', 'has_location',
        'cover_short', 'photos_short', 'video_short', 'files_short', 'price', 'is_original',
        'link', 'logs_short', 'more_short', 'sort', 'language_code',
        'is_subitem_thread', 'main_thread', 'remark', 'create_time', 'update_time', 'is_deleted',
        'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9', 'field_10',
        'field_11', 'field_12', 'field_13', 'field_14', 'field_15',
    )
    list_filter = ['category', 'classify', 'show', 'group_id', 'access_level', 'region_code']
    list_display_links = ['id', 'title_short']
    # 赵杨合并来的未优化代码 20230925
    # search_fields = ( 'title', 'subtitle', 'summary', 'content', 'region_code', 'publish_time', )
    search_fields = ('thread_no', 'title', 'subtitle', 'summary', 'region_code')
    raw_id_fields = ['category', 'classify', 'show', 'main_thread']
    readonly_fields = ('id', 'update_time', 'user_name_query')  # 只读
    # ordering = ['-update_time']  # 排序 # 使用 ModelAdmin.ordering 排序可能会导致性能问题，因为在一个大的查询集上排序会很慢。
    list_per_page = 20  # 每页显示10条

    def get_queryset(self, request):
        # print('get_queryset request:', request)
        qs = super().get_queryset(request)
        # print('get_queryset qs:', qs)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def get_list_display_links(self, request, list_display):
        # print('get_list_display_links request:', request, list_display)
        return self.list_display_links

    # # 优化页面的访问速度
    # def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
    #     print('get_paginator request:', datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), request, queryset, per_page, )
    #     rtn = self.paginator(queryset, per_page, orphans, allow_empty_first_page)
    #     print('get_paginator rtn:', datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), rtn, rtn.count)
    #     return rtn

    # class Media:
    #     css = {
    #         'all': (
    #             '/css/fancy.css',
    #         )
    #     }


@admin.register(ThreadMainExtendField)
class ThreadMainExtendFieldAdmin(admin.ModelAdmin):
    fields = ('id', 'category', 'field_index', 'field', 'value', 'default', 'type', 'unit', 'config', 'description',)
    list_display = (
        'id', 'category', 'field_index', 'field', 'value', 'default', 'type', 'unit', 'config_short', 'description',)
    search_fields = ('category__value', 'field_index', 'type')
    raw_id_fields = ['category']
    readonly_fields = ('id',)
    ordering = ['-category_id']
    list_per_page = 20  # 每页显示20条


@admin.register(ThreadCategory)
class ThreadCategoryAdmin(admin.ModelAdmin):
    fields = (
        'id', 'platform_code', 'value', 'name', 'need_auth', 'config', 'parent', 'description',
        'sort', 'is_deleted',)
    list_display = (
        'id', 'platform_code', 'value', 'name', 'need_auth', 'config', 'parent', 'short_description',
        'sort', 'is_deleted',)
    search_fields = ('id', 'platform_code', 'value', 'name',)
    readonly_fields = ('id',)
    ordering = ['platform_code', 'parent', 'sort']


@admin.register(ThreadClassify)
class ThreadClassifyAdmin(admin.ModelAdmin):
    fields = ('id', ('value', 'name'), ('category', 'show'), ('icon', 'config'), 'parent', 'description', 'sort',)
    list_display = ('id', 'value', 'name', 'category', 'show', 'icon', 'config', 'parent', 'description', 'sort',)
    list_display_links = ('id', 'value', 'name')
    search_fields = ('id', 'value', 'name', 'category', 'show')
    raw_id_fields = ['category', 'show', 'parent']
    readonly_fields = ['id']
    ordering = ['category', 'parent', 'sort']


@admin.register(ThreadShow)
class ThreadShowAdmin(admin.ModelAdmin):
    fields = ('id', 'value', 'name', 'config', 'description')
    list_display = ('id', 'value', 'name', 'config', 'description')
    search_fields = ('id', 'value', 'name', 'config')
    readonly_fields = ('id',)


@admin.register(ThreadExtendField)
class ThreadExtendFieldAdmin(admin.ModelAdmin):
    fields = ('id', 'category', 'field_index', 'field', 'value', 'default', 'type', 'unit', 'config', 'description',)
    list_display = ('id', 'category', 'field_index', 'field', 'value', 'default', 'type', 'unit', 'description',)
    search_fields = ('category__value', 'field_index', 'type')
    raw_id_fields = ['category']
    readonly_fields = ('id',)
    ordering = ['-category_id']
    list_per_page = 20  # 每页显示20条


@admin.register(ThreadExtendData)
class ThreadExtendDataAdmin(admin.ModelAdmin):
    fields = (
        'thread_id',
        ('field_1', 'field_2'), ('field_3', 'field_4'), ('field_5', 'field_6'), ('field_7', 'field_8'),
        ('field_9', 'field_10'), ('field_11', 'field_12'), ('field_13', 'field_14'),
        ('field_15'), ('field_16', 'field_17'), ('field_18', 'field_19'), 'field_20',)
    list_display = (
        'thread_id', 'short_field_1', 'short_field_2', 'short_field_3', 'short_field_4', 'short_field_5',
        'short_field_6', 'short_field_7', 'short_field_8', 'short_field_9', 'short_field_10', 'short_field_11',
        'short_field_12', 'short_field_13', 'short_field_14', 'short_field_15', 'short_field_16', 'short_field_17',
        'short_field_18', 'short_field_19', 'short_field_20',)
    search_fields = (
        'thread_id', 'short_field_1', 'short_field_2', 'short_field_3', 'short_field_4', 'short_field_5',
        'short_field_6', 'short_field_7', 'short_field_8', 'short_field_9', 'short_field_10', 'short_field_11',
        'short_field_12', 'short_field_13', 'short_field_14', 'short_field_15', 'short_field_16', 'short_field_17',
        'short_field_18', 'short_field_19', 'short_field_20',)
    raw_id_fields = ['thread_id']


@admin.register(ThreadTag)
class ThreadTagAdmin(admin.ModelAdmin):
    fields = ('id', 'value', 'user_id')
    search_fields = ('id', 'value', 'user_id')
    list_display = ('id', 'value')
    readonly_fields = ('id', 'thread')


@admin.register(ThreadTagMapping)
class ThreadTagMappingAdmin(admin.ModelAdmin):
    fields = ('thread', 'tag', 'statistic')
    list_display = ('id', 'thread', 'tag', 'statistic')
    search_fields = ('id', 'thread', 'tag')
    raw_id_fields = ['thread', 'tag', 'statistic']


# @admin.register(ThreadImageAuth)
# class ThreadImageAuthAdmin(admin.ModelAdmin):
#     list_display = ('id', 'value')
#     search_fields = ('id', 'value')
#     fields = (
#         'id',
#         'value',
#     )
#     readonly_fields = ('id',)


@admin.register(ThreadStatistic)
class ThreadStatisticAdmin(admin.ModelAdmin):
    fields = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', ('views', 'plays', 'comments'),
        ('likes', 'favorite', 'shares'),)
    list_display = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', 'views', 'plays', 'comments', 'likes', 'favorite',
        'shares',)
    search_fields = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', 'views', 'plays', 'comments', 'likes', 'favorite',
        'shares',)
    raw_id_fields = ['thread_id']


admin.site.site_header = config.get('main', 'app_name', 'msa一体化管理后台')
admin.site.site_title = config.get('main', 'app_name', 'msa一体化管理后台')

# @admin.register(ThreadResource)
# class ThreadImageAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     search_fields = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     fields = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     readonly_fields = ('id',)


# @admin.register(ThreadAuth)
# class ThreadAuthAdmin(admin.ModelAdmin):
#     list_display = ('id', 'value')
#     search_fields = ('id', 'value')
#     fields = ('id', 'value',)
#     readonly_fields = ('id',)
