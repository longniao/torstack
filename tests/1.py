# -*- coding: utf-8 -*-

'''
torstack..1
1 definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''


class Base(object):

    def __init__(self):
        print('Base init')

    def play(self):
        print('Base is playing!')


class A(Base):

    def __init__(self):
        super(A, self).__init__()
        print('A init')

    def play1(self):  # 自动覆盖父类的此方法
        print('A is playing')


class B(Base):

    def __init__(self):
        super(B, self).__init__()
        print('B init')

    def play2(self):
        print('B is playing')

    @property
    def x(self):
        print('xxx')
        return 'xxx'


class C(A, B):  # 继承A,B
    pass


c = C()
c.play()
c.play1()
c.play2()
c.x