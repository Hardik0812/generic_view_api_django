# generic_view_api_django
###### Objectives:-
By the end of this article, you should be able to explain:

1. What GenericAPIView is, what mixins are, and how they both come together to create concrete views.
2. Which mixins you use and what they can do.
3. How to create a custom mixin and how to use it.
4. Which generic views you can use and what they do.
5. Generic Views.

 Generic views are a set of commonly used patterns.They're built on top of the APIView class, which we presented in the previous article of this series.Their purpose is for you to quickly build API views that map closely to your database models without repeating yourself.They consist of GenericAPIView, mixins, and concrete views:

GenericAPIView is a more loaded version of APIView. It isn't really useful on its own but can be used to create reusable actions.
Mixins are bits of common behavior. They're useless without GenericAPIView.
Concrete views combine GenericAPIView with the appropriate mixins to create views often used in APIs.
DRF uses different names for concrete views. In the documentation and in code comments, they can be found as concrete view classes, concrete generic views or concrete views.

Since the names are so similar, it's easy to confuse them. Generic views is a word that represents both mixins and concrete views. When using generic views, concrete views is probably the level you'll be working with.

# GenericAPIView
GenericAPIView is a base class for all other generic views. It provides methods like get_object/get_queryset and get_serializer. Although it's designed to be combined with mixins (as it's used within generic views), it's possible to use it on its own:

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

``` class RetrieveDeleteItem(GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```
When extending GenericAPIView, queryset and serializer_class must be set. Alternatively, you can overwrite get_queryset()/get_serializer_class().
Since there are several mixins meant to be used with GenericAPIView, I don't recommend reinventing the wheel by using it on its own.

# Mixins
Mixins provide bits of common behavior. They cannot be used standalone; they must be paired with GenericAPIView to make a functional view. While the mixin classes provide create/retrieve/update/delete actions, you still need to bind the appropriate actions to the methods.

Available mixins:

|Mixin	                |           Usage         |
|-----------------------|-------------------------|
|CreateModelMixin|	      Create a model instance|
|ListModelMixin	|          List a queryset|
|RetrieveModelMixin|	      Retrieve a model instance|
|UpdateModelMixin|	      Update a model instance|
|DestroyModelMixin	|      Delete a model instance|

You can use only one of them or combine them to achieve the desired result.

Here's an example of what a mixin looks like:

```
class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```
As you can see, RetrieveModelMixin provides a function (an action) called retrieve that retrieves an object from the database and returns it in its serialized form.

##### ListModelMixin and CreateModelMixin
ListModelMixin implements an action that returns a (optionally paginated) serialized representation of the queryset.

CreateModelMixin implements an action that creates and saves a new model instance.

Often, they are used together to create a list-create API endpoint:
```
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class CreateListItems(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```
In CreateListItems we used the serializer_class and queryset provided by GenericAPIView.

We defined get and post methods on our own, which used list and create actions provided by the mixins:

1. CreateModelMixin provides a create action
2. ListModelMixin provides a list action

Binding Actions to Methods

Theoretically, that means that you could bind POST methods with list actions and GET methods with create actions, and things would "kind" of work.

For example:
```
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class CreateList(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
       return self.list(request, *args, **kwargs)
```


##### RetrieveModelMixin, UpdateModelMixin and DestroyModelMixin
RetrieveModelMixin, UpdateModelMixin and DestroyModelMixin all deal with a single model instance.

RetrieveModelMixin and UpdateModelMixin both return serialized representations of the object, while DestroyModelMixin, in the case of a success, returns HTTP_204_NO_CONTENT.

You can use one of them or combine them as you see fit.

In this example, we combined all three into a single endpoint for every action that's possible for a detailed view:

```
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class RetrieveUpdateDeleteItem(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```
Actions provided:

1. RetrieveModelMixin provides a retrieve action
2. UpdateModelMixin provides update and partial_update actions
3. DestroyModelMixin provides a destroy action

So, with the RetrieveUpdateDeleteItem endpoint, a user can retrieve, update, or delete a single item.

You can also limit the view to specific actions:
```
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class RetrieveUpdateItem(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

```
In this example, we omitted the DestroyModelMixin and used only the update action from UpdateModelMixin.

##### Grouping Mixins
It's a good idea to have a single view for handling all instances -- listing all instances and adding a new instance -- and another view for handling a single instance -- retrieving, updating, and deleting single instances.

That said, you can combine mixins how you see fit. For example, you could combine the RetrieveModelMixin and CreateModelMixin mixins:
```
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class RetrieveCreate(mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

```


# Custom Mixins
In real-life applications, there's a good chance you'll want some custom behavior, and you'll want it in more than one place. You can create a custom mixin, so you don't need to repeat your code and include it in your view class.

Let's say you want to use a different serializer depending on the request method. You could add a number of if statements to the view, but this can get confusing quickly. Besides, in two months, you'll add another model, and you'll need to do a similar thing again.

In this case, it's a good idea to create a custom mixin to map serializers to the request methods:
```
class SerializerByMethodMixin:
    def get_serializer_class(self, *args, **kwargs):

        return self.serializer_map.get(self.request.method, self.serializer_class)
```
Here, we overrode the get_serializer_class method from GenericAPIView class.

Maybe you want to override other methods, like get_queryset or get_object? Take a look at the code inside the GenericAPIView class, where the DRF creators specify which methods you may want to override.

Now you just need to add SerializerByMethodMixin to your view and set the serializer_map attribute:
```
class ListCreateItems(SerializerByMethodMixin, ListCreateAPIView):

    queryset = Item.objects.all()
    serializer_map = {
        'GET': GetItemSerializer,
        'POST': PostItemSerializer,
    }

```
> Make sure you include the mixin as the first parameter, so its methods are not overridden (higher priority first).

