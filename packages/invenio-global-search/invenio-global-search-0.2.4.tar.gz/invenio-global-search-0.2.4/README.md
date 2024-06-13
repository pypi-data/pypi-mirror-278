# invenio-global-search

# configuration

add following code to the invenio.cfg file

from invenio_search_ui.views import blueprint
from invenio_rdm_records.services.components import DefaultRecordsComponents
from invenio_global_search.components import RDMToDublinCoreComponent
from flask import render_template

RDM_RECORDS_SERVICE_COMPONENTS = DefaultRecordsComponents + [RDMToDublinCoreComponent]
LOM_RECORDS_SERVICE_COMPONENTS = LOMDefaultRecordsComponents + [LOMToDublinCoreComponent]
MARC21_RECORDS_SERVICE_COMPONENTS = Marc21DefaultRecordsComponents + [Marc21ToDublinCoreComponent]

SEARCH_UI_SEARCH_TEMPLATE = "invenio_records_dublin_core/search/search.html"

@blueprint.route("/records/search")
def records_search():
    """Search page ui."""
    return render_template("invenio_app_rdm/records/search.html")

GLOBAL_SEARCH_ORIGINAL_SCHEMAS = {
    "lom": {
        "schema": "lom",
        "name_l10n": _("OER"),
    },
    "rdm": {
        "schema": "rdm",
        "name_l10n": _("Research Result"),
    },
    "marc21": {
        "schema": "marc21",
        "name_l10n": _("Publication"),
    },
}
