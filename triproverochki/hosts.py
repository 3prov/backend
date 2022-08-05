from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'api', 'triproverochki.urls', name='triproverochki'),
    # host(f'form', '')
)
