from rest_framework import routers
from user.api import *
from posts.api import *
from comments.api import *
from likes.api import *

router = routers.DefaultRouter(trailing_slash=True)


#user
router.register(r"register", RegisterViewSet),
router.register(r"login", LoginViewSet),
router.register(r"userprofile", UserProfileViewSet),
#posts
router.register(r"posts", PostViewset),
#comments
router.register(r"comments", CommentViewset),
#likes
router.register(r"likes", LikeViewSet),
