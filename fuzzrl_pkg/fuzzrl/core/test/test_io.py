# project: fuzzrl
# Copyright (C) 6/12/18 - 3:16 PM
# Author: bbrighttaer

from fuzzrl.core.io.simdata import *
from fuzzrl.core.test import *


class TestIO(unittest.TestCase):
    def test_Line(self):
        line = Line() \
            .add(Text(1)) \
            .add(Text(2)) \
            .add(Text(3)) \
            .add(Text(4))

        for text in line:
            log.info(text)
        line2 = Line() \
            .add(5) \
            .add(6) \
            .add(7)
        log.info(line2)
        log.info(line + line2)
        a, b = -line2
        print(str(a), 'line =', str(b))

    def test_savedocument(self):
        line = Line() \
            .add(Text(1)) \
            .add(Text(2)) \
            .add(Text(3)) \
            .add(Text(4))
        line2 = Line(delimiter=',') \
            .add(5) \
            .add(6) \
            .add(7)
        document = Document("test_doc.txt", '', line, line2)
        print('\n', str(document))
        document.save(append=False)
