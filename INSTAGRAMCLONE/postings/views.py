from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import transaction
from .models import Posting, Comment, HashTag
from .forms import PostingForm, ImageForm, CommentForm, ImageFormset


@require_GET
def posting_list(request):
    postings = Posting.objects.all()
    return render(request, 'postings/posting_list.html', {
        'postings': postings,
    })


@require_GET
def posting_detail(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    user = request.user
    comment_form = CommentForm()
    is_like = posting.like_users.filter(id=request.user.id).exists()
    return render(request, 'postings/posting_detail.html', {
        'posting': posting,
        'user': user,
        'comment_form': comment_form,
        'is_like': is_like,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def create_posting(request):
    if request.method == 'POST':
        posting_form = PostingForm(request.POST)
        image_form = ImageFormset(request.POST, request.FILES)
        if posting_form.is_valid() and image_form.is_valid():
            posting = posting_form.save(commit=False)
            posting.author = request.user

            with transaction.atomic():
                posting.save()
                image_form.instance = posting
                image_form.save()

            # 띄어쓰기를 기준으로 split
            words = posting.contents.split()
            for word in words:
                if word[0] == '#':
                    # get_or_create는 list를 return
                    tag = HashTag.objects.get_or_create(content=word)
                    posting.hashtags.add(tag[0])

            return redirect(posting)
    else:
        posting_form = PostingForm()
        image_form = ImageFormset()
    return render(request, 'postings/posting_form.html', {
        'posting_form': posting_form,
        'image_form': image_form,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def update_posting(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    if posting.author == request.user:
        if request.method == 'POST':
            form = PostingForm(request.POST, instance=posting)
            if form.is_valid():
                posting = form.save()
                return redirect(posting)
        else:
            form = PostingForm(instance=posting)
    else:
        return redirect(posting)
    return render(request, 'postings/posting_form.html', {
        'posting_form': form,
    })


@login_required
@require_POST
def delete_posting(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    if posting.author == request.user:
        posting.delete()
    else:
        return redirect(posting)
    return redirect('postings:posting_list')


@login_required
@require_POST
def create_comment(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.posting = posting
        comment.save()
    return redirect(posting)


@login_required
@require_POST
def delete_comment(request, posting_id, comment_id):
    posting = get_object_or_404(Posting, id=posting_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('posting_detail', id=posting.id)


@login_required
def toggle_like(request, posting_id):
    if request.is_ajax:
        posting = get_object_or_404(Posting, id=posting_id)
        user = request.user
        if posting.like_users.filter(id=user.id).exists():
            posting.like_users.remove(user)
            liked = False
        else:
            posting.like_users.add(user)
            liked = True
        like_count = posting.like_users.count()

        context = {
            'posting_id': posting.id,
            'user_id': user.id,
            'liked': liked,
            'like_count': like_count,
        }
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()


