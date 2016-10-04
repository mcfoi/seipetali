from django.http import Http404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from pythonutils.args import *
from tokens import token_generator


__all__ = ('post_to_dict', 'deferrable', 'called', 'resume_deferred')


## Convert a POST structure to a dictionary.
#
#  Django doesn't use standard "dict"s to store POST data. Use this to
#  convert. It's pretty simple.
#
#  @param[in]  post  Django POST data.
#  @returns    A dictionary containing the converted POST data.
#
def post_to_dict(post):
    return dict([(k, post[k]) for k in post.keys()])


## Redirect to an URL using deferral.
#
#  Similar to the standard Django "redirect", but stores additional information
#  in the request session to facilitate resuming. A token is generated to
#  uniquely identify this deferral.
#
#  @param[in]  request    A Django request.
#  @param[in]  url        The destination URL.
#  @param[in]  return_to  The URL to return to once the deferral is complete.
#  @returns    A Django response object.
#
def redirect_defer(request, url, return_to, **kwargs):
    token = token_generator.make_token(request.user)
    request.session[token] = {
        'token': token,
        'return_to': return_to,
        'post': post_to_dict(request.POST),
    }
    request.session[token].update(kwargs)
    return redirect(url + '?token=%s'%token)


## Convert a deferral action into an URL.
#
#  Actions can be given as either a tuple, containing the action URL and and
#  an iterable of indices into a list of arguments, or just as an URL.
#
def action_to_url(action, args=[], kwargs={}):
    if isinstance(action, tuple):
        target_url = reverse(action[0], args=[a(args, kwargs) for a in action[1]])
    else:
        target_url = reverse(action)
    return target_url


## Declares a view as deferrable.
#
#  A deferrable view is one with a form containing one or more submit buttons
#  connected to other views. When the form is submitted using one of these
#  buttons processing is transferred to the connected view. That view may then
#  return to this view when ready, and all form field entries will be restored.
#
#  @param[in]  actions  Dictionary mapping submit button names to view names.
#  @returns    The decorated view function.
#
def deferrable(actions={}, store_background=False):
    def deferrable_inner(view):

        def deferrable_view(request, *args, **kwargs):

            # Check for a resumed view.
            retoken = request.GET.get('retoken', None)
            if retoken:

                # There must be a matching token in the session.
                try:
                    post = request.session[retoken]['post']
                except:
                    raise Http404

                # Add a flag indicating a resume and provide the post data.
                request.defer_resumed = True
                request.defer_post = post
                return view(request, *args, **kwargs)

            else:
                request.defer_resumed = False

            # Check for a defer action.
            if request.method == 'POST':
                for name, action in actions.iteritems():
                    if name in request.POST:
                        extra = {}

                        # If requested, store the background.
                        if store_background:
                            old_method = request.method
                            request.method = 'GET'
                            request.defer_initial = request.POST
                            extra['background'] = view(request, *args, **kwargs).content
                            request.method = old_method

                        # Perform the redirect.
                        target_url = action_to_url(action, args, kwargs)
                        return redirect_defer(request, target_url, request.path, **extra)

            # Nothing fancy going on, render the view as usual.
            request.defer_post = {}
            return view(request, *args, **kwargs)

        return deferrable_view
    return deferrable_inner


def chainable(actions={}, back_tag=None):
    def chainable_inner(view):

        def chainable_view(request, *args, **kwargs):

            # Try and pull out a token.
            token = request.REQUEST.get('token', None)

            # If a back tag was given and is found, return.
            if back_tag and back_tag in request.REQUEST:
                try:
                    return_to = request.GET['return_to']
                except KeyError:
                    raise Http404

                # Return with an optional token.
                if token:
                    return redirect(return_to + '?token=%s'%token)
                else:
                    return redirect(return_to)

            # Search for actions.
            for name, action in actions.iteritems():
                if name in request.REQUEST:
                    target_url = action_to_url(action, args, kwargs)
                    if token:
                        return redirect(target_url + '?token=%s'%token)
                    else:
                        return redirect(target_url)

            return view(request, *args, **kwargs)

        return chainable_view
    return chainable_inner


def called(cancel_tags=[], use_background=False):
    def called_inner(view):

        def called_view(request, *args, **kwargs):

            # When first called the token generated by the deferring view is passed
            # in GET, but in successive submits on this view the token will be passed
            # in POST. Use REQUEST to cover both of these.
            try:
                token = request.REQUEST['token']
            except KeyError:

                # TODO: Why do we try this?
                try:
                    token = request.defer_post['token']
                except:
                    raise Http404

            # Get the return to address and maybe the background.
            try:
                return_to = request.session[token]['return_to']
                if use_background:
                    background = request.session[token]['background']
            except:
                raise Http404

            # Have any of the cancel triggers been used? If so, return to
            # the deferred view without returning an updated POST.
            if request.method == 'POST':
                for tag in cancel_tags:
                    if tag in request.POST:
                        return resume_deferred(request)

            # Put the defer token and return to address on the request for use
            # in the "resume_deferred" function.
            request.defer_token = token
            request.defer_return_to = return_to

            # Render the response.
            response = view(request, *args, **kwargs)

            # If we have been instructed to use the background, do so now.
            if use_background:

                # Render the foreground.
                foreground = u'''<div style="display:block;position:fixed;top:0px;left:0px;width:100%%;height:100%%;z-index:10000;background-color:rgba(0,0,0,0.7);">
  <div style="position:absolute;left:25%%;top:25%%;width:50%%;height:50%%;z-index:10001;background-color:#FFF;">%s</div>
</div>
'''%response.content

                # To combine the background and foreground, we need to hunt down the end
                # of the body tag of the background and insert the foreground into it.
                idx = background.rfind('</body>')
                response.content = background[:idx] + foreground + background[idx + len('</body>'):]

            return response

        return called_view
    return called_inner


## Return to a previously deferred view.
#
#  This is here to ease the procedure of safely returning to a previously
#  deferred view. It checks for validity and automatically determines
#  the path of the prior view.
#
#  @param[in]  request  The current view's request.
#  @param[in]  kwargs   A dictionary used to return values to the deferred view.
#  @returns    A redirect response object.
def resume_deferred(request, **kwargs):

    # Must be able to get the token, data and return url.
    try:
        token = request.REQUEST['token']
        data = dict(request.session[token])
        return_to = data['return_to']
    except KeyError:

        # TODO: What's all this? ... Try the 'defer_post' option on request.
        # request.defer_post
        raise Http404

    # Update the post data.
    for name, value in kwargs.iteritems():
        data['post'][name] = value

    # Reset data and return.
    request.session[token] = data
    return redirect(return_to + '?retoken=%s'%token)
