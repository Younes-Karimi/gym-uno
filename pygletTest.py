import pyglet

class example(pyglet.window.Window):
    def __init__(self):
        super(example, self).__init__(640, 480, resizable=False, fullscreen=False, caption="Test")
        self.clear()

        self.document = pyglet.text.document.FormattedDocument('This is a multi line document. This is a multi line document.')
        #self.document.set_style(0,len(self.document.text),dict(color=(255,0,0,255)))
        self.text = pyglet.text.layout.TextLayout(self.document,240,420,multiline=True)

        pyglet.clock.schedule_interval(self.update, .01)

    def update(self,dt):
        self.draw()

    def draw(self):
        self.clear()
        self.text.draw()

if __name__ == '__main__':
    window = example()
    pyglet.app.run()