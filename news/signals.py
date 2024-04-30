from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from .models import Post, Category, Subscription
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import truncatewords_html
from django.db.models.signals import post_save



@receiver(post_save, sender=Post)
def send_notification_on_post_create(sender, instance, created, **kwargs):
    """
    Отправка уведомления при создании новой статьи
    """
    if created:
        from .tasks import send_notification  # Импорт здесь, чтобы избежать циклической зависимости
        send_notification.delay(instance.id)



#@receiver(m2m_changed, sender=Post.postCategory.through)
#def post_created(sender, instance, action, pk_set, **kwargs):
 #   print('*******************************')
  #  print(f'post_created called with action: {action}')
   # print('*******************************')
    #if action == 'post_add':

    #    categorys = Category.objects.filter(pk__in=pk_set)
     #   for category in categorys:
      #      subscriptions = Subscription.objects.filter(category=category)
       #     for subscription in subscriptions:
        #        send_subscription_email(subscription.user, instance)
#


#def send_subscription_email(user, post):

 #   subject = f'Новый пост в категории {post.postCategory.first().name}'
  #  truncated_content = truncatewords_html(post.text, 10,)
   # text_content = (
    #    f'Здравствуйте, {user.username}!\n\n'
     #   f'Вы подписаны на категорию {post.postCategory.first().name}, и там появилась новая публикация:\n'
      #  f'Название: {post.title}\n'
       # f'Краткое описание: {truncated_content}\n\n'
        #f'Читать полностью: http://127.0.0.1:8000{post.get_absolute_url()}'
    #)

    #html_content = (
     #   f'<h4>Здравствуйте, {user.username}!</h4>'
      #  f'<p>Вы подписаны на категорию {post.postCategory.first().name}, и там появилась новая публикация:</p>'
       # f'<p>Название: {post.title}</p>'
        #f'<p>Краткое описание: {truncated_content}</p>'
        #f'<p><a href="http://127.0.0.1:8000{post.get_absolute_url()}">Читать полностью</a></p>'
    #)

  #  msg = EmailMultiAlternatives(
 #       subject,
 #       text_content,
 #       settings.EMAIL_HOST_USER,
 #       [user.email]
 #   )

  #  msg.attach_alternative(html_content, "text/html")
 #   msg.send()

