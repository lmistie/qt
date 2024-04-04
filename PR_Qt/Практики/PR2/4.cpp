#include <iostream>

class KgToLb {
private:
    double kg;

public:
    // Конструктор класса
    KgToLb(double initial_kg) : kg(initial_kg) {}

    // Геттер для получения значения в килограммах
    double get_kg() const {
        return kg;
    }

    // Сеттер для установки нового значения в килограммах
    void set_kg(double new_kg) {
        kg = new_kg;
    }

    // Метод для перевода из килограммов в фунты
    double to_lb() const {
        return kg * 2.20462;
    }
};

int main() {
    // Пример использования класса
    KgToLb weight(10.0);

    // Вывод текущего значения в килограммах
    std::cout << "Текущий вес в килограммах: " << weight.get_kg() << " кг" << std::endl;

    // Установка нового значения в килограммах
    weight.set_kg(15.0);

    // Вывод нового значения в килограммах и соответствующего значения в фунтах
    std::cout << "Новый вес в килограммах: " << weight.get_kg() << " кг" << std::endl;
    std::cout << "Эквивалент веса в фунтах: " << weight.to_lb() << " фунтов" << std::endl;

    return 0;
}
