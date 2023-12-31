from rest_framework import routers
from user.api import *
from posts.api import *
from comments.api import *


router = routers.DefaultRouter(trailing_slash=True)


#user
router.register(r"register", RegisterViewSet, basename="register"),
router.register(r"login", LoginViewSet, basename="login"),
router.register(r"userprofile", UserViewSet, basename="userprofile"),
#posts
router.register(r"posts", PostViewset, basename="posts"),
#comments
router.register(r"comments", CommentViewset, basename="comments"),
