#include <iostream>

class Raboch {
private:
    std::string name;
    int vozrast;

public:
    Raboch(const std::string& n, int v) : name(n), vozrast(v) {
        count++; // Увеличиваем счетчик при создании объекта
    }

    void display_raboch() {
        std::cout << "Имя: " << name << ", Возраст: " << vozrast << std::endl;
    }

    static int count;

    static void display_count() {
        std::cout << "Количество рабочих: " << count << std::endl;
    }
};

int Raboch::count = 0;

class Deti {
private:
    std::string name;
    int vozrast;
    int schoolNum;

public:
    Deti(const std::string& n, int v) : name(n), vozrast(v) {
        if (vozrast <= 10) {
            schoolNum = 1;  // Младшая школа
        } else if (vozrast >= 11 && vozrast <= 14) {
            schoolNum = 2;  // Средняя школа
        } else {
            schoolNum = 3;  // Старшая школа
        }
    }

    void school() {
        std::cout << name << " учится в школе " << schoolNum << " с " << vozrast << " лет." << std::endl;
    }
};

int main() {
    Raboch raboch1("Иван", 35);
    Raboch raboch2("Мария", 28);

    std::cout << "Данные о рабочем 1:" << std::endl;
    raboch1.display_raboch();

    std::cout << "Данные о рабочем 2:" << std::endl;
    raboch2.display_raboch();

    Raboch::display_count();

    Deti deti1("Анна", 10);
    Deti deti2("Петя", 14);
    Deti deti3("Ольга", 15);

    deti1.school();
    deti2.school();
    deti3.school();

    return 0;
}
