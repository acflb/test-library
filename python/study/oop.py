# 面向对象(OOP)的四个核心概念

# 1. 类与对象
# - 类是个"模版"或"蓝图"
# - 对象是按照这个模版创建出来的具体实例
# 类的定义
class Cat:
    def __init__(self, name, color):
        self.name = name  # 属性
        self.color = color

    def meow(self):  # 方法
        return f"{self.name}说：喵~"


# 对象的创建
# my_cat = Cat("小萌", "白色")
# print(my_cat.meow())


# 2.封装
# - 讲数据和错做这些数据的方法绑定在一起
# - 隐藏内部实现细节，只暴露必要的接口
# - 通过“访问控制”（public、private、protected）来限制谁能访问什么
class Cat_1:
    def __init__(self, name):
        self.__hunger = 0  # 私有属性，外部不能直接访问
        self.name = name  # 公开属性

    def eat(self, amount):  # 公开方法
        self.__hunger -= amount  # 内部才能改变饥饿值

    def get_hunger(self):  # 通过这个方法获取饥饿值
        return self.__hunger


my_cat = Cat_1("喵")
print(my_cat.get_hunger())
my_cat.eat(10)
print(my_cat.get_hunger())

# 3. 继承
# - 子类可以继承父类的属性和方法
# - 避免代码重复,形成一个"家族树"


class Animal:
    def breathe():
        return "呼吸..."


class Cat_2(Animal):
    def meow():
        return "喵~"


animal1 = Cat_2
print(animal1.breathe(), animal1.meow())


# 4. 多态
# - 同一个方法名,不同对象会有不同表现
class Dog:
    def sound():
        return "汪!"


class Bird:
    def sound():
        return "啾啾"


def make_sound(animal):
    print(animal.sound())


dog = Dog
bird = Bird
make_sound(dog)
make_sound(bird)


# 抽象(Abstraction)

# 只关注事物的关键特征，忽略无关细节
# 就像看到猫咪时，你注意的是"是只猫"这个本质，而不会关注喵咪每一根胡须的长度

# 接口(Interface) 和 抽象类(Abstract Class)

# 定义一个"合同"——规定必须提供什么方法，但不实现细节
# 多个类可以实现同一个接口

# 组合(Composition) vs 继承(Inheritance)

# 有时候用"包含"的方式比"继承"更灵活
# 比如：猫有尾巴(组合)，而不是猫继承尾巴
