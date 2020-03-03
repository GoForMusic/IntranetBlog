from mainblog import Admin, ModelView, app, AdminIndexView
from mainblog.routes import current_user, redirect, url_for, request, db, User, Post



class AdminView(ModelView):
    page_size = 50
    home_page = False

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login_page', next=request.url))



#admin dashboard

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))