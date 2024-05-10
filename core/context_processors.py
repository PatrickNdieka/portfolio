from .models import ConfigurationSetting


def configurations(request):
    confs = ConfigurationSetting.objects.prefetch_related('children').all()
    social_links = confs.filter(
        key='social_links').first()
    user_details = confs.filter(
        key='user_details').first()

    if social_links:
        social_links = {
            link.key: {
                item.key: item.get_value for item in link.children.all()
            } for link in social_links.children.prefetch_related('children').all()
        }
    if user_details:
        user_details = {
            detail.key: {
                **dict(((item.key, item.get_value) for item in detail.children.all())),
                'detail_type': dict((('email', 'mailto:'), ('phone', 'tel:'))).get(detail.key, ''),
            } for detail in user_details.children.prefetch_related('children').all().order_by('key')
        }
    return {
        'social_links': social_links,
        'user_details': user_details,
    }
