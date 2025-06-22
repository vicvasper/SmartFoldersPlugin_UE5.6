import unreal

def add_toolbar_button():
    unreal.log("Iniciando add_toolbar_button")

    # Verificar la ruta del widget
    widget_path = "/SmartFolders/Core/EUW_SmartFolders.EUW_SmartFolders"
    if not unreal.EditorAssetLibrary.does_asset_exist(widget_path):
        unreal.log_error(f"Widget no encontrado en: {widget_path}")
        return

    # Comando Python para abrir el widget
    python_command = (
        "import unreal\n"
        f"widget_path = '{widget_path}'\n"
        "widget_class = unreal.load_asset(widget_path)\n"
        "if widget_class:\n"
        "    subsystem = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)\n"
        "    if subsystem:\n"
        "        subsystem.spawn_and_register_tab(widget_class)\n"
        "        unreal.log('Widget abierto exitosamente')\n"
        "    else:\n"
        "        unreal.log_error('Subistema de utilidad no disponible')\n"
        "else:\n"
        "    unreal.log_error('No se pudo cargar el widget')\n"
    )

    # Crear la entrada del botón para el toolbar
    entry = unreal.ToolMenuEntry(
        name="AssetOrganizerButton_Auto",
        type=unreal.MultiBlockType.TOOL_BAR_BUTTON
    )
    entry.set_label("Organizador")
    entry.set_tool_tip("Abre la herramienta para organizar assets")

    # Usar ScriptSlateIcon con el icono predefinido
    try:
        icon = unreal.ScriptSlateIcon(
            style_set_name="DefaultRevisionControlStyle",
            style_name="RevisionControl.Branched",
            small_style_name="RevisionControl.Branched"

        )
        entry.set_icon(icon.style_set_name, icon.style_name, icon.small_style_name)
        unreal.log("Ícono configurado: ControlRigEditorStyle.ControlRig.FilterAnimLayerSelected")
    except Exception as e:
        unreal.log_error(f"Error al configurar ScriptSlateIcon: {str(e)}")
        # Fallback a un icono alternativo
        entry.set_icon("EditorStyle", "LevelEditor.OpenContentBrowser")
        unreal.log("Ícono configurado (fallback): EditorStyle.LevelEditor.OpenContentBrowser")

    # Configurar la acción asociada al botón para ejecutar el comando Python
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="SmartFoldersCommand",
        string=python_command
    )

    # Agregar el botón al menú del toolbar del LevelEditor
    tool_menus = unreal.ToolMenus.get()
    unreal.log("Buscando menú: LevelEditor.LevelEditorToolBar.User")
    toolbar = tool_menus.find_menu("LevelEditor.LevelEditorToolBar.User")
    if not toolbar:
        unreal.log_warning("Menú no encontrado, creando uno nuevo")
        toolbar = tool_menus.add_menu("LevelEditor.LevelEditorToolBar.User", "User ToolBar")
    if toolbar:
        try:
            toolbar.add_section("Common", "Common Section")
            unreal.log("Sección 'Common' creada o ya existente")
        except Exception as error:
            unreal.log_warning(f"Error al agregar sección 'Common': {str(error)}")

        toolbar.add_menu_entry("Common", entry)
        tool_menus.refresh_all_widgets()
        unreal.log("Botón agregado exitosamente")
    else:
        unreal.log_error("No se pudo crear el menú")

# Ejecutar la función
add_toolbar_button()