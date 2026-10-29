import json

class Product:
    """Класс, представляющий товар."""
    def __init__(self, name, price, quantity):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_cost(self):
        """Возвращает общую стоимость товара (цена × количество)."""
        return self.price * self.quantity

    def to_dict(self):
        """Преобразует товар в словарь для сериализации."""
        return {"name": self.name, "price": self.price, "quantity": self.quantity}

    @classmethod
    def from_dict(cls, data):
        """Создаёт товар из словаря."""
        return cls(data["name"], data["price"], data["quantity"])

    def __str__(self):
        return f"{self.name} — {self.price} руб. × {self.quantity} шт. = {self.total_cost()} руб."


class ProductManager:
    """Класс для управления списком товаров."""
    def __init__(self):
        self.products = []

    def create(self, name, price, quantity):
        """Добавляет новый товар."""
        product = Product(name, price, quantity)
        self.products.append(product)
        return product

    def read_all(self):
        """Возвращает список всех товаров."""
        return self.products

    def read_by_index(self, index):
        """Возвращает товар по индексу."""
        if index < 0 or index >= len(self.products):
            raise IndexError("Неверный индекс товара")
        return self.products[index]

    def update(self, index, name=None, price=None, quantity=None):
        """Обновляет данные товара по индексу."""
        product = self.read_by_index(index)
        if name is not None:
            product.name = name
        if price is not None:
            if price < 0:
                raise ValueError("Цена не может быть отрицательной")
            product.price = price
        if quantity is not None:
            if quantity < 0:
                raise ValueError("Количество не может быть отрицательным")
            product.quantity = quantity
        return product

    def delete(self, index):
        """Удаляет товар по индексу."""
        if index < 0 or index >= len(self.products):
            raise IndexError("Неверный индекс товара")
        return self.products.pop(index)

    def save_to_file(self, filename):
        """Сохраняет все товары в JSON-файл."""
        with open(filename, "w", encoding="utf-8") as f:
            data = [p.to_dict() for p in self.products]
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename):
        """Загружает товары из JSON-файла."""
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.products = [Product.from_dict(item) for item in data]

    def report_total(self):
        """Отчёт: общая стоимость всех товаров и общее количество."""
        total_cost = sum(p.total_cost() for p in self.products)
        total_quantity = sum(p.quantity for p in self.products)
        return total_cost, total_quantity

    def report_most_expensive(self):
        """Отчёт: самый дорогой товар (по цене за единицу)."""
        if not self.products:
            return None
        return max(self.products, key=lambda p: p.price)

    def __str__(self):
        if not self.products:
            return "Список товаров пуст."
        return "\n".join(f"{i}. {p}" for i, p in enumerate(self.products))


def main():
    manager = ProductManager()

    while True:
        print("\n--- УЧЁТ ТОВАРОВ ---")
        print("1 - Добавить товар")
        print("2 - Показать все")
        print("3 - Обновить товар")
        print("4 - Удалить товар")
        print("5 - Сохранить в файл")
        print("6 - Загрузить из файла")
        print("7 - Отчёт: общая стоимость")
        print("8 - Отчёт: самый дорогой товар")
        print("0 - Выход")
        choice = input("Выбор: ")

        try:
            if choice == "1":
                name = input("Название: ")
                price = float(input("Цена: "))
                quantity = int(input("Количество: "))
                manager.create(name, price, quantity)
                print("Товар добавлен.")

            elif choice == "2":
                print(manager)

            elif choice == "3":
                idx = int(input("Номер товара: "))
                name = input("Новое название (Enter — пропустить): ") or None
                price_str = input("Новая цена (Enter — пропустить): ")
                price = float(price_str) if price_str else None
                qty_str = input("Новое количество (Enter — пропустить): ")
                quantity = int(qty_str) if qty_str else None
                manager.update(idx, name, price, quantity)
                print("Товар обновлён.")

            elif choice == "4":
                idx = int(input("Номер товара: "))
                manager.delete(idx)
                print("Товар удалён.")

            elif choice == "5":
                manager.save_to_file("products.json")
                print("Сохранено.")

            elif choice == "6":
                manager.load_from_file("products.json")
                print("Загружено.")

            elif choice == "7":
                cost, qty = manager.report_total()
                print(f"Общая стоимость: {cost} руб.")
                print(f"Общее количество: {qty} шт.")

            elif choice == "8":
                expensive = manager.report_most_expensive()
                if expensive:
                    print(f"Самый дорогой товар: {expensive.name} ({expensive.price} руб.)")
                else:
                    print("Список пуст.")

            elif choice == "0":
                break
        except (ValueError, IndexError) as e:
            print("Ошибка:", e)
        except FileNotFoundError:
            print("Ошибка: файл не найден.")
        except json.JSONDecodeError:
            print("Ошибка: повреждённый JSON-файл.")

if __name__ == "__main__":
    main()