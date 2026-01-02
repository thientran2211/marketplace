from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item
from .models import Conversation
from .forms import MessageForm

# Create your views here.


@login_required
def new_conversation(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if item.created_by == request.user:
        return redirect('dashboard:index')

    conversation = Conversation.objects.filter(
        item=item, members__in=[request.user.id])

    if conversation:
        return redirect('conversation:detail', conversation_id=conversation.first().id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()
            return redirect('item:item_detail', item_id=item.id)
    else:
        form = MessageForm()

    return render(request, 'conversation/new.html', {
        'form': form,
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })


@login_required
def detail(request, conversation_id):
    conversation = Conversation.objects.filter(
        members__in=[request.user.id]).get(id=conversation_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()
            return redirect('conversation:detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
    })
