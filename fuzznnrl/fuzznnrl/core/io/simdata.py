# project: fuzznnrl
# Copyright (C) 6/12/18 - 2:52 PM
# Author: bbrighttaer


class Text(object):
    """Models a word or field in a line of text"""

    def __init__(self, data):
        self.__data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, v):
        self.__data = v

    def __str__(self):
        return str(self.__data)


class Line(object):
    """
    Models a line of text
    """

    def __init__(self, text_list=None, delimiter=' '):
        if text_list:
            self.__line = text_list
        else:
            self.__line = []
        self.__delimiter = delimiter

    @property
    def line(self):
        return self.__line

    @line.setter
    def line(self, l):
        """
        The list of texts of this line
        :param l:
        :return:
        """
        self.__line = l

    @property
    def delimiter(self):
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, delimiter):
        self.__delimiter = delimiter

    def add(self, text):
        """
        Add a text to the line
        :param text: The text to be added
        """
        if isinstance(text, Text):
            self.__line.append(text)
        else:
            self.__line.append(Text(text))
        return self

    def join(self, l):
        """
        Joins two lines
        :param l: The line to be added
        :return: The current state of the line
        """
        self.__line += l.line
        return self

    def __add__(self, other):
        """
        allows the operation line1 = line1 + line2
        :param other: the second line to be added to this line
        :return: the current state of the line
        """
        return self.join(other)

    def __neg__(self):
        """
        Serves as backspace
        :return: A tuple containing the removed text and the current state of the line
        """
        return self.__line.pop(), self

    def backspace(self):
        """
        Alternative method for calling __neg__
        """
        return -self

    def __iter__(self):
        """
        Iterates over the text in the line
        :return: A text object
        """
        for x in self.__line:
            yield x

    def __getitem__(self, index):
        return str(self.__line[index])

    def __setitem__(self, key, value):
        if isinstance(value, Text):
            self.__line[key] = value
        else:
            self.__line[key] = Text(value)

    def __str__(self):
        if len(self.__line) > 0:
            line = self[0]
            size = len(self.__line)
            for i in range(1, size):
                line += self.__delimiter + self[i]
            return line


class Document(object):
    """
    Models a document of lines that can be saved to disk
    """

    def __init__(self, name, path='', lines=None):
        self.__doc = []
        if lines:
            for line in lines:
                self.__doc.append(line)
        self.__name = name
        self.__path = path

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def doc(self):
        return self.__doc

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    def addline(self, line):
        self.__doc.append(line)
        return self

    def __str__(self):
        if len(self.__doc) > 0:
            doc = str(self.__doc[0])
            for i in range(1, len(self.__doc)):
                doc += '\n' + str(self.__doc[i])
            return doc

    def clear(self):
        """
        Clears the content of the document
        """
        self.__doc.clear()

    def save(self, append=True):
        """
        Saves the document to a specified location

        Parameters
        --------------
        :param append indicates the writing mode
        """
        full_name = None
        try:
            if len(self.__path) > 0:
                full_name = self.__path + '/' + self.__name
            else:
                full_name = self.__name

            if append:
                mode = 'a'
            else:
                mode = 'w'
            if len(self.__doc) > 0:
                with open(full_name, mode) as f:
                    f.write(str(self.__doc[0]) + '\n')
                    for i in range(1, len(self.__doc)):
                        f.write(str(self.__doc[i]) + '\n')
        except PermissionError:
            print("Permission denied for path {}".format(full_name))
