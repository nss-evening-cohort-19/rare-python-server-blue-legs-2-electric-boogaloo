from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views.comment_requests import create_comment, delete_comment, get_all_comments, get_single_comment, update_comment
from views.post_request import create_post, delete_post, get_all_posts, get_single_post, update_post
from views.subscription_request import create_subscription, delete_subscription, get_all_subscriptions, get_single_subscription, update_subscription
from views.category_requests import create_category, delete_category, get_all_categories, get_single_category, update_category
from views.user import create_user, login_user
from views.reaction_request import create_reaction, get_all_reactions, get_single_reaction, delete_reaction, update_reaction
from views.post_reaction_request import create_post_reaction, delete_post_reaction, update_post_reaction, get_all_post_reactions, get_single_post_reaction


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)
        
        response = {}
        
        parsed = self.parse_url()
        
        if '?' not in self.path:
            ( resource, id ) = parsed
            
            if resource == 'posts':
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == 'comments':
                if id is not None:
                    response = f"{get_single_comment(id)}"
                else:
                    response = f"{get_all_comments()}"
            elif resource == 'reactions':
                if id is not None:
                    response = f"{get_single_reaction(id)}"
                else:
                    response = f"{get_all_reactions()}"
            elif resource == 'postreactions':
                if id is not None:
                    response = f"{get_single_post_reaction(id)}"
                else:
                    response = f"{get_all_post_reactions()}"
            elif resource == 'categories':
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            elif resource == 'subscriptions':
                if id is not None:
                    response = f"{get_single_subscription(id)}"
                else:
                    response = f"{get_all_subscriptions()}"
            elif resource == 'tags':
                pass
            elif resource == 'postags':
                pass
 
        self.wfile.write(response.encode())
        
    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        (resource, id) = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        elif resource == 'register':
            response = create_user(post_body)
        elif resource == 'posts':
            response = create_post(post_body)
        elif resource == 'subscriptions':
            response = create_subscription(post_body)
        elif resource == 'comments':
            response = create_comment(post_body)
        elif resource == 'reactions':
            response = create_reaction(post_body)
        elif resource == 'postreactions':
            response = create_post_reaction(post_body)
        elif resource == 'categories':
            response = create_category(post_body)
        elif resource == 'subscriptions':
            pass
        elif resource == 'tags':
            pass
        elif resource == 'postags':
            pass

        self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url()

        success = False

        if resource == "posts":
            success = update_post(id, post_body)
        elif resource == 'comments':
            success = update_comment(id, post_body)
        elif resource == 'reactions':
            success = update_reaction(id, post_body)
        elif resource == 'postreactions':
            success = update_post_reaction(id, post_body)
        elif resource == 'categories':
            success = update_category(id, post_body)
        elif resource == 'subscriptions':
            success = update_subscription(id, post_body)
        elif resource == 'tags':
            pass
        elif resource == 'postags':
            pass

        
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)
        
        (resource, id) = self.parse_url()
        
        if resource == "posts":
            delete_post(id)
        elif resource == 'comments':
            delete_comment(id)
        elif resource == 'reactions':
            delete_reaction(id)
        elif resource == 'postreactions':
            delete_post_reaction(id)
        elif resource == 'categories':
            delete_category(id)
        elif resource == 'subscriptions':
            delete_subscription(id)
        elif resource == 'tags':
            pass
        elif resource == 'postags':
            pass
            
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
