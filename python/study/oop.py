# 面向对象
class Cat:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def meow(self):
        return f"{self.name}说：喵~"


my_cat = Cat("小萌", "白色")
print(my_cat.meow())
