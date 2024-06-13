from sqlalchemy.dialects import registry

try:
    registry.register("ocient.pyocient", "sqlalchemy_ocient.ocient", "OcientDialect")

    from sqlalchemy.testing.plugin.pytestplugin import *
except Exception:
    pass
