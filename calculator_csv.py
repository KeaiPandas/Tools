import csv
import sys
import json

def calculator(income):
    """计算税后收入的函数，参数用户原始收入"""
    social_insurance_point = 0.08+0.02+0.005+0.06
    # 纳税额为收入减5000
    shouldPay = income*(1 - social_insurance_point) - 5000

    # 用条件判断语句，根据扣税表写出不同薪资的扣税公式
    if shouldPay <= 0:
        tax = 0
    elif 0 < shouldPay <= 3000:
        tax = shouldPay * 0.03
    elif 3000 < shouldPay <= 12000:
        tax = shouldPay * 0.1 - 210 
    elif 12000 < shouldPay <= 25000:
        tax = shouldPay * 0.2 - 1410
    elif 25000 < shouldPay <= 35000:
        tax = shouldPay * 0.25 - 1410
    elif 35000 < shouldPay <= 55000:
        tax = shouldPay * 0.3 - 4410 
    elif 55000 < shouldPay <= 80000:
        tax = shouldPay * 0.35 - 7160 
    else:
        tax = shouldPay * 0.45 -15160 
    #计算总收入，并返回值
    salary = income * (1 - social_insurance_point) - tax
    return '{:.2f}'.format(salary)

def output(data):
    '''
    将字典存入文件
    '''
    #将字典存入json格式
    json_str = json.dumps(data)

    #打开sys.aregv[2]路径的文件,属性为'w'，写入json_str
    with open(sys.argv[2],'w') as f:
        f.write(json_str)

def main():
    '''
    main()函数
    '''
    #新建一个字典,存入形式ID：税后收入
    result = {}
    #通过sys.argv[1]拿到csv文件的路径
    data_file = sys.argv[1]
    #读取csv文件，计算税后收入，并存入字典
    usr_csv = csv.reader(open(data_file))
    data_list = list(usr_csv)

    print(data_list)
    for item in data_list:
        id, income = item[0],float(item[1])
        income = calculator(income)
        result[id] = income


    output(result)

if __name__ == '__main__':
    main()
