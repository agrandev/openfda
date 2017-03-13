import http.client
import http.server
import json



class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"

    def get_event(self):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        #search = patient.reaction.reactionnedrapt:"fati"
        conn.request('GET',self.OPENFDA_API_EVENT+'?limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        return events

    def get_medicamentos(self):

        events=self.get_event()

        medicamentos = []
        results = events["results"]
        for event in results:

            medicamentos += [event["patient"]["drug"][0]["medicinalproduct"]]

        return medicamentos

    def get_incognita(self):
        incognita = self.path.split("=")[1]
        print (incognita)
        return incognita



    def get_search(self):

        incognita = self.get_incognita()
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT+'?search=patient.drug.medicinalproduct:' +incognita + '&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        return events

    def get_empresas(self):
        events=self.get_search()

        empresas = []
        results = events["results"]

        for event in results:

                empresas += [event["companynumb"]]
        return empresas



    def get_main_page(self):
        html = """
        <html>
            <head>
            </head>
            <body>
                <form method="get" action="receive">
                    </input>
                    <input type = "submit" value="Drug List:Send to OpenFDA">
                </form>
                <form method="get" action="search">
                    <input type = "text" name="drug"></input>
                    <input type = "submit" value="Drug Search LYRICA: Send to OpenFDA">
                </form>
            </body>
        </html>
        """
        return html


    def get_second_page(self, medicamentos):
        s=""
        for med in medicamentos:
            s += "<li>" +med+ "</li>"


        html = """
        <html>
        <head></head>
        <body>
            <h1>Medical Products</h1>
            <ul>
                %s
            </ul>
        </body>
        </html>
        """%(s)

        return html



    def do_GET(self):


        main_page= False
        is_event=False
        is_search=False
        if self.path== "/":
            main_page= True
        elif self.path == "/receive":
            is_event = True
        elif self.path.find("search"): # == "/search?drug=LYRICA":
            is_search = True

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()



        if main_page:
            html = self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))
        elif is_event:
            medicamentos= self.get_medicamentos()
            event = self.get_event()
            html2 = self.get_second_page(medicamentos)
            self.wfile.write(bytes(html2, "utf8"))
        elif is_search:
            empresas= self.get_empresas()
            html3 = self.get_second_page(empresas)
            self.wfile.write(bytes(html3, "utf8"))

        return
