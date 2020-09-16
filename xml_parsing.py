import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json, os

class memoqRULES():
    def __init__(self, DIRECTORY):
        self.DIR = DIRECTORY
        self.source = []
        os.chdir(self.DIR)

    def get_json(self):
        """Will search DIR defined at init. If any files with extension .NOR that do not start with "_" are found, the function will export all text and markup within the <Seg> tags within that XML.
           The resulting JSONs can be imported into memoQ for translation."""
        for fil in os.listdir(self.DIR):
            if fil.endswith(".NOR") and not fil.startswith("_"):
                self.source.append(fil)

        if self.source:
            for fil in self.source:
           
                #Parsing med BeautifulSoup har bedre resultat enn med XML
                with open(fil, "r", encoding="utf-16-le") as f:
                    data = f.read()
                soup = BeautifulSoup(data, "xml")
                segments = soup.find_all("Seg")        
                output = {}

                for elem in segments:
                    
                    #Dette gjør at jeg også får med mixede segmenter. Som <WS/>-taggene.
                    #Ellers kunne jeg bare brukt elem.text
                    textvalue = ""
                    for child in elem.children:
                        textvalue += str(child)

                    output[elem.get("SegID")] = textvalue

                with open(fil + '.json', 'w', encoding="utf-16") as outfile:
                    json.dump(output, outfile)
        else:
            print("No .NOR file found")

    def give_json(self, **kwargs):
        """Will search DIRECTORY and populate XMLs with present json exports from memoQ.
            Kwargs: DIRECTORY=self.DIR"""
        
        DIRECTORY = self.DIR
        for key, value in kwargs.items():
            if key == "DIRECTORY":
                DIRECTORY = value

        for jsonfil in os.listdir(DIRECTORY):
            if jsonfil.endswith("_nor.json"):
                with open(jsonfil, encoding="utf-16-le") as f:
                    data = f.read()
                    translation = json.loads(data)
                
                xmlfilename = jsonfil.rstrip("_nor.json")
                print(xmlfilename)

                with open(xmlfilename, "rb") as f:
                    data = f.read()
                soup = BeautifulSoup(data, "xml", from_encoding="utf-16-le")
                segments = soup.find_all("Seg")

                for elem in segments:
                    elem.string = translation[elem.get("SegID")]

                with open(xmlfilename, "w", encoding="utf-16-le") as f:
                    f.write(soup.encode("utf-16").decode("utf-16"))

                # tree = ET.parse(xmlfilename)

                # for elem in tree.iter("Seg"):
                #     elem.text = translation[elem.attrib["SegID"]]

                # tree.write(xmlfilename)

