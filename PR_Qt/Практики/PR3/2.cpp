#include <iostream>
#include <dirent.h>
#include <sys/stat.h>

void print_directory_contents(const std::string& path) {
    DIR* dir = opendir(path.c_str());

    if (dir == nullptr) {
        std::cerr << "Не удалось открыть директорию: " << path << std::endl;
        return;
    }

    struct dirent* entry;
    while ((entry = readdir(dir)) != nullptr) {
        std::string full_path = path + "/" + entry->d_name;

        struct stat file_stat;
        if (stat(full_path.c_str(), &file_stat) == -1) {
            std::cerr << "Ошибка при получении информации о файле: " << full_path << std::endl;
            continue;
        }

        if (S_ISDIR(file_stat.st_mode)) {
            if (std::string(entry->d_name) != "." && std::string(entry->d_name) != "..") {
                std::cout << "Директория: " << entry->d_name << std::endl;
                print_directory_contents(full_path);
            }
        } else {
            std::cout << "Файл: " << entry->d_name << std::endl;
        }
    }

    closedir(dir);
}

int main() {
    // Путь к выбранной папке
    std::string folder_path = "/Users/lmistie/Desktop/Практики";

    // Выводим содержимое выбранной папки и всех вложенных папок
    print_directory_contents(folder_path);

    return 0;
}
