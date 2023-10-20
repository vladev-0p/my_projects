import operator

list_string = ['315 - 150', '30 + 300', '100 + 300','4000 + 5000']


# string ='30 + 3300'
# compile=eval(compile(string,'string','eval'))
# compile_str=str(compile)
# num_one=string.split(' ')[0]
# operator=string.split(' ')[1]
# num_two=string.split(' ')[2]
# top=''
# mid=''
# bot=''
# print(num_one)
# print(num_two)
# print(5-1%5)
# print(' ' *(5 - len(num_one)%5),num_one)
# print(operator+' ' *(4 - len(num_two)%5),num_two)
# print(' '*(5- len(compile_str)%5),compile)
# mid=''*len(operator)+''*(5-((max(len(num_one,num_two))%5)+num_two
# bot=''*(5-len(compile_str)+compile_str)
# print(top\n,mid\n,bot\n)

def calculate(list_string):
    top = ''
    mid = ''
    bot = ''
    border=''

    for i in list_string:
        compilex = eval(compile(i, 'string', 'eval'))
        compile_str = str(compilex)
        num_one = i.split(' ')[0]
        operator = i.split(' ')[1]
        num_two = i.split(' ')[2]
        if (len(num_two) or len(num_two))>5:
            raise Exception('Неверный ввод')
        else:
            add_top = (' ' * (5-len(num_one)) + num_one+' ')
            add_mid = (operator + ' ' * (4 -len(num_two)) + num_two+' ')
            add_border=(' '*(5-len(max(num_two,num_one))) + '_'*(max(len(num_two),len(num_one),len(compile_str))%5) +' ')
            add_bot = (' ' * (5 - max(len(num_one), len(num_two)) % 5) + str(compilex)+' ')
            top += add_top
            mid += add_mid
            border +=add_border
            bot += add_bot

    print(f'{top}\n{mid}\n{border}\n{bot}\n')

calculate(list_string)