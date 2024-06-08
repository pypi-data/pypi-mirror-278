import pymel.core as pm
import json
import cwmaya.lib.const as k


def layout_form(form, text, main_layout, *buttons):
    form.attachForm(text, "left", k.FORM_SPACING_X)
    form.attachForm(text, "right", k.FORM_SPACING_X)
    form.attachForm(text, "top", k.FORM_SPACING_Y)
    form.attachNone(text, "bottom")

    form.attachForm(main_layout, "left", k.FORM_SPACING_X)
    form.attachForm(main_layout, "right", k.FORM_SPACING_X)
    form.attachControl(main_layout, "top", k.FORM_SPACING_Y, text)
    form.attachControl(main_layout, "bottom", k.FORM_SPACING_Y, buttons[0])

    form.attachForm(buttons[0], "left", k.FORM_SPACING_X)
    form.attachNone(buttons[0], "top")
    form.attachForm(buttons[0], "bottom", k.FORM_SPACING_Y)

    if len(buttons) == 1:
        form.attachForm(buttons[0], "right", k.FORM_SPACING_X)
    else:  # 2
        form.attachPosition(buttons[0], "right", k.FORM_SPACING_X, 50)

        form.attachPosition(buttons[1], "left", k.FORM_SPACING_X, 50)
        form.attachForm(buttons[1], "right", k.FORM_SPACING_X)
        form.attachNone(buttons[1], "top")
        form.attachForm(buttons[1], "bottom", k.FORM_SPACING_Y)


def show_as_json(data, **kw):
    title = kw.get("title", "Json Window")
    indent = kw.get("indent", 2)
    sort_keys = kw.get("sort_keys", True)
    result_json = json.dumps(data, indent=indent, sort_keys=sort_keys)
    pm.window(width=600, height=800, title=title)
    pm.frameLayout(cll=False, lv=False)
    pm.scrollField(text=result_json, editable=False, wordWrap=False)
    pm.showWindow()


def show_data_in_window(data, **kw):
    title = kw.get("title", "Window")
    result_json = json.dumps(data, indent=2)
    pm.window(width=600, height=800, title=title)
    pm.frameLayout(cll=False, lv=False)
    pm.scrollField(text=result_json, editable=False, wordWrap=False)
    pm.showWindow()

def show_text_in_window(text, **kw):
    title = kw.get("title", "Window")
    pm.window(width=600, height=800, title=title)
    pm.frameLayout(cll=False, lv=False)
    pm.scrollField(text=text, editable=False, wordWrap=False)
    pm.showWindow()
