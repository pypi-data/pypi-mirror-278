import requests
from selenium import webdriver
import sqlite3
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queue import PriorityQueue

#wishlist:
#agregar funcion test con un solo parametro, pensar en tener eso en el back-end
#diccionario de configuracion en vez de parametros
class customDriver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super(customDriver, self).__init__(*args, **kwargs)
        #tomar este valor del usuario luego
        self.testId = -1
        self.session = requests.Session()
        self.baseURL = "http://127.0.0.1:8000/api/self_healing"
        self.find_element_count = 0
        #this variable may not be needed
        self.elements_healing_queue = []
        # lista de elementos que fueron exitosos y tenemos que guardar en la base de datos
        self.elements_persist_queue = []
        #crear base de datos sqlite
        self.conn = sqlite3.connect('example.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                htmlid TEXT,
                type TEXT,
                name TEXT,
                class TEXT,
                aria_autocomplete TEXT,
                title TEXT,
                href TEXT,
                htmltext TEXT,
                value TEXT,
                aria_label TEXT,
                role TEXT
            )
        ''')
        #para obtener el numero de elementos, ordenar ids desc
    def setup(self, test, script, collection, personal_access_token):
        #otbener el test con este nombre, si no existe crear uno y asignarlo al script, si no existe el script con ese nombre crearlo y asignarlo a la coleccion, si no existe una coleccion con ese nombre crearla y asignarlo
        #todo eso es dentro del API, aqui solo mandar un request autenticado al endpoint
        self.session.headers.update({
            'Authorization': f'{personal_access_token}',
        })
        finalURL = f'{self.baseURL}/selfHealingSetup'
        data = {'test': test, 'script': script, 'collection': collection}
        response = self.session.post(finalURL, json=data)
        data = response.json()
        print(data["testid"])
        if response.status_code >= 200 and response.status_code < 300:
            if 'testid' in data:
                self.testId = data["testid"]
                return response
            else:
                raise Exception("Data returned from request was unexpected")

        else: 
            raise Exception("request failed for setup")


    def makeReport(self, selenium_selector):
        if self.testId != -1:
            finalURL = f'{self.baseURL}/create_report_item'
            data = {'selenium_selector': selenium_selector, 'testId': str(self.testId)}
            # self.save_screenshot('screenshot_test.png')

            response = self.session.post(finalURL, json=data)
            report_id = int(response.text)
            if response.status_code >= 200 and response.status_code < 300:
                if report_id:
                    return report_id
                else:
                    raise Exception("Data returned from request was unexpected")
            else:
                raise Exception("request failed for makeReport")
        else:
            #retornar algo que no es el reportid maybe, mostrar un error
            raise Exception("setup function did not run")

    def startReport(self, reportId):
        if self.testId != -1:
            finalURL = f'{self.baseURL}/start_report'
            data = {'reportId': f'{reportId}'}
            self.save_screenshot('screenshot_test.png')

            with open('screenshot_test.png', 'rb') as img_file:
                files = {'img': ('screenshot_test.png', img_file, 'image/jpeg')}
                response = self.session.post(finalURL, data=data, files=files)
                data = response.json()
                if response.status_code >= 200 and response.status_code < 300:
                    if 'reportid' in data:
                        return response
                    else:
                        raise Exception("Data returned from request was unexpected")
                else:
                    raise Exception("request failed for startReport")
        else:
            raise Exception("setup function did not run")

    def endReport(self, reportId, healingDescription, status):
        if self.testId != -1:
            finalURL = f'{self.baseURL}/end_report'
            data = {'status': f'{status}', 'healingDescription': f'{healingDescription}', 'reportId': f'{reportId}'}
            self.save_screenshot('screenshot_test.png')
            with open('screenshot_test.png', 'rb') as img_file:
                files = {'img': ('screenshot_test.png', img_file, 'image/jpeg')}
                response = self.session.post(finalURL, data=data, files=files)
                data = response.json()
                if response.status_code >= 200 and response.status_code < 300:
                    if 'reportid' in data:
                        return response
                    else:
                        raise Exception("Data returned from request was unexpected")
                else:
                    raise Exception("request failed for endReport")
        else:
            raise Exception("setup function did not run")

    def find_element_custom(self, query, queryText):
        reportId = self.makeReport(str(query))
        self.find_element_count += 1

        try:
            #Buscar elemento antes con WebDriverWait
            WebDriverWait(self, 5).until(
                EC.presence_of_element_located((query, queryText))
           )

            current_element = self.find_element(query, queryText)
            #Elemento procesado exitosamente
            current_element_data = {
                "tag": current_element.tag_name,
                "htmlid": current_element.get_attribute("id") or None,
                "type": current_element.get_attribute("type") or None,
                "name": current_element.get_attribute("name") or None,
                "class": current_element.get_attribute("class") or None,
                "aria_autocomplete": current_element.get_attribute("aria-autocomplete") or None,
                "title": current_element.get_attribute("title") or None,
                "href": current_element.get_attribute("href") or None,
                "htmltext": current_element.text or None,
                "value": current_element.get_attribute("value") or None,
                "aria_label": current_element.get_attribute("aria-label") or None,
                "role": current_element.get_attribute("role") or None
            }
            self.elements_persist_queue.append(current_element_data)
            #enviar endpoint a end_report, este es el reporte final que fue un exito
            self.endReport(reportId, 'Success without self-healing', 'Success')
            return current_element

        except:

            self.startReport(reportId)
            sqlquery = "SELECT * FROM elements WHERE id = ?"
            element_to_test = pd.read_sql_query(sqlquery, self.conn, params=(self.find_element_count,))
            if not element_to_test.empty:
                probability, new_element = self._self_healing(element_to_test)
                new_element_dict = new_element.to_dict()
                new_query = query
                new_query_text = queryText
                try:
                    if query == By.NAME:
                        new_query_text = new_element["name"]
                    elif query == By.CSS_SELECTOR:
                        raise Exception(":/")
                    elif query == By.CLASS_NAME:
                        new_query_text = new_element["class"]
                    elif query == By.ID:
                        new_query_text = new_element["htmlid"]
                    elif query == By.LINK_TEXT:
                        new_query_text = new_element["href"]
                    elif query == By.PARTIAL_LINK_TEXT:
                        new_query_text = new_element["href"]
                    elif query == By.TAG_NAME:
                        new_query_text = new_element["tag"]
                    elif query == By.XPATH:
                        raise Exception(":/")
                    WebDriverWait(self, 5).until(
                        EC.presence_of_element_located((query, new_query_text))
                    )
                    self.endReport(reportId, f'self-healing done, element found with probability {probability*100}%', 'Success')
                    return self.find_element(query, new_query_text)

                except:
                    text = PriorityQueue()
                    selector = PriorityQueue()
                    for locator in new_element_dict:
                        if locator == "htmlid" and new_element_dict[locator] != 'None':
                            new_query = By.ID
                            new_query_text = new_element_dict[locator]
                            text.put((0, new_query_text))
                            selector.put((0, new_query))
                        elif locator == "name" and new_element_dict[locator] != 'None':
                            new_query = By.NAME
                            new_query_text = new_element_dict[locator]
                            text.put((1, new_query_text))
                            selector.put((1, new_query))
                        elif locator == "class" and new_element_dict[locator] != 'None':
                            new_query = By.CLASS_NAME
                            new_query_text = new_element_dict[locator]
                            text.put((6, new_query_text))
                            selector.put((6, new_query))
                        elif locator == "tag" and new_element_dict[locator] != 'None':
                            new_query = By.TAG_NAME
                            new_query_text = new_element_dict[locator]
                            text.put((3, new_query_text))
                            selector.put((3, new_query))
                        elif locator == "type" and new_element_dict[locator] != 'None':
                            new_query = By.XPATH
                            new_query_text = "//*[@type='text']"
                            text.put((4, new_query_text))
                            selector.put((4, new_query))
                        elif locator == "text" and new_element_dict[locator] != 'None':
                            new_query = By.XPATH 
                            new_query_text = "//*[contains(text(), " + new_element_dict[locator] + ")]" 
                            text.put((5, new_query_text))
                            selector.put((5, new_query))
                    _, new_query_text = text.get()
                    _, new_query = selector.get()
                    WebDriverWait(self, 5).until(
                        EC.presence_of_element_located((new_query, new_query_text))
                    )
                    self.endReport(reportId, f'self-healing done, element found with a different locator, probability of match: {probability*100}%', 'Success')
                    return self.find_element(new_query, new_query_text)

                    
            else:
                self.endReport(reportId, 'self-healing could not be performed and element was not found', 'Failed')
                raise ValueError("llego a la excepcion porque no pudo haber self-healing")


    def quit(self):
        self.cursor.execute('''
            SELECT * FROM elements;
        ''')
        elements = self.cursor.fetchall()
        if len(self.elements_persist_queue) == self.find_element_count:
            self.cursor.execute('DROP TABLE elements')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS elements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag TEXT,
                    htmlid TEXT,
                    type TEXT,
                    name TEXT,
                    class TEXT,
                    aria_autocomplete TEXT,
                    title TEXT,
                    href TEXT,
                    htmltext TEXT,
                    value TEXT,
                    aria_label TEXT,
                    role TEXT
                )
            ''')
            df = pd.DataFrame(self.elements_persist_queue)
            df.to_sql('elements', self.conn, if_exists='append', index=False)
            self.cursor.execute('SELECT * FROM elements')
            rows = self.cursor.fetchall()
        super().quit()

    def _self_healing(self, element_to_test):
        elements = self.find_elements("xpath", "//*")
        data = []
        test_data_list = []
        for element in elements:
            element_data = {
                "tag": element.tag_name,
                "htmlid": element.get_attribute("id") or None,
                "type": element.get_attribute("type") or None,
                "name": element.get_attribute("name") or None,
                "class": element.get_attribute("class") or None,
                "aria_autocomplete": element.get_attribute("aria-autocomplete") or None,
                "title": element.get_attribute("title") or None,
                "href": element.get_attribute("href") or None,
                "htmltext": element.text or None,
                "value": element.get_attribute("value") or None,
                "aria_label": element.get_attribute("aria-label") or None,
                "role": element.get_attribute("role") or None,
            }
            data.append(element_data)

        train_data  = pd.DataFrame(data)
        test_data = element_to_test
        
        train_data.fillna('None', inplace=True)
        test_data.fillna('None', inplace=True)
        encoder = OneHotEncoder(handle_unknown='ignore')

        combined_data = pd.concat([train_data.drop('htmlid', axis=1), test_data.drop('htmlid', axis=1)])

        encoded_combined_data = encoder.fit_transform(combined_data)

        encoded_train_data = encoded_combined_data[:len(train_data)]
        encoded_test_data = encoded_combined_data[len(train_data):]

        rf = RandomForestClassifier(n_estimators=100, random_state=42)

        rf.fit(encoded_train_data, range(len(train_data)))

        predicted_index = rf.predict(encoded_test_data)[0]
        probabilities = rf.predict_proba(encoded_test_data)[0]


        return max(probabilities), train_data.iloc[predicted_index]

