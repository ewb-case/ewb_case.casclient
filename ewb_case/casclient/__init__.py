from ewb_case.casclient import install


install.register_casclient_plugin()


def initialize(context):
    """
    """
    install.register_casclient_plugin_class(context)
