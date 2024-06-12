# Add facilities to test chemistry endpoints. This will run its own webserver.
# These testing will require working with a server with chemistry license and is set up with chemistry correctly.
from io import StringIO, BytesIO

from sapiopylib.rest.ClientCallbackService import ClientCallback
from sapiopylib.rest.DataMgmtService import DataMgmtServer
from sapiopylib.rest.DataTypeService import DataTypeManager
from sapiopylib.rest.WebhookService import AbstractWebhookHandler, WebhookConfiguration, WebhookServerFactory
from sapiopylib.rest.pojo.datatype.FieldDefinition import VeloxDoubleFieldDefinition
from sapiopylib.rest.pojo.webhook.ClientCallbackRequest import *
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext
from sapiopylib.rest.pojo.webhook.WebhookResult import SapioWebhookResult
from sapiopylib.rest.utils.autopaging import QueryDataRecordByIdListAutoPager
from sapiopylib.rest.utils.recorddatasinks import InMemoryRecordDataSink

from data_type_models import *
from sapiopycommons.multimodal.multimodal import MultiModalManager
from sapiopycommons.multimodal.multimodal_data import *


def __select_type_and_item_to_load(client_callback: ClientCallback) -> tuple[ChemDataType, bool]:
    options = ["Compound Parts", "Compound Samples", "Chem Reagent Parts", "Chem Reagent Samples"]
    selected = client_callback.show_option_dialog(OptionDialogRequest(
        "Select Item Type", "Select one of the following item types that correspond to what you are registering",
        options))
    data_type: ChemDataType
    is_adding_items: bool
    if selected == 0:
        data_type = ChemDataType.CompoundPart
        is_adding_items = False
    elif selected == 1:
        data_type = ChemDataType.CompoundPart
        is_adding_items = True
    elif selected == 2:
        data_type = ChemDataType.ChemicalReagentPart
        is_adding_items = False
    elif selected == 3:
        data_type = ChemDataType.ChemicalReagentPart
        is_adding_items = True
    else:
        raise ValueError("Invalid selection index: " + str(selected))
    return data_type, is_adding_items


def download_chem_image(context: SapioWebhookContext) -> SapioWebhookResult:
    """
    Upload a chemical smiles user enters and download its SVG image.
    """
    user = context.user
    client_callback = DataMgmtServer.get_client_callback(user)
    smiles = client_callback.show_input_dialog(InputDialogCriteria("Enter a structure SMILES or RxN to load", ""))
    if not smiles:
        return SapioWebhookResult(False)
    reg_man = MultiModalManager(user)
    is_reaction_sel = client_callback.show_option_dialog(OptionDialogRequest("Is this a reaction?", "", ["Yes", "No"]))
    is_reaction = is_reaction_sel == 0
    image_list = reg_man.load_image_data(ImageDataRequestPojo([smiles], is_reaction))
    image_svg_text = image_list[0]
    with BytesIO(image_svg_text.encode('utf-8')) as io:
        client_callback.send_file("image.svg", False, io)
    return SapioWebhookResult(True)


def register_interactively(context: SapioWebhookContext) -> SapioWebhookResult:
    """
    Load an SDF file, provide error report back to the caller, and then let user pick the field mapping like loading from material management.
    """
    # TODO pending client_callback enablement on the webhook => webservice endpoint route.
    user = context.user
    client_callback = DataMgmtServer.get_client_callback(user)
    data_type, is_adding_items = __select_type_and_item_to_load(client_callback)

    data_sink = InMemoryRecordDataSink(user)
    data_sink.upload_single_file_to_webhook_server(FilePromptRequest("Upload SDF File Data", file_extension=".sdf"))

    reg_man = MultiModalManager(user)
    reg_result: ChemCompleteImportPojo = reg_man.register_interactively(
        ChemInteractiveRegisterRequestPojo(data_type, ChemFileType.SDF, is_adding_items, data_sink.data))
    if not reg_result:
        client_callback.display_warning("Registration incomplete.")
        return SapioWebhookResult(False)
    if reg_result.errors:
        for error in reg_result.errors:
            client_callback.display_warning(
                "Item with properties " + str(error.properties) + "cannot be registered: " + str(error.errorMsg))
    client_callback.display_info(
        "Successfully registered " + str(len(reg_result.newPartList)) + " new parts and used " + str(
            reg_result.numOldParts) + " old parts in this registration.")
    return SapioWebhookResult(True)


