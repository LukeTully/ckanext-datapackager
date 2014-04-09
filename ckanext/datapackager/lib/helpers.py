'''Some custom template helper functions.

'''
import ckan.lib.helpers as helpers
import ckan.model as model
import ckan.plugins.toolkit as toolkit


def resource_display_name(*args, **kwargs):
    '''Return a display name for the given resource.

    This overrides CKAN's default resource_display_name template helper
    function and replaces 'Unnamed resource' with 'Unnamed file'.

    '''
    display_name = helpers.resource_display_name(*args, **kwargs)
    if display_name == 'Unnamed resource':
        display_name = 'Unnamed file'
    return display_name


def get_resource_schema(resource_id):
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
    }
    schema_show = toolkit.get_action('resource_schema_show')
    return schema_show(context, {'resource_id': resource_id})


def resource_schema_field_show(resource_id, index):
    '''A wrapper for the resource_schema_field_show action function.

    So templates can call the action function.

    '''
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
    }
    schema_field_show = toolkit.get_action('resource_schema_field_show')
    data_dict = {'resource_id': resource_id, 'index': index}
    return schema_field_show(context, data_dict)

def get_resource(resource_id):

    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
    }
    resource_show = toolkit.get_action('resource_show')
    return resource_show(context,{'id': resource_id})

def csv_data(resource):
    '''Return the CSV data for the given resource.

    '''
    import csv
    import itertools
    import ckan.lib.uploader as uploader

    preview_limit = 10
    upload = uploader.ResourceUpload(resource)

    try:
        with open(upload.get_path(resource['id'])) as csv_file:
            try:
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                csv_file.seek(0)
                csv_reader = csv.reader(csv_file, dialect)
                csv_values = itertools.islice(csv_reader, preview_limit)
                csv_values = zip(*csv_values)
            except csv.Error, e:
                raise
    except IOError as e:
        raise
    return csv_values