import os
import xml.etree.ElementTree as xet
from zipfile import ZipFile
import pandas as pd
import logging

logging.basicConfig(filename="Convert.log", level=logging.INFO,
                    format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")


class Convert:
    """
    The following code will extract the xml file from the zip and will convert the xml
    file to csv formatted file.
    """

    def __init__(self, filename):
        self.filename = filename

    def extract_file(self):
        """
        Will extract the xml file from 1.zip
        """
        with ZipFile(self.filename, "r") as z:
            z.extractall(os.curdir)
            logging.info(".xml file extracted")

    def convert_file(self):

        """
        Finding the file to be converted to csv
        """

        filepath = None
        for (dirpath, dirnames, filenames) in os.walk(os.curdir):
            for f in filenames:
                if f == "DLTINS_20210117_01of01.xml":
                    filepath = os.path.join(os.curdir, f)

        # parsing the file to get the root of the xml file
        tree = xet.parse(filepath)
        root = tree.getroot()

        # finding the parent tag
        parent = 'TermntdRcrd'

        # finding the 1st child tag
        child1 = 'FinInstrmGnlAttrbts'

        # finding the 2nd child tag
        child2 = 'Issr'

        # determining the Columns
        children = ['Id', 'FullNm', 'ClssfctnTp', 'CmmdtyDerivInd', 'NtnlCcy']
        cols = [child1 + '.' + k for k in children]
        cols.append(child2)

        # Fetching the rows
        rows = list()
        for i in root.iter():

            # If parent is found initialize the list
            if parent in i.tag:
                temp = [None for x in range(len(children) + 1)]
                for child in i:

                    # If required child has been found
                    if child1 in child.tag:

                        # Fetching the grandchild
                        for j in child:
                            for k in range(len(children)):

                                # If grandchildren found, updating the temp
                                if children[k] in j.tag:
                                    temp[k] = j.text

                    # If Issr is found
                    if child2 in child.tag:
                        temp[5] = child.text

                # Adding data to the rows
                rows.append(temp)

        # Creating dataframe and saving the file in csv
        df = pd.DataFrame(data=rows, columns=cols)
        df.to_csv('output.csv')
        logging.info("The xml file has been converted to csv file")


if __name__ == '__main__':
    p = Convert(filename="1.zip")
    p.extract_file()
    p.convert_file()
