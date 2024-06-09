class SoupElement:
    """
    Базовий клас для всіх елементів парсера.

    :param parent: Батьківський елемент.
    :type parent: SoupElement, optional
    """

    def __init__(self):
        self.parent = None

    def find(self, name=None, attrs=None):
        """
        Знаходить перший дочірній елемент із заданими атрибутами.

        :param name: Ім'я тегу для пошуку.
        :type name: str, optional
        :param attrs: Атрибути для відповідності.
        :type attrs: dict, optional
        :return: Знайдений елемент або None, якщо не знайдено.
        :rtype: SoupElement or None
        :raises NotImplementedError: Якщо метод не реалізований.
        """
        if attrs is None:
            attrs = {}
        raise NotImplementedError

    def find_all(self, name=None, attrs=None):
        """
        Знаходить всі дочірні елементи із заданими атрибутами.

        :param name: Ім'я тегу для пошуку.
        :type name: str, optional
        :param attrs: Атрибути для відповідності.
        :type attrs: dict, optional
        :return: Список знайдених елементів.
        :rtype: list[SoupElement]
        :raises NotImplementedError: Якщо метод не реалізований.
        """
        if attrs is None:
            attrs = {}
        raise NotImplementedError

    def get_text(self):
        """
        Отримує текстовий вміст елемента.

        :return: Текстовий вміст.
        :rtype: str
        :raises NotImplementedError: Якщо метод не реалізований.
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Повертає строкове представлення елемента.

        :return: Строкове представлення.
        :rtype: str
        :raises NotImplementedError: Якщо метод не реалізований.
        """
        raise NotImplementedError


class NavigableString(SoupElement):
    """
    Клас для представлення рядків всередині HTML.

    :param data: Текстові дані.
    :type data: str
    """

    def __init__(self, data):
        super().__init__()
        self.data = data

    def get_text(self):
        return self.data

    def __repr__(self):
        return self.data


