class TheThing(object):
    def __init__(self):
        self.number = 0
    def some_func(self):
        print 'Some function called'
    def add_me_up(self,more):
        self.number += more
        return self.number
a = TheThing()
b = TheThing()
a.some_func()
b.some_func()
print a.add_me_up(10)
print a.add_me_up(20)
print b.add_me_up(13)
print b.add_me_up(98)

print 'Number in a ',a.number
print 'Number in b',b.number

class Test1(object): # always inherit from object in 2.x. it's called new-style classes. look it up
    def method1(self, a, b):
        return a + b

    @staticmethod
    def method2(a, b):
        return a + b

    @classmethod
    def method3(cls, a, b):
        return cls.method2(a, b)

t = Test1()  # same as doing it in another class

print Test1.method1(t, 1, 2) #form one of calling a method on an instance
print t.method1(1, 2)        # form two (the common one) essentially reduces to form one

print Test1.method2(1, 2)  #the static method can be called with just arguments
print t.method2(1, 2)      # on an instance or the class

print Test1.method3(1, 2)  # ditto for the class method. It will have access to the class
print t.method3(1, 2)      # that it's called on (the subclass if called on a subclass) 
                     # but will not have access to the instance it's called on 
                     # (if it is called on an instance)



a = [1,2,3,4,5,6]
st = 'Hello hi this'
lis = ['hi','hello','everybody']
print st[-2:]
print a[len(a)-2:]
s =''
print s[:2]=='*/'
print 'jklasdf'
print ','.join(lis)
st = st.lower()
print st.find('he')
print st.split()

def fn(*row):
    print ','.join(row)+'hello'

fn('qwe','wer','rtyu')
filename = '123 hello.txt'
if filename.find('.') != -1:
        print filename[:filename.find('.')]

filen = '001 hello'
lis = filen.split()
print lis[0]

path = 'D:\\TW\\Steps'
import os
for root,directory,filename in os.walk(path):
    print 'root',root
    print 'directory',directory
    print 'filename',filename
    for files in filename:
        print files