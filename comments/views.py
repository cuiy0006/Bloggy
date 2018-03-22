from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from users.models import User
from comments.models import Comment
from comments.forms import CommentForm, CommentExtensionForm
from django.http import HttpResponseRedirect

# Create your views here.
def post_comment(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    postId = request.POST['postId']
    post = get_object_or_404(Post, pk=postId)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            commenterId = request.user.pk
            commenter = get_object_or_404(User, pk=commenterId)
            comment.post = post
            comment.commenter = commenter
            comment.save()

            underId = request.POST['underId']
            replyToId = request.POST['replyToId']
            comment_ext_form = CommentExtensionForm(request.POST)
            if underId != '' and comment_ext_form.is_valid():
                comment_ext = comment_ext_form.save(commit=False)
                comment_ext.comment = comment

                under = get_object_or_404(Comment, pk=underId)
                replyTo = get_object_or_404(Comment, pk=replyToId)
                comment_ext.under = under
                comment_ext.replyTo = replyTo
                comment_ext.save()
    return redirect(post)

