from mainblog import Admin, ModelView, app, AdminIndexView
from mainblog.routes import current_user, redirect, url_for, request, db, User, Post, Comments, Groups, Position



class AdminView(ModelView):
    page_size = 50
    home_page = False

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login_page', next=request.url))


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
admin.add_view(AdminView(Comments, db.session))
admin.add_view(AdminView(Groups, db.session))
admin.add_view(AdminView(Position, db.session))