# Custom Base Class

If you're using the mixin for the same type of view multiple times, you can even create a custom base class.

For example:
```
class BaseCreateListView((MixinSingleOrListSerializer, ListCreateAPIView)):
    pass
```
# Concrete Views

Concrete views do most of the work that we need to do on our own when using APIView. They use mixins as their basic building blocks, combine the building blocks with GenericAPIView, and bind actions to the methods.

Take a quick look at the code for one of the concrete view classes, ListCreateAPIView:
```
# https://github.com/encode/django-rest-framework/blob/3.12.4/rest_framework/generics.py#L232

class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```
As you can see, it's fairly simple and looks very similar to what we created on our own when using mixins. They extend the appropriate mixins and GenericAPIView. They also define each of the relevant methods and bind the appropriate actions to them.

Unless you need highly customized behavior, this is the view to go with if you're using generic views.

There are nine classes, each providing a combination of behavior that you might need:

|Class|	Usage|	Method handler	|Extends mixin|
|CreateAPIView|	create-only|	post|	CreateModelMixin|
|ListAPIView	|read-only for multiple instances|	get|	ListModelMixin|
|RetrieveAPIView|	read-only for single instance|	get	|RetrieveModelMixin|
|DestroyAPIView	|delete-only for single instance|	delete|	DestroyModelMixin|
|UpdateAPIView	|update-only for single instance|	put, patch	|UpdateModelMixin|
|ListCreateAPIView|	read-write for multiple instances|	get, post	|CreateModelMixin, ListModelMixin|
|RetrieveUpdateAPIView|	read-update for single instance|	get, put, patch	|RetrieveModelMixin, UpdateModelMixin|
|RetrieveDestroyAPIView|	read-delete for single instance	|get, delete	|RetrieveModelMixin, DestroyModelMixin|
|RetrieveUpdateDestroyAPIView|	read-update-delete for single instance|	get, put, patch, delete	|RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin|
Here's another helpful table that shows which class a particular method handler is mapped back to:

Class	get	post	put/patch	delete
CreateAPIView		✓		
ListAPIView	✓			
RetrieveAPIView	✓			
DestroyAPIView				✓
UpdateAPIView			✓	
ListCreateAPIView	✓	✓		
RetrieveUpdateAPIView	✓		✓	
RetrieveDestroyAPIView	✓			✓
RetrieveUpdateDestroyAPIView	✓		✓	✓
All classes that extend from a concrete view need:

queryset
serializer class
Additionally, you can provide policy attributes, as explained in the first article in this series.

Next, we'll look at examples of each of the nine concrete views in action.

CreateAPIView
By extending CreateAPIView, here, we created an endpoint where the user can create a new item:

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

class CreateItem(CreateAPIView):
    permission_classes = [IsAdminUser]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
We added a policy attribute so that the endpoint is accessible only by the admin.

ListAPIView
Here, we extended ListAPIView to create an endpoint where all the "not-done" items are listed:

from rest_framework.generics import ListAPIView

class ItemsNotDone(ListAPIView):

    queryset = Item.objects.all().filter(done=False)
    serializer_class = ItemSerializer
Our queryset is filtered based on the done field. It doesn't contain any additional policies, so it's accessible to any user.

Keep in mind that each of these views needs to be included in the URLs individually:

# urls.py

from django.urls import path
from .views import ListItems

urlpatterns = [
   path('all-items', ListItems.as_view())
]
RetrieveAPIView
While ListAPIView returns a list of all the items, RetrieveAPIView is meant for retrieving a single item:

from rest_framework.generics import RetrieveAPIView

class SingleItem(RetrieveAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
Example urls.py for RetrieveAPIView (and other views for a single instance):

from django.urls import path
from .views import SingleItem
>
urlpatterns = [
   path('items/<pk>', SingleItem.as_view())
]
DestroyAPIView
Extending DestroyAPIView creates an endpoint with the sole purpose of deleting a single item:

from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated


class DeleteItem(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
Access is restricted to authenticated users only.

UpdateAPIView
Endpoint for updating a single item:

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle


class UpdateItem(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
Here, using policy attributes, we throttled the number of requests and restricted the endpoint to authenticated users.

ListCreateAPIView
ListCreateAPIView is the first concrete view class with more than one responsibility, listing all items and creating a new item:

from rest_framework.generics import ListCreateAPIView

class ListCreateItems(ListCreateAPIView):

    authentication_classes = [TokenAuthentication]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
In this example, the user is authenticated with a token.

RetrieveUpdateAPIView
Extending RetrieveUpdateAPIView creates an endpoint for retrieving and updating a single item:

from rest_framework.generics import RetrieveUpdateAPIView

class RetrieveUpdateItem(RetrieveUpdateAPIView):
    renderer_classes = [JSONRenderer]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
Here, we used a policy attribute to return the data in JSON format.

RetrieveDestroyAPIView
By extending RetrieveDestroyAPIView, here, we created an endpoint for retrieving and deleting a single item:

from rest_framework.generics import RetrieveDestroyAPIView

class RetrieveDeleteItem(RetrieveDestroyAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
RetrieveUpdateDestroyAPIView
Here, by extending RetrieveUpdateDestroyAPIView, we created an endpoint where all possible actions for a single item are accessible: retrieving, (partially) updating, and deleting.

from rest_framework.generics import RetrieveUpdateDestroyAPIView

class RetrieveUpdateDeleteItem(RetrieveUpdateDestroyAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
Conclusion
Generic views offer a variety of pre-built solutions.

If you don't have any special requirements, concrete views (i.e., RetrieveDestroyAPIView) are a great way to go. If you need something less rigorous, you can use concrete classes as building blocks -- GenericAPIView and mixins (e.g., UpdateModelMixin). This will still save some work over just using the APIView class.