
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import xml.etree.ElementTree as ET



options = webdriver.ChromeOptions()
# options.add_experimental_option("debuggerAddress", f'127.0.0.1:{9222}')
svc = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=svc, options=options)
driver.maximize_window()




def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Access elements and attributes in the XML file
    for element in root:
        print(f"Element: {element.tag}, Attribute: {element.attrib}")
        for child in element:
            print(f"  Child: {child.tag}, Value: {child.text}")
            driver.get("https://www.doximity.com/pub/susan-wimmer-pharmacist")
            
            driver.close()
            driver.quit()

if __name__ == "__main__":
    file_path = "path/to/your/file.xml"
    read_xml_file(file_path)
