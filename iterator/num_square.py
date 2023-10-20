class MyIter:
    def __init__(self,number):
        self.count=0
        self.number=number

    def __iter__(self):
        return self

    def __next__(self):
        self.count+=1
        if self.count== self.number:
            raise StopIteration
        else:
            return self.count ** 2

user=int(input("Введите число "))
my_iter = MyIter(number=user)

for i_elem in my_iter:
    print(i_elem,end=' ')

print('\n')

def gen_func(number):
    for i_num in range(number):
        yield i_num**2

gen = gen_func(user)

for i_elem in gen:
    print(i_elem, end=' ')


gen = (i_elem**2 for i_elem in range(user))
print('\n')
for i in gen:
    print(i,end=' ')