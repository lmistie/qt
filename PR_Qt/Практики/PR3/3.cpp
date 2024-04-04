#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

// Функция для поиска слов максимальной длины в строке
std::vector<std::string> find_longest_words(const std::string& line) {
    std::istringstream iss(line);
    std::string word;
    std::vector<std::string> longestWords;
    size_t maxLength = 0;

    while (iss >> word) {
        // Удаляем из слова знаки пунктуации
        word.erase(std::remove_if(word.begin(), word.end(), ispunct), word.end());

        // Проверяем длину слова
        if (word.length() > maxLength) {
            maxLength = word.length();
            longestWords.clear();
            longestWords.push_back(word);
        } else if (word.length() == maxLength) {
            longestWords.push_back(word);
        }
    }

    return longestWords;
}

// Функция для обработки файла и вывода слов максимальной длины
void process_file(const std::string& filename) {
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Не удалось открыть файл: " << filename << std::endl;
        return;
    }

    std::string line;
    while (std::getline(file, line)) {
        std::vector<std::string> longestWords = find_longest_words(line);

        // Выводим результат
        if (!longestWords.empty()) {
            std::cout << "Слова максимальной длины (" << longestWords[0].length() << " символов): ";
            for (const auto& word : longestWords) {
                std::cout << word << " ";
            }
            std::cout << std::endl;
        }
    }

    file.close();
}

int main() {
    // Путь к файлу с текстом
    std::string filepath = "text.txt";

    // Обработка файла
    process_file(filepath);

    return 0;
}
