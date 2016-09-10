import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                        autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    blogPost = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    def render_front(self, title="", blogPost="", error=""):
        blogPosts = db.GqlQuery("SELECT * FROM BlogPost "
                           "ORDER BY created DESC")
        self.render("front.html", title=title, blogPost=blogPost, error=error, blogPosts=blogPosts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        blogPost = self.request.get("blogPost")

        if title and blogPost:
            a = BlogPost(title = title, blogPost = blogPost)
            a.put()

            self.redirect("/")
        else:
            error = "We need both a title and a post!"
            self.render_front(title, blogPost,error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
