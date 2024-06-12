class ModelAdmin:
    # model
    model_readable_name = ''  # model readable name, if not, use model name
    # field
    model_fields = ()  # base fields for model
    list_display_restraint = ()  # show in list page, only restraint, not need interface
    list_editable_restraint = ()  # can edit in list page, only restraint, not need interface
    model_edit_fields = ()  # can edit in detail page
    model_create_fields = ()  # can create in create page
    model_translate_fields = ()  # translate model fields to human readable
