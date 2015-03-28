from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#playing with decorators
def add_br(fn):#decorator
    def add(*args):
        return fn(*args)+"</br>"
    return add

def outer(arg):
    def add_ref(fn):#decorator
        def add(*args):
            return "<a href ='"+fn(*args)+"'>"+arg+"</a></br>"
        return add
    return add_ref
#playing with decorators



class WebServerHandler(BaseHTTPRequestHandler):
    def response_ok(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @add_br
    def name_format(self, name):
        return name

    @outer('Edit')
    def edit_format(self, link):
        return link
    @outer('Delete')
    def delete_format(self, link):
        return link
    
    def do_GET(self):
        if self.path.endswith("/restaurants"):
            restaurants = session.query(Restaurant).all()
            self.response_ok()#return sucessful response codes
            output = "<html><body>"
            for restaurant in restaurants:
                output+= self.name_format(restaurant.name)
                output+=self.edit_format('')
                output+=self.delete_format('')
                output+="</br>"
            output += "</body></html>"
            self.wfile.write(output)
            return

        if self.path.endswith("/restaurants/new"):
            restaurants = session.query(Restaurant).all()
            self.response_ok()#return sucessful response codes
            output = ""
            output += "<html><body>"
            output += "<h1>Add new Restaurant</h1>"
            output += '''<form method='POST' enctype='multipart/form-data'
                        action='/restaurants'><h2>Restaurant Name</h2>
                        <input name="message" type="text" ><input type="submit"
                        value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output +=  "<html><body>"
            output += "<h1>Add new Restaurant</h1>"
            output += "<h1>Name: %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data'
                        action='/restaurants'><h2>Restaurant Name</h2>
                        <input name="message" type="text" ><input type="submit"
                        value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            restaurant1 = Restaurant(name = messagecontent[0])
            session.add(restaurant1)
            session.commit()
            self.do_GET()
            print output
        except:
            pass
        

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s"  % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
	main()
