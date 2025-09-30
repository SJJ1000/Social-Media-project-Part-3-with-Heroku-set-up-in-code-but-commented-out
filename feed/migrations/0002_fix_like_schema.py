from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


def forwards_copy_username_to_user(apps, schema_editor):
    Like = apps.get_model('feed', 'Like')
    
    for like in Like.objects.all():
        
        if getattr(like, 'user_id', None) is None and getattr(like, 'username_id', None) is not None:
            like.user_id = like.username_id
            like.save(update_fields=['user'])


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(
                related_name='post_likes',
                null=True,  # temporarily nullable
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        
        migrations.AddField(
            model_name='like',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        
        migrations.RunPython(forwards_copy_username_to_user, migrations.RunPython.noop),
        
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(
                related_name='post_likes',
                null=False,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('post', 'user')},
        ),
        
        migrations.RemoveField(
            model_name='like',
            name='username',
        ),
    ]
