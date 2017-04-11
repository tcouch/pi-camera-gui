class Model:
     def update(self, input):
          self.do_something_with_input(input)

class Controller:
     def __init__(self):
         self.model = Model()
         self.view = View(self.model)

    def go(self):
        until end_condition():
            input = get_input()
            self.model.update(input)
            self.view.display()
            sleep(n)

class View:
       def __init__(self, model):
             self.model = model
       def display(self):
             display_something(self.model)
