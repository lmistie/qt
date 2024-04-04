#include <iostream>

class TriangleChecker {
private:
    double side1, side2, side3;

public:
    // Конструктор класса, принимает три положительных числа
    TriangleChecker(double s1, double s2, double s3) {
        // Проверка на положительность входных значений
        if (s1 > 0 && s2 > 0 && s3 > 0) {
            side1 = s1;
            side2 = s2;
            side3 = s3;
        } else {
            std::cout << "С отрицательными числами ничего не выйдет!" << std::endl;
        }
    }

    // Метод для проверки возможности построения треугольника
    void is_triangle() {
        if (side1 + side2 > side3 && side1 + side3 > side2 && side2 + side3 > side1) {
            std::cout << "Ура, можно построить треугольник!" << std::endl;
        } else {
            std::cout << "Жаль, но из этого треугольник не сделать." << std::endl;
        }
    }
};

int main() {
    // Пример использования класса TriangleChecker
    TriangleChecker triangle1(3, 4, 5);  // Возможность построения треугольника
    triangle1.is_triangle();

    TriangleChecker triangle2(-1, 2, 3);  // Отрицательное число
    TriangleChecker triangle3(1, 2, 4);   // Невозможность построения треугольника
    triangle3.is_triangle();

    return 0;
}
