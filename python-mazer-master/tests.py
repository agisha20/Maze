import unittest
import main
import cv2
from unittest.mock import patch

TEST_MAZE_HSTART = 'testmazes/maze_h_start.png'
TEST_MAZE_VSTART = 'testmazes/maze_v_start.png'
TEST_MAZE_COMPLEX = 'testmazes/bigbigmaze.png'
class TestMain (unittest.TestCase):

    @patch('cv2.waitKey', return_value=0)
    def test_mainreadsimage(self, waitKey):
        try:
            main.main(TEST_MAZE_HSTART)
        except ValueError:
            self.fail('main() could not read image')
        
        self.assertRaises(ValueError, main.main, '_filethatdoesnotexist.doggo')
        
    
    def test_getstartingpoint(self):
        maze1 = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        expected_position = (0, 3)
        actual_position = main.get_starting_position(maze1)

        self.assertEqual(actual_position, expected_position)

        maze1 = cv2.imread(TEST_MAZE_VSTART, cv2.IMREAD_GRAYSCALE)
        expected_position = (1, 0)
        actual_position = main.get_starting_position(maze1)

        self.assertEqual(actual_position, expected_position)


    def test_getstartingpoint_raiseserror(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        # remove the starting point from the maze
        maze.itemset((0, 3), main.BLACK)

        self.assertRaises(ValueError, main.get_starting_position, maze)


    def test_findsfinishposition(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        expected_output = True
        actual_output = main.isfinish(maze, (7, 5))

        self.assertEqual(actual_output, expected_output)

        expected_output = False
        actual_output = main.isfinish(maze, (7, 4))

        self.assertEqual(actual_output, expected_output)


    def test_getoptions_returnslist(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        position = (0, 3)
        output = main.get_options(maze, position)
        
        self.assertIs(list, type(output))


    def test_getoptions_findsoptions(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        expected_output = [(1, 3)]
        actual_output = main.get_options(maze, (0, 3))

        self.assertEqual(actual_output, expected_output)

        expected_output = [(2, 3), (1, 2), (1, 4)]
        actual_output = main.get_options(maze, (1, 3))

        self.assertEqual(actual_output, expected_output)


    def test_getoptions_noexceedborder(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        expected_output = []
        actual_output = main.get_options(maze, (7, 2))

        self.assertEqual(actual_output, expected_output)
        
        expected_output = [(6, 1)]
        actual_output = main.get_options(maze, (7, 1))

        self.assertEqual(actual_output, expected_output)


    def test_paintpath(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        path = [(0, 3), (1, 3)]
        output = main.paint_path(maze, path)

        self.assertEqual(output.item(0, 3, 2), main.PATH_REDVALUE)
        self.assertEqual(output.item(1, 3, 2), main.PATH_REDVALUE)
        self.assertEqual(output.item(0, 1, 2), main.BLACK)


    def test_traverse_returnslist(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        maze.itemset((5, 5), main.ALREADY_VISITED)
        expected_output = list
        actual_output = main.traverse(maze, (6, 5), [])

        self.assertEqual(type(actual_output), expected_output)


    def test_traverse_solvessimplemaze(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        start = (0, 3)
        finish = (7, 5)

        expected_path = [(1, 3), (4, 3), (5, 5), (7, 5), (6, 5), (4, 5), (4, 4), (3, 3), (2, 3), (0, 3)]
        actual_path = main.traverse(maze, start, [])

        self.assertEqual(actual_path, expected_path)
        self.assertIn(finish, actual_path)
        self.assertIn(start, actual_path)


    def test_traverse_solvecomplexmaze(self):
        maze = cv2.imread(TEST_MAZE_COMPLEX, cv2.IMREAD_GRAYSCALE)
        start = (33, 0)
        finish = (1, 34)
        expected_path = [(33, 1), (33, 25), (14, 33), (6, 33), (1, 34), (1, 33), (2, 33), (3, 33), (4, 33), (5, 33), (7, 33), (8, 33), (9, 33), (10, 33), (10, 32), (10, 31), (11, 31), (12, 31), (13, 31), (14, 31), (14, 32), (15, 33), (16, 33), (17, 33), (18, 33), (19, 33), (20, 33), (21, 33), (22, 33), (23, 33), (24, 33), (25, 33), (26, 33), (27, 33), (28, 33), (29, 33), (29, 32), (29, 31), (29, 30), (29, 29), (28, 29), (27, 29), (27, 28), (27, 27), (28, 27), (29, 27), (29, 26), (29, 25), (30, 25), (31, 25), (32, 25), (33, 24), (33, 23), (33, 22), (33, 21), (33, 20), (33, 19), (33, 18), (33, 17), (33, 16), (33, 15), (33, 14), (33, 13), (33, 12), (33, 11), (33, 10), (33, 9), (33, 8), (32, 8), (31, 8), (31, 7), (31, 6), (32, 6), (33, 6), (33, 5), (33, 4), (33, 3), (33, 2), (33, 0)]
        actual_path = main.traverse(maze, (33, 0), [])

        self.assertEqual(actual_path, expected_path)
        self.assertIn(finish, actual_path)
        self.assertIn(start, actual_path)


    def test_traverse_returnsnone(self):
        maze = cv2.imread(TEST_MAZE_HSTART, cv2.IMREAD_GRAYSCALE)
        maze.itemset((7, 5), main.BLACK)
        actual_output = main.traverse(maze, (0, 3), [])

        self.assertIsNone(actual_output)


if __name__ == '__main__':
    unittest.main()