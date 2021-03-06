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
            output+= "<a href = '/restaurants/new'> Add a New Restaurant</a></br></br>"
            for restaurant in restaurants:
                output+= self.name_format(restaurant.name)
                output+=self.edit_format('/restaurants/'+str(restaurant.id)+'/edit')
                output+=self.delete_format('/restaurants/'+str(restaurant.id)+'/delete')
                output+="</br>"
            output += "</body></html>"
            self.wfile.write(output)
            return
        
        if self.path.endswith("/edit"):
            rid= self.path.split('/')[2]
            #print self.path.split('/')[1], self.path.split('/')[2]
            restaurant = session.query(Restaurant).filter_by(id = rid).one()
            self.response_ok()#return sucessful response codes
            output = "<html><body>"
            output += "<h1>"
            output += restaurant.name
            output += "</h1>"
            output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % rid
            output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % restaurant.name
            output += "<input type = 'submit' value = 'Rename'>"
            output += "</form>"
            output += "</body></html>"
            self.wfile.write(output)
            return

        if self.path.endswith("/delete"):
            rid= self.path.split('/')[2]
            restaurant = session.query(Restaurant).filter_by(id = rid).one()
            self.response_ok()#return sucessful response codes
            output = "<html><body>"
            output += "<h1>Delete %s </h1>"%restaurant.name
            output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % str(rid)
            output += "<input type = 'submit' value = 'Delete'>"
            output += "</form>"
            output += "</body></html>"
            self.wfile.write(output)
            return

        
        if self.path.endswith("/restaurants/new"):
            #restaurants = session.query(Restaurant).all()
            self.response_ok()#return sucessful response codes
            output = ""
            output += "<html><body>"
            output += "<h1>Make a New Restaurant</h1>"
            output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
            output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
            output += "<input type='submit' value='Create'>"
            output += "</form></body></html>"
            self.wfile.write(output)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('newRestaurantName')
              
                    #Create new Restaurant Object
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
              
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                rid = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=rid).one()
                if restaurant !=[]:
                    session.delete(restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('newRestaurantName')
              
                    #edit Restaurant Object
                    rid= self.path.split('/')[2]
                    restaurant = session.query(Restaurant).filter_by(id = rid).one()
                    if restaurant !=[]:
                        restaurant.name = messagecontent[0]
                        session.add(restaurant)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location','/restaurants')
                        self.end_headers()
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
