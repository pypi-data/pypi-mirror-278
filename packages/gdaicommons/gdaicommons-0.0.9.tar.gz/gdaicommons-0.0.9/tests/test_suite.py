import unittest

from tests.fill_mask import FillMaskTest
from tests.text2text_generation import Text2TextGenerationTest
from tests.text_classification import TextClassificationTest
from tests.text_generation import TextGenerationTest
from tests.text_labelling import TextLabellingTest
from tests.text_summarization import TextSummarizationTest

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(FillMaskTest))
test_suite.addTest(unittest.makeSuite(Text2TextGenerationTest))
test_suite.addTest(unittest.makeSuite(TextClassificationTest))
test_suite.addTest(unittest.makeSuite(TextGenerationTest))
test_suite.addTest(unittest.makeSuite(TextLabellingTest))
test_suite.addTest(unittest.makeSuite(TextSummarizationTest))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite)
