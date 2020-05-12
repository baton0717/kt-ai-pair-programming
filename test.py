from flask import Flask, request, redirect
from random import *
import os

app = Flask(__name__)
app.env = 'development'
app.debug = True

@app.route('/')
def index():
    return "Welcom to Test"
# 사용자로부터 2 ~ 9 사이의 숫자를 입력 받은 후, 해당 숫자에 대한 구구단을 출력하세요.
# /gugu/<number>
@app.route('/gugu/<number>')
def gugu(number):
    trees = []
    if not number.isnumeric():
        return "숫자를 입력해 주세요."
    if int(number)<2 or int(number)>9:
        return "2~9사이의 값이 아닙니다. 다시 입력해 주세요."

    for i in range(9):
        trees.append(number+" * "+str(i+1)+" = "+str(int(number) * (i+1)))
    
    result =number+"단 입니다."+'<br>'+'<br>'.join(trees) 

    return result

# 사용자로부터 숫자를 N을 입력받은 후 1부터 N까지의 숫자 중 소수만 출력하세요.
# /prime?num=N
@app.route("/prime/<number>", methods=['get', 'post'])
def prime(number):
    num = int(number)
    num_list = []
    if num<=1:
        return "1보다 큰 값을 입력해 주세요."
    if num==2:
        return "2"

    for i in range(2, num+1):
        counter = 0
        for j in range(2, i):
            if i%j != 0:
                counter = counter+1
            if counter == i-2:
                num_list.append(i)
    num_list.sort()
    num_sort=[]
    for i in num_list:
        if(i not in num_sort):
            num_sort.append(i)
    
    result = number+" 이하의 소수 입니다."+'<br>'+str(num_sort)
    return result

# 사용자로부터 숫자를 N을 입력받아. N의 약수를 모두 출력하세요. 
# /common_factor?num=N
@app.route("/common_factor/<number>", methods=['get', 'post'])
def common_factor(number):
    num = int(number)
    num_list = []
    if num<1:
        return "1이상의 숫자를 넣어주세요"
    for i in range(1, num+1):
        if num%i == 0:
            num_list.append(i)
    
    result = number+" 의 약수 입니다."+'<br>'+str(num_list)
    return result


# 사용자로부터 숫자를 N, M을 입력받아 N과 M의 최대공약수와 최소공배수를 출력하세요. 
# /commons?num1=N&num2=M
@app.route("/commons/<number1>/<number2>", methods=['get', 'post'])
def commons(number1, number2):
    num1 = int(number1)
    num2 = int(number2)
    num_list = []
    s1 = 1
    if num1>num2:
        for i in range(1, num1):
            if num1%i == 0:
                if num2%i == 0:
                    s1=i
    else:
        for i in range(1, num2):
            if num2%i == 0:
                if num1%i == 0:
                    s1=i

    s2 = 1
    if num1>num2:
        for i in range(1,num2):
            if (num1*i)%num2==0:
                s2=num1*i
                break   
    else:
        for i in range(1,num1):
            if (num2*i)%num1==0:
                s2=num2*i
                break
    result = "{0}과 {1}의 최대공약수는 {2}이고, 최소공배수는 {3}입니다.".format(num1,num2,s1,s2)
    return result

# 사용자로부터 숫자를 N을 입력받아, 1, 5, 10, 25, 50의 숫자를 이용하여 최소 갯수로 N을 표현해보자 
# 예) 183 = 50 * 3 + 25 * 1 + 5 * 1 + 1 * 3 => 총 8개
# /coins?num=N

@app.route("/coins/<number>", methods=['get', 'post'])
def coins(number):
    num = int(number)
    c_50 = 0
    c_25 = 0
    c_10 = 0
    c_5 = 0
    c_1 = 0
    while num>0:
        if num >= 50:
            while num >= 50:
                num -= 50
                c_50 += 1
        elif num >= 25:
            while num >= 25:
                num -= 25
                c_25 += 1
        elif num >= 10:
            while num >= 10:
                num -= 10
                c_10 += 1
        elif num >= 5:
            while num >= 5:
                num -= 5
                c_5 += 1
        else:
            while num >= 1:
                num -= 1
                c_1 += 1
    sum = c_50+c_25+c_10+c_5+c_1
    result = "50 * {0} + 25 * {1} + 10 * {2} + 5 * {3} + 1 * {4} => 총 {5}개".format(c_50,c_25,c_10,c_5,c_1,sum)

    return result

# 주민등록번호를 입력받아 올바른 주민번호인지 검증하라.
# 주민번호 : ① ② ③ ④ ⑤ ⑥ - ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬
# 합계 
# = 마지막수를 제외한 12자리의 숫자에 2,3,4,5,6,7,8,9,2,3,4,5 를 순서대로 곱산수의 합
# = ①×2 + ②×3 + ③×4 + ④×5 + ⑤×6 + ⑥×7 + ⑦×8 + ⑧×9 + ⑨×2 + ⑩×3 + ⑪×4 + ⑫×5
# 나머지 = 합계를 11로 나눈 나머지
# 검증코드 = 11 - 나머지
# 여기서 검증코드가 ⑬자리에 들어 갑니다.
#
# /jumin 
# with form post
def get_template(filename):
    with open(f'./web/{filename}', 'r', encoding='utf8') as f:
        content=f.read()
    return content

@app.route('/jumin', methods=['get', 'post'])
def verify_jumin():
    # print(11-sum%11)      검증확인번호
    template = get_template('jumin.html')

    jumin = '000000-0000000'
    if request.method =='POST':
        jumin = request.form.get('jumin')
        li=[]
        for i in jumin:
            if i != '-':
                li.append((int(i)))
        sum = 0
        verify = [2,3,4,5,6,7,8,9,2,3,4,5]
        for i in verify:
            for j in li[:11]:
                sum += i*j

        if (11-sum%11) == li[-1]:
            return template.format("올바른 주민번호 입니다.")
        else:
            return template.format("잘못된 주민번호 입니다")

    return template.format("주민번호 검증 전입니다.")

# 원의 원주율을 구해보자
# /pi
@app.route("/pi", methods=['get', 'post'])
def pi():
    num = 10000000
    counter = 0
    for i in range(num):
        x = random()
        y = random()
        if (x**2+y**2) <= 1:
            counter += 1    

    pi = counter/num
    result = "원주율은 {0}입니다. (1000만번 계산한 경우)".format(pi*4)
    return result



app.run()