import gi
gi.require_version("Gtk", "3.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, Pango, PangoCairo

from config import Config

class EditorView(Gtk.Misc):
    """A widget for drawing text.

    """

    def __init__(self, text="", config=None):
        self.text = text

        # Set defaults
        self.config = Config(config={
            "cursor": {
                "style": "block",
                "highlight_line": True,
                "position": 0
            },
            "font": {
                "family": "Monospace",
                "size": 14
            },
            "editor": {
                "word_wrap": True
            }
        })

        if (config):
            self.config.merge(config)

        __gtype_name__ = "EditorView"

        Gtk.Misc.__init__(self)
        self.set_size_request(10, 10)

    def set_text(self, text):
        self.text = text
        self.queue_draw()

    def do_draw(self, cr):
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
        fg_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        allocation = self.get_allocation()

        # Set up text for drawing
        layout = PangoCairo.create_layout(cr)

        # Draw background
        cr.set_source_rgba(*list(bg_color))
        cr.paint()

        # Draw the text
        cr.set_source_rgba(*list(fg_color))
        cr.move_to(0, 0)
        layout.set_text(self.text, -1)
        layout.set_font_description(Pango.font_description_from_string(self.config["font"]["family"] + " " +
                                    str(self.config["font"]["size"])))
        # Set the width for word wrap
        if self.config["editor"]["word_wrap"]:
            layout.set_width(Pango.SCALE * allocation.width)

        PangoCairo.show_layout(cr, layout)

        # Draw the cursor
        if self.config["cursor"]["position"] < layout.get_character_count():
            line, x = layout.index_to_line_x(self.config["cursor"]["position"], 0)
            x = x / Pango.SCALE

            if self.config["cursor"]["highlight_line"]:
                # Move to line
                cr.move_to(0, layout.get_pixel_size().height * (line / layout.get_line_count()))
                # Highlight line
                cr.set_source_rgba(0, 0, 0, 0.2)
                cr.rectangle(0,
                             layout.get_pixel_size().height * (line / layout.get_line_count()),
                             allocation.width,
                             layout.get_pixel_size().height * (line / layout.get_line_count()))
                cr.fill()

            # Move to the current cursor position
            cr.move_to(x, layout.get_pixel_size().height * (line / layout.get_line_count()))
            
            if self.config["cursor"]["style"] == "vertical_bar":
                cr.set_line_width(4)
                # Set color
                cr.set_source_rgba(1, 0, 0, 1)
                # Move to line
                cr.move_to(x+2, layout.get_pixel_size().height * (line / layout.get_line_count()))
                cr.line_to(x+2, layout.get_pixel_size().height * ((line+1) / layout.get_line_count())) # down to the next line
                cr.stroke()

            elif self.config["cursor"]["style"] == "block":
                cr.set_source_rgba(1, 0, 0, 0.5)
                _, x_end = layout.index_to_line_x(self.config["cursor"]["position"], -1)
                x_end = x_end / Pango.SCALE
                y = layout.get_pixel_size().height * (line / layout.get_line_count())
                y_end = layout.get_pixel_size().height * ((line+1) / layout.get_line_count())
                cr.rectangle(x, y, x_end - x, y_end - y)

                cr.fill()

