# Your name: Isabella Valice
# Your student id: 83
# Your email: ivalice@umich.edu
# List who you have worked with on this homework: Addison Bassock, Margeaux Fortin, Orli Forster

import unittest
import os


class FileReader:
    """
    Represents a generic file reader. Used to read in data from a file of the
    user’s choice, analyze, and manipulate its data as Python objects.
    """
    def __init__(self, filename):
        """
        The constructor. Creates a new FileReader object based on the
        specified filename. For our purposes, the file should be in the same
        folder as HW5.py. To open a file called “mydiary.txt”, you would call
        FileReader(‘mydiary.txt’)
        """

        # this gives you the full path to the folder that this HW5.py is in
        # using the os library allows the code to run on Mac or Windows
        self.root_path = os.path.dirname(os.path.abspath(__file__))

        # all we have to do now is add the name of the file we want to open
        # to the full path
        self.filename = os.path.join(self.root_path, filename)

    def open_file(self):
        """
        Opens the file in read only mode, stores the resulting object as an
        instance variable called file_obj.
        """

        self.file_obj = open(self.filename, 'r', errors='replace')

    def read_lines(self):
        """
        Reads the lines from the file object into a list where each row of the
        CSV is a seperate element and stores it as an instance variable called
        file_data. Then closes the file object.
        """

        self.file_data = self.file_obj.readlines()
        self.file_obj.close()

    def strip_trailing_newlines(self):
        """
        Removes unnecessary newline characters (\n) from the end of
        each string in file_data.
        """

        for i in range(len(self.file_data)):
            self.file_data[i] = self.file_data[i].replace('\n', '')


class CsvReader(FileReader):
    """
    A child class of FileReader for reading CSV files only.
    """

    def __init__(self, csvfile):
        """
        The constructor. Overwrites the FileReader constructor such that in
        order to read a file called “mycsv.csv”, one only needs to call
        CsvReader(‘mycsv’). (Since CsvReader is designed to work only with
        .csv files, we don’t need to specify an extension.)
        """
        super().__init__(csvfile + ".csv")

    def build_data_dict(self):
        """
        Accesses the data stored in the file_data instance variable (a list)
        and converts it to a dictionary, data_dict, where each key is a column
        name found in the CSV, and each value is a list of data in that column
        with the same order as it was in the file.  Each element of the list
        corresponds to a single row in the CSV. For example, to access the
        “Name” column in the CSV, I would access data_dict['Name'].
        """

        self.data_dict = {
            'Name': [],
            'Rating': [],
            'URL': [],
            'Release Date': [],
            'Genre': [],
        }

        for i in (self.file_data[1:]):
            row = i.split(',')
            self.data_dict['Name'].append(row[0])
            self.data_dict['Rating'].append(row[1])
            self.data_dict['URL'].append(row[2])
            self.data_dict['Release Date'].append(row[3])
            self.data_dict['Genre'].append(row[4])

    def get_name_rating(self):
        """
        From the data stored in the data_dict instance variable, returns a
        list of tuples containing the name of the movie and its rating in the
        format (Name, Rating). The list should be sorted based on descending order of ratings.

        For example, [('Inception', 8.8), ('Interstellar', 8.6), ('Parasite', 8.6)]
        """

        tuples_list = []
        for i in range(len(self.data_dict['Name'])):
            tuples_list.append(
                (self.data_dict['Name'][i], float(self.data_dict['Rating'][i]))
                )

        sorted_tuples = sorted(tuples_list, key=lambda x: x[1], reverse = True)

        return sorted_tuples

    def get_genre_counts(self):
        """
        From the data stored in the data_dict instance variable, returns a
        list of tuples in the format ('Comedy', 10) where the
        first element is the genre, and the second element is the number of
        movies with that genre. The list should be sorted in descending order
        by the number of movies.

        For example, [(‘Comedy’, 20), (‘Drama’, 15), (‘Action’, 12),
                      (‘Romance’, 8)]
        """

        genre_counts = {}
        listofgenres = []
        for genre in self.data_dict['Genre']:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

        return sorted(genre_counts.items(), key = lambda x: x[1], reverse = True)


    def most_common_month(self):
        """
        Iterates through the "Release Date" column and counts the number of movies
        that were released in the same month (regardless of year) . Finally,
        returns the month with the maximum number of movie releases.

        For example, if the most movie releases were in July,
        this method would return 7.

        (We are using the American date format of month/date/year.)
        """

        month_counts = {}
        for i in self.data_dict['Release Date']:
            month = i.split('/')[0]
            month_counts[month] = month_counts.get(month, 0) + 1

        top_months = sorted(month_counts.items(), key = lambda x: x[1], reverse = True)

        return int(top_months[0][0])

    def get_movie_ID(self):
        """
        Returns a list of IDs for each row in the 'URL' column of
        the CSV by extracting the ID from the end of the URL.
        (i.e. the ID that would be extracted from the URL
        "https://www.imdb.com/title/tt1825683" would be "tt1825683")

        For example, given:
        [‘https://www.imdb.com/title/tt1825683’, ‘https://www.imdb.com/title/tt8946378’,
         ‘https://www.imdb.com/title/tt1375666’],
        this method would return ['tt1825683', 'tt8946378', 'tt1375666'].
        """

        ids = []
        for i in self.data_dict['URL']:
            ids.append(i.split('title/')[1])
        return ids

    # If you are attempting the extra credit, you can define
    # find_common_release_dates below
    def find_common_release_dates(self):
        """
        Returns a list of tuples, with each tuple consisting of two elements. 
        The first element should be a common release date, i.e. a release date (including 
        both day and month, regardless of year) shared by more than 1 movie. The second 
        element should indicate the number of movies that share that release date. Finally, 
        this list should be sorted in decreasing order of the number of movies.

        For example, this method should return a list like: 
        [('10/5', 5), ('11/4', 3), ('5/23', 2)]
        """


