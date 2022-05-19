import unittest
from unittest import mock
import pandas as pd
from pandas.util.testing import assert_frame_equal
from app_main import get_all_options, bar_chart_figure, color_range, color_range_BRE

class TestAppMain(unittest.TestCase):
    
    # BAR_CHART_FIGURE_TESTS

    @mock.patch('app_main.get_all_options', return_value = ['test1', 'test2'])
    def test_bar_chart_figure_wrong_names(self, options):
        with self.assertRaises(TypeError):
            bar_chart_figure()
    
    @mock.patch('app_main.get_all_options', return_value = ['test_1', 'test_2'])
    def test_bar_chart_figure_no_csv_files(self, options):
        with self.assertRaises(TypeError):
            bar_chart_figure()


    # COLOR_RANGE_TESTS

    # Test color_range, if input df is equal to expected output, usint assert_frame_equal
    def test_color_range_floats(self):
        df_input = pd.DataFrame({'Scenario2/Scenario1': [0.1, 0.3, 0.5, 0.8, 0.7, 0.9]})

        df_expected = pd.DataFrame({'Scenario2/Scenario1': [0.1, 0.3, 0.5, 0.8, 0.7, 0.9],
                                  'Color': ['rgb(220,20,60)', 'rgb(220,20,60)', 'rgb(220,20,60)', 
                                            'rgb(144,238,144)', 'rgb(240,128,128)', 'rgb(0, 128, 0)']})
        
        assert_frame_equal(color_range(df_input), df_expected)

    # Test color_range for string appears in float column
    def test_color_range_strings(self):
        df_input = pd.DataFrame({'Scenario2/Scenario1': ["test", 0.3, 0.5, 0.8, 0.7, 0.9]})

        with self.assertRaises(TypeError):
            assert_frame_equal(color_range(df_input))
        
    # COLOR_RANGE_BRE TESTS
    def test_color_range_floats(self):
        df_input = pd.DataFrame({'Scenario2/Scenario1': [0.1, 0.3, 0.5, 0.8, 0.85, 0.9]})

        df_expected = pd.DataFrame({'Scenario2/Scenario1': [0.1, 0.3, 0.5, 0.8, 0.85, 0.9],
                                    'Color': ['rgb(220,20,60)', 'rgb(220,20,60)', 'rgb(220,20,60)', 
                                             'rgb(0, 128, 0)', 'rgb(0, 128, 0)', 'rgb(0, 128, 0)']})
        
        assert_frame_equal(color_range_BRE(df_input), df_expected)




if __name__ == '__main__':
    unittest.main()
    