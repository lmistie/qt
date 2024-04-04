import sys
import os
from PyQt5 import uic, QtWidgets

def my_eval(expression): 
    operators = {'+': 1, '-': 1, '*': 2, '/': 2} 
    ops_stack = [] 
    nums_stack = [] 

    def apply_op(): 
        op = ops_stack.pop() 
        num2 = nums_stack.pop() 
        num1 = nums_stack.pop() 
        if op == '+':
            nums_stack.append(num1 + num2)
        elif op == '-':
            nums_stack.append(num1 - num2)
        elif op == '*':
            nums_stack.append(num1 * num2)
        elif op == '/':
            nums_stack.append(num1 / num2)
    
    i = 0
    while i < len(expression):
        if expression[i].isdigit():
            num = int(expression[i])
            i += 1
            while i < len(expression) and expression[i].isdigit():
                num = num * 10 + int(expression[i])
                i += 1
            nums_stack.append(num)
        elif expression[i] in operators:
            while ops_stack and ops_stack[-1] != '(' and operators[ops_stack[-1]] >= operators[expression[i]]: 
                apply_op()
            ops_stack.append(expression[i])
            i += 1
        elif expression[i] == '(':
            ops_stack.append(expression[i])
            i += 1
        elif expression[i] == ')':
            while ops_stack[-1] != '(':
                apply_op()
            ops_stack.pop()
            i += 1
        else:
            i += 1

    while ops_stack:
        apply_op() 
    return nums_stack[0]

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # ui_file_path = os.path.join(current_dir, 'main1.ui')
        # uic.loadUi(ui_file_path, self)
        # /Users/lmistie/Desktop/RTU_MIREA/Магистратура/1_Курс/2_Семестр/Инструментальное программное обеспечение разработки и проектирования информационных систем/PR_Qt/PR5/main.ui
        uic.loadUi('/Users/lmistie/Desktop/RTU_MIREA/Магистратура/1_Курс/2_Семестр/Инструментальное программное обеспечение разработки и проектирования информационных систем/PR_Qt/PR5/main.ui', self)
        self.calculate.clicked.connect(self.calc)
    
    def calc(self):
        expression = self.input.text()
        result = my_eval(expression)
        self.result.setText(str(result))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
