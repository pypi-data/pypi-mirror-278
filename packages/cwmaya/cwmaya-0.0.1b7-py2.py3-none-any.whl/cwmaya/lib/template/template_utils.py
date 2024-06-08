def setDialogTitle(dialog, node):
    name = node.name()
    title = f"Storm Tools | {name}"
    dialog.setTitle(title)
    dialog.setIconName(title)