def register_non_interactively(context: SapioWebhookContext) -> SapioWebhookResult:
    """
    Without asking user for anything in between the registration,
    complete registration using non-interactive endpoints only.

    The only interactions are those provided within this webhook explicitly or custom rules/on-save actions.
    """
    user = context.user
    client_callback = DataMgmtServer.get_client_callback(user)
    data_type, is_adding_items = __select_type_and_item_to_load(client_callback)

    smiles = client_callback.show_input_dialog(InputDialogCriteria("Enter SMILES to register", ""))
    if not smiles:
        return SapioWebhookResult(False)
    reg_man = MultiModalManager(user)
    loaded_result: PyMoleculeLoaderResult = reg_man.load_compounds(CompoundLoadRequestPojo(
        data_type, ChemLoadType.SMILES_LIST, data_list=[smiles]))
    if loaded_result.errorList:
        client_callback.display_warning(
            "There is an error loading the structure. Registration was aborted.: " + str(loaded_result.errorList[0]))
    complete_result: ChemCompleteImportPojo = reg_man.register_compounds(
        ChemRegisterRequestPojo(data_type, loaded_result.compoundList))
    client_callback.display_info(
        "Registered " + str(len(complete_result.newPartList)) + " new parts and used " +
        str(complete_result.numOldParts) + " old parts in this registration.")
    return SapioWebhookResult(True)


def register_reaction(context: SapioWebhookContext) -> SapioWebhookResult:
    user = context.user
    client_callback = DataMgmtServer.get_client_callback(user)

    rxn = client_callback.show_input_dialog(InputDialogCriteria("Enter RxN to register", ""))
    if not rxn:
        return SapioWebhookResult(False)
    reg_man = MultiModalManager(user)
    loaded_result = reg_man.load_reactions(rxn)
    registered = reg_man.register_reactions(loaded_result.reactionRxn)
    client_callback.display_info("Successfully registered with Record: " + str(registered.fields))
    return SapioWebhookResult(True)


