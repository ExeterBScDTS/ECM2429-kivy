# Kivy UI design

Use this example to experiment with Kivy widgets - buttons, sliders, etc.

## Kivy widgets

<https://kivy.org/doc/stable/api-kivy.uix.html>

### Layouts

<https://kivy.org/doc/stable/gettingstarted/layouts.html>

## The Kv language

<https://kivy.org/doc/stable/guide/lang.html>

## Text inputs

Kivy supports touch screens on tablets and phones, where on screen keyboards are used.
If you get an on screen keyboard on your laptop you might want to modify your Kivy configuration.

The default ```~/.kivy/config.ini``` file may have this line

```text
keyboard_mode = dock
```

Change the value to

```text
keyboard_mode = system
```

For more information see <https://kivy.org/doc/stable/guide/config.html#configure-kivy>
