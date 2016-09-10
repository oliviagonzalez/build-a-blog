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


class Index(Handler):
    def render_front(self, title="", blogPost="", error=""):
        blogPosts = db.GqlQuery("SELECT * FROM BlogPost "
                           "ORDER BY created DESC")
        self.render("frontpage.html", title=title, blogPost=blogPost, error=error, blogPosts=blogPosts)

    def get(self):
        self.render_front()

class Blog(Handler):
    def render_blog(self, title="", blogPost="", error=""):
        blogPosts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 5")
        self.render("blog.html", title=title, blogPost=blogPost, error=error, blogPosts=blogPosts)

    def get(self):
        self.render_blog();

class AddNewPost(Handler):
    def render_new(self, title="", blogPost="", error=""):
        blogPosts = db.GqlQuery("SELECT * FROM BlogPost "
                           "ORDER BY created DESC")
        self.render("add-new-post.html", title=title, blogPost=blogPost, error=error, blogPosts=blogPosts)

    def get(self):
        self.render_new()

    def post(self):
        title = self.request.get("title")
        blogPost = self.request.get("blogPost")

        if title and blogPost:
            a = BlogPost(title = title, blogPost = blogPost)
            a.put()

            self.redirect("/")
        else:
            if title:
                error = "The submission requires a post."
            if blogPost:
                error = "The submission requires a title."
            self.render_new(title, blogPost, error)

app = webapp2.WSGIApplication([
        ('/', Index),
        ('/blog', Blog),
        ('/newpost', AddNewPost)
        ], debug=True)