def structure_search(context: SapioWebhookContext) -> SapioWebhookResult:
    """
    Perform a substructure search or a similarity search.
    """
    user = context.user
    client_callback = DataMgmtServer.get_client_callback(user)
    option = client_callback.show_option_dialog(OptionDialogRequest(
        "Select Search Type", "",
        ["Compound Substructure", "Compound Similarity", "Reaction Substructure"]))
    search_type: ChemSearchType
    if option == 0:
        search_type = ChemSearchType.COMPOUND_SUBSTRUCTURE
    elif option == 1:
        search_type = ChemSearchType.COMPOUND_SIMILARITY
    else:
        search_type = ChemSearchType.REACTION_SUBSTRUCTURE
    query: str = client_callback.show_input_dialog(InputDialogCriteria(
        "Enter Search Text",
        "Enter the SMARTS for compound substructure search or SMILES for compound similarity search, "
        "or rSMARTS for reaction substructure search."))

    join_method: CartridgeMolJoinMethod | None = None
    if search_type is ChemSearchType.COMPOUND_SUBSTRUCTURE or search_type is ChemSearchType.COMPOUND_SIMILARITY:
        option = client_callback.show_option_dialog(OptionDialogRequest(
            "Select Join Type", "Select a Sapio registry type you are joining result with.",
            ["Compounds", "Chemical Reagants", "HELM Chemical Properties"]))
        if option == 0:
            join_method = CartridgeMolJoinMethod.COMPOUND_REGISTRY
        elif option == 1:
            join_method = CartridgeMolJoinMethod.REAGENT_REGISTRY
        else:
            join_method = CartridgeMolJoinMethod.HELM_STRUCTURE
    sim_search_upper: float | None = None
    if search_type is ChemSearchType.COMPOUND_SIMILARITY:
        field_def = VeloxDoubleFieldDefinition("Upper", "Upper", "Upper",
                                               0.0, 1.0, 0.95, 5)
        field_def.editable = True
        sim_search_upper = client_callback.show_input_dialog(InputDialogCriteria(
            "Enter Similarity Upper Bound", "", field_def))

    next_page_context: ChemQuickSearchContextData | None = None

    if not query:
        return SapioWebhookResult(False)
    reg_man = MultiModalManager(user)
    dt_man = DataTypeManager(user)
    temp_dt: TemporaryDataType
    if search_type is ChemSearchType.REACTION_SUBSTRUCTURE:
        temp_dt: TemporaryDataType = dt_man.get_temporary_data_type(ReactionModel.DATA_TYPE_NAME)
    elif join_method is CartridgeMolJoinMethod.COMPOUND_REGISTRY:
        temp_dt: TemporaryDataType = dt_man.get_temporary_data_type(CompoundPartModel.DATA_TYPE_NAME)
    elif join_method is CartridgeMolJoinMethod.REAGENT_REGISTRY:
        temp_dt: TemporaryDataType = dt_man.get_temporary_data_type(ChemicalReagentPartModel.DATA_TYPE_NAME)
    elif join_method is CartridgeMolJoinMethod.HELM_STRUCTURE:
        temp_dt: TemporaryDataType = dt_man.get_temporary_data_type(HelmChemPropertyModel.DATA_TYPE_NAME)
    else:
        raise ValueError("Unable to obtain temp type to display???")
    while True:
        search_result = reg_man.search_structures(
            ChemSearchRequestPojo(query, search_type, join_method, next_page_context, sim_search_upper))
        if not search_result.nextPageAvailable:
            client_callback.display_info("Hit End of Results. No further pages available.")
            return SapioWebhookResult(True)
        next_page_context = search_result.nextPageContext
        if search_result.recordIdListOfPage:
            records: list[DataRecord] = QueryDataRecordByIdListAutoPager(
                temp_dt.data_type_name, search_result.recordIdListOfPage, user).get_all_at_once()
            client_callback.show_table_entry_dialog(TableEntryDialogRequest(
                "Current Page Results", "", temp_dt, [x.fields for x in records]))
        else:
            client_callback.display_popup(DisplayPopupRequest(
                "No Results in Page", "This page may not contain any results. Good luck next time!",
                PopupType.Info))
        selected = client_callback.show_option_dialog(OptionDialogRequest("Continue?", "Continue to next page?", ["Yes", "No"]))
        if selected is None or selected != 0:
            return SapioWebhookResult(True)


class ChemistryRegistrationTestHandler(AbstractWebhookHandler):
    """
    This one will test the facilities to parse a chemical structure and return a svg file to user's browser.
    """

    def run(self, context: SapioWebhookContext) -> SapioWebhookResult:
        options = ['Download Image', 'Register Interactively', 'Register Non-Interactively', 'Structure Search',
                   'Register Reaction']
        user = context.user
        client_callback = DataMgmtServer.get_client_callback(user)
        selected = client_callback.show_option_dialog(OptionDialogRequest(
            "Select Test Option", "Select one of the test options below", options, closable=True))
        if selected is None:
            return SapioWebhookResult(False)
        if selected == 0:
            return download_chem_image(context)
        elif selected == 1:
            return register_interactively(context)
        elif selected == 2:
            return register_non_interactively(context)
        elif selected == 3:
            return structure_search(context)
        elif selected == 4:
            return register_reaction(context)
        return SapioWebhookResult(False)

config: WebhookConfiguration = WebhookConfiguration(verify_sapio_cert=False, debug=True)
config.register('/chem_test', ChemistryRegistrationTestHandler)

app = WebhookServerFactory.configure_flask_app(app=None, config=config)
app.run(host="0.0.0.0", port=8099)