class SelectableTag(SoupElement):
    """
    Клас для представлення HTML тегів з підтримкою CSS селекторів.

    :param tag: Ім'я тегу.
    :type tag: str
    :param attrs: Атрибути тегу.
    :type attrs: dict
    """

    def __init__(self, tag, attrs):
        super().__init__()
        self.tag = tag
        self.attrs = attrs
        self.children = []
        self.text = ""

    def add_child(self, child):
        """
        Додає дочірній елемент до цього тегу.

        :param child: Дочірній елемент для додавання.
        :type child: SoupElement
        """
        child.parent = self
        self.children.append(child)
        if isinstance(child, NavigableString):
            self.text += child.data

    def get_text(self):
        """
        Повертає текст тільки від безпосередніх дітей, виключаючи вкладені елементи.

        :return: Текстовий вміст.
        :rtype: str
        """
        return ''.join(child.get_text() for child in self.children if isinstance(child, NavigableString))

    def get_text_ch(self):
        """
        Повертає текст від всіх дітей, включаючи вкладені елементи.

        :return: Текстовий вміст.
        :rtype: str
        """
        texts = []
        for child in self.children:
            texts.append(child.get_text())
        return ''.join(texts)

    def find(self, name=None, attrs=None):
        """
        Знаходить перший дочірній елемент із заданими атрибутами.

        :param name: Ім'я тегу для пошуку.
        :type name: str, optional
        :param attrs: Атрибути для відповідності.
        :type attrs: dict, optional
        :return: Знайдений елемент або None, якщо не знайдено.
        :rtype: SoupElement or None
        """
        if attrs is None:
            attrs = {}
        if self._matches(name, attrs):
            return self
        for child in self.children:
            if isinstance(child, SelectableTag):
                result = child.find(name, attrs)
                if result:
                    return result
        return None

    def find_all(self, name=None, attrs=None):
        """
        Знаходить всі дочірні елементи із заданими атрибутами.

        :param name: Ім'я тегу для пошуку.
        :type name: str, optional
        :param attrs: Атрибути для відповідності.
        :type attrs: dict, optional
        :return: Список знайдених елементів.
        :rtype: list[SoupElement]
        """
        if attrs is None:
            attrs = {}
        matches = []
        if self._matches(name, attrs):
            matches.append(self)
        for child in self.children:
            if isinstance(child, SelectableTag):
                matches.extend(child.find_all(name, attrs))
        return matches

    def find_all_by_attrs(self, attrs):
        """
        Знаходить елементи за кількома атрибутами.

        :param attrs: Атрибути у вигляді словника.
        :type attrs: dict
        :return: Список знайдених елементів.
        :rtype: list[SoupElement]
        """
        matches = self.find_all()
        for attr, value in attrs.items():
            matches = [element for element in matches if element.get(attr) == value]
        return matches

    def find_by_text(self, text):
        """
        Знаходить перший дочірній елемент, що містить заданий текст.

        :param text: Текст для пошуку.
        :type text: str
        :return: Знайдений елемент або None, якщо не знайдено.
        :rtype: SoupElement or None
        """
        if text in self.get_text():
            return self
        for child in self.children:
            if isinstance(child, SelectableTag):
                result = child.find_by_text(text)
                if result:
                    return result
        return None

    def find_all_by_text(self, text):
        """
        Знаходить всі дочірні елементи, що містять заданий текст.

        :param text: Текст для пошуку.
        :type text: str
        :return: Список знайдених елементів.
        :rtype: list[SoupElement]
        """
        matches = []
        if text in self.get_text():
            matches.append(self)
        for child in self.children:
            if isinstance(child, SelectableTag):
                matches.extend(child.find_all_by_text(text))
        return matches

    def get(self, attr, default=None):
        """
        Отримує значення заданого атрибута.

        :param attr: Ім'я атрибута.
        :type attr: str
        :param default: Значення за замовчуванням, якщо атрибут не знайдено.
        :type default: any, optional
        :return: Значення атрибута або значення за замовчуванням.
        :rtype: any
        """
        return self.attrs.get(attr, default)

    def _matches(self, name, attrs):
        """
        Перевіряє, чи відповідає тег заданим критеріям.

        :param name: Ім'я тегу для відповідності.
        :type name: str
        :param attrs: Атрибути для відповідності.
        :type attrs: dict
        :return: True, якщо тег відповідає, False в іншому випадку.
        :rtype: bool
        """
        if name and self.tag != name:
            return False
        for attr, value in attrs.items():
            if attr == 'class':
                class_values = self.attrs.get(attr, "").split()
                if isinstance(value, list):
                    if not all(v in class_values for v in value):
                        return False
                else:
                    if value not in class_values:
                        return False
            elif self.attrs.get(attr) != value:
                return False
        return True

    def select(self, selector):
        """
        Знаходить елементи, що відповідають CSS селектору.

        :param selector: CSS селектор.
        :type selector: str
        :return: Список знайдених елементів.
        :rtype: list
        """
        if selector.startswith('.'):
            return self.find_all_by_class(selector[1:])
        elif selector.startswith('#'):
            return self.find_all_by_id(selector[1:])
        else:
            return self.find_all(selector)

    def find_all_by_class(self, class_names):
        """
        Знаходить елементи за ім'ям класу.

        :param class_names: Список імен класів.
        :type class_names: list
        :return: Список знайдених елементів за іменами класів.
        :rtype: list
        :raises TypeError: Якщо `class_names` не є списком.
        """
        if not isinstance(class_names, list):
            raise TypeError("class_names повинен бути списком")

        matches = []
        for class_name in class_names:
            matches.extend(self.find_all(attrs={'class': class_name}))
        return matches

    def find_all_by_id(self, id_names):
        """
        Знаходить елементи за ID.

        :param id_names: Імена ID у вигляді списку.
        :type id_names: list
        :return: Список знайдених елементів.
        :rtype: list
        """
        matches = []
        for id_name in id_names:
            matches.extend(self.find_all(attrs={'id': id_name}))
        return matches

    def __repr__(self):
        """
        Повертає текстове представлення тега.

        :return: Текстове представлення.
        :rtype: str
        """
        attrs_repr = {k: v.split() if k == 'class' else v for k, v in self.attrs.items()}
        return f"<Tag(tag={self.tag}, attrs={attrs_repr}, children={len(self.children)}, text={self.text})>"
