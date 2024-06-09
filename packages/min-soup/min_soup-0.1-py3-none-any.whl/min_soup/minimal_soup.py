import re
from .soup_element import NavigableString, SelectableTag

def _parse_attrs(attrs):
    """
    Розбирає атрибути тега.

    :param attrs: Рядок з атрибутами.
    :type attrs: str
    :return: Словник атрибутів.
    :rtype: dict
    """
    attr_re = re.compile(r'(\w+)="([^"]*)"')
    return {name: value for name, value in attr_re.findall(attrs)}


class MinimalSoup:
    """
    Головний клас для розбору HTML.

    :param html: HTML контент для розбору.
    :type html: str
    """

    TAG_RE = re.compile(r'<(/?)(\w+)([^>]*)>')

    def __init__(self, html):
        self.root = None
        self.current = None
        self.stack = []
        self._parse(html)

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

    def _parse(self, html):
        """
        Розбирає HTML контент.

        :param html: HTML контент.
        :type html: str
        """
        pos = 0
        while pos < len(html):
            match = self.TAG_RE.search(html, pos)
            if not match:
                self._handle_data(html[pos:])
                break

            start, end = match.span()
            self._handle_data(html[pos:start])
            self._handle_tag(match)
            pos = end

    def _handle_tag(self, match):
        """
        Обробляє розпізнаний тег.

        :param match: Об'єкт співпадіння.
        :type match: re.Match
        """
        slash, tag, attrs = match.groups()
        if slash:
            self._handle_endtag(tag)
        else:
            self._handle_starttag(tag, attrs)

    def _handle_starttag(self, tag, attrs):
        """
        Обробляє початковий тег.

        :param tag: Ім'я тега.
        :type tag: str
        :param attrs: Атрибути тега.
        :type attrs: str
        """
        attrs_dict = _parse_attrs(attrs)
        new_tag = SelectableTag(tag, attrs_dict)
        if self.current is not None:
            self.current.add_child(new_tag)
        else:
            self.root = new_tag
        self.stack.append(new_tag)
        self.current = new_tag

    def _handle_endtag(self, tag):
        """
        Обробляє кінцевий тег.

        :param tag: Ім'я тега.
        :type tag: str
        """
        if self.stack:
            self.stack.pop()
            self.current = self.stack[-1] if self.stack else None

    def _handle_data(self, data):
        """
        Обробляє текстові дані.

        :param data: Текстові дані.
        :type data: str
        """
        if data.strip():
            new_string = NavigableString(data.strip())
            if self.current is not None:
                self.current.add_child(new_string)

    def find(self, name=None, attrs=None):
        """
        Знаходить перший елемент з вказаними атрибутами.

        :param name: Ім'я тега для пошуку.
        :type name: str
        :param attrs: Атрибути для порівняння.
        :type attrs: dict
        :return: Знайдений елемент або None, якщо не знайдено.
        :rtype: SelectableTag або None
        """
        if attrs is None:
            attrs = {}
        if not self.root:
            return None
        return self.root.find(name, attrs)

    def find_all(self, name=None, attrs=None):
        """
        Знаходить всі елементи з вказаними атрибутами.

        :param name: Ім'я тега для пошуку.
        :type name: str
        :param attrs: Атрибути для порівняння.
        :type attrs: dict
        :return: Список знайдених елементів.
        :rtype: list
        """
        if attrs is None:
            attrs = {}
        if not self.root:
            return []
        return self.root.find_all(name, attrs)

    def find_all_by_attrs(self, attrs):
        """
        Знаходить елементи за кількома атрибутами.

        :param attrs: Атрибути у вигляді словника.
        :type attrs: dict
        :return: Список знайдених елементів.
        :rtype: list
        """
        if not self.root:
            return []
        return self.root.find_all_by_attrs(attrs)

    def find_by_text(self, text):
        """
        Знаходить перший елемент, що містить вказаний текст.

        :param text: Текст для пошуку.
        :type text: str
        :return: Знайдений елемент або None, якщо не знайдено.
        :rtype: SelectableTag або None
        """
        if not self.root:
            return None
        return self.root.find_by_text(text)

    def find_all_by_text(self, text):
        """
        Знаходить всі елементи, що містять вказаний текст.

        :param text: Текст для пошуку.
        :type text: str
        :return: Список знайдених елементів.
        :rtype: list
        """
        if not self.root:
            return []
        return self.root.find_all_by_text(text)

    def get_text(self):
        """
        Отримує текстовий вміст HTML.

        :return: Текстовий вміст.
        :rtype: str
        """
        return self.root.get_text() if self.root else ''

    def select(self, selector):
        """
        Знаходить елементи, що відповідають CSS селектору.

        :param selector: CSS селектор.
        :type selector: str
        :return: Список знайдених елементів.
        :rtype: list
        """
        if selector.startswith('.'):
            class_names = selector[1:].split('.')
            return self.find_all_by_class(class_names)
        elif selector.startswith('#'):
            return self.find_all_by_id(selector[1:])
        else:
            return self.find_all(selector)

    def select_one(self, selector):
        """
        Знаходить перший елемент, що відповідає CSS селектору.

        :param selector: CSS селектор.
        :type selector: str
        :return: Перший знайдений елемент або None, якщо не знайдено.
        :rtype: SelectableTag або None
        """
        elements = self.select(selector)
        return elements[0] if elements else None