##############################################################################
# DO NOT MODIFY ANY CODE BELOW THIS - These are the test cases you must pass
##############################################################################

class TestHomework5(unittest.TestCase):
    def setUp(self):
        try:
            self.reader = CsvReader('H5Data')
            self.reader.open_file()
        except FileNotFoundError:
            self.reader = CsvReader('H5Data.csv')
            self.reader.open_file()
        self.reader.read_lines()
        self.reader.strip_trailing_newlines()
        self.reader.build_data_dict()

    def test_constructor(self):
        reader2 = CsvReader('testing123')
        self.assertTrue(reader2.filename.endswith('testing123.csv'))

    def test_read_lines(self):
        self.assertTrue(self.reader.file_obj.closed)

    def test_newline_strip(self):
        self.assertEqual(
            self.reader.file_data[0],
            'Name,Rating,URL,Release Date,Genre'
            )

    def test_first_row(self):
        self.assertEqual(self.reader.data_dict['Name'][0], 'Black Panther')
        self.assertEqual(self.reader.data_dict['Rating'][0], '7.3')
        self.assertEqual(
            self.reader.data_dict['URL'][0],
            'https://www.imdb.com/title/tt1825683'
            )
        self.assertEqual(self.reader.data_dict['Release Date'][0], '2/16/18')
        self.assertEqual(self.reader.data_dict['Genre'][0], 'Action')

    def test_get_name_rating(self):
        target = [
            ('Inception', 8.8),
            ('Interstellar', 8.6),
            ('Parasite', 8.6)
            ]
        self.assertEqual(self.reader.get_name_rating()[:3], target)

    def test_get_genre_counts(self):
        expected = [
            ('Action', 5),
            ('Drama', 5),
            ('Comedy', 4),
            ('Adventure', 1),
            ('Horror', 1)
            ]
        self.assertEqual(self.reader.get_genre_counts(), expected)

    def test_most_common_month(self):
        self.assertEqual(type(self.reader.most_common_month()), int)
        self.assertEqual(self.reader.most_common_month(), 11)

    ###########################################################################
    # You may modify the test case below.
    # You are required to write 2 assert statements in a loop here.
    # This is not extra credit.
    ###########################################################################

    def test_get_movie_ID(self):
        """
        Write the test case for test_get_movie_ID. You should loop over the data 
        returned by CsvReader.test_get_movie_ID() and write two assert statements 
        within that loop. The first assert statement should test if each ID starts 
        with ‘tt’. The second should check whether the length of each ID is 9.  

        We will check that your output for CsvReader.get_movie_ID() passes a hidden 
        test case that meets the above two requirements. You will receive points for 
        passing our version of this test case, and correctly implementing (and passing)
        your own version of this test case.

        """

        ids = self.reader.get_movie_ID()
        for i in range(len(ids)):
            self.assertEqual(self.reader.get_movie_ID()[i][:2], "tt")
            self.assertEqual(len(self.reader.get_movie_ID()[i]), 9)
        pass

    ###########################################################################
    # If you are doing the extra credit, write your new test case below.
    ###########################################################################



    
# The main() function runs the above test cases
def main():
    unittest.main(verbosity=2)

# Standard call for main() function
if __name__ == '__main__':
    main()
