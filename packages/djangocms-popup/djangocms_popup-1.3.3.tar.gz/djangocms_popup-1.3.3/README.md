<div align="center">
<img src="https://gitlab.com/kapt/open-source/djangocms-popup/uploads/e2df99dead12ac2c16e684d0f97d9ad3/image.png" alt="DjangoCMS-popup" /><br />
<i>This is a screenshot of an actual popup with the default css.</i>
</div>

## Install

1) Install module
   ```
   python3 -m pip install djangocms-popup
   ```

2) Add it to your INSTALLED_APPS
   ```
       "djangocms_popup",
   ```

3) Migrate
   ```
   python3 manage.py migrate djangocms_popup
   ```

4) Launch your django-cms site, it should be here!

![](https://gitlab.com/kapt/open-source/djangocms-popup/uploads/5bbbc877a1e68a440852f390c2259152/image.png)

### Requirements

* `django-cms`: Obviously,
* `django-sekizai`: Only for the template.

## Features

### A popup

![DjangoCMS-popup demo](https://gitlab.com/kapt/open-source/djangocms-popup/uploads/401e4f5d0182f2c5fd169e6cb2651a52/popup-demo.webm)

### An Admin list of popups that you can access from a button in your taskbar

![DjangoCMS-popup demo list](https://gitlab.com/kapt/open-source/djangocms-popup/uploads/7ae6ff72b81d6037023d88e7b6186f70/popup-list-demo.webm)

### More popups!

You can add more choices for the popup using a tuple in your settings, that let you choose which template file to use for each popup.

To do so, just add a var named `DJANGOCMS_POPUP_LIST` in your settings, like this:

```python
DJANGOCMS_POPUP_LIST = (
    ("bottom_right.html", "Bottom right popup"),
    ("bottom_left.html", "Bottom left popup"),
    ("top_right.html", "Top right popup"),
    ("top_left.html", "Top left popup"),
    ("center.html", "Center popup"),
)
```

Don't forget to add all the templates in the `templates/popup/` folder!

## Configuration

* `DJANGOCMS_POPUP_LIST` (default: `(("bottom_right.html", "Bottom right popup"),)`)
  Just a tuple. Let user choose other templates for the popups.

* `DJANGOCMS_POPUP_TOOLBAR_BUTTON` (boolean, default: `True`)
  Whether to add a button in the CMS toolbar to list all existing popups

* `DJANGOCMS_POPUP_TOOLBAR_MENU_IDENTIFIER` (string, default: `None`)
  The identifier of the menu in which the new button will be added.
  If it is None it will be added in the main toolbar.

  > :warning: Beware that the menu matching the provided menu identifier must exist prior to the creation of the Popup menu: the app defining this menu must appear before djangocms_popup in your INSTALLED_APPS.

* `DJANGOCMS_POPUP_TOOLBAR_MENU_POSITION` (integer, default: `None`)
  The position of the button in the toolbar or in the menu defined by `DJANGOCMS_POPUP_TOOLBAR_MENU_IDENTIFIER`

## Customize it!

The template included in this project serves demonstration purpose only, it's up to you to integrate it into your graphic charter by creating a file in `templates/popup/popup_plugin.html`.

## How it works

It's a classic djangocms-plugin, with all the stuff in `admin.py`, `cms_plugins.py`, `cms_toolbars.py` and `models.py`.

The "fun" part is in the template.

The child plugins will be rendered inside a div which have a `visibility` property (see [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/visibility)).

Then, a _very_ dumb script (in vanilla javascript) will display the div with a delay using `setTimeout`, and will add an event listener on a small button (that will show/hide the popup when clicked).

If the option "*Allow the popup to be reopened if it is closed*", the small button will still be visible, even if you refresh the page.

The state of the popup is stored inside the localStorage (the id is `popup_is_open_{{ instance.id }}`), so a closed popup won't reopen at a page reload.

*Warning!* The plugin uses the `visibility` property! So if any of the plugins you put inside the popup have a `visibilit: visible` property it will be shown!
