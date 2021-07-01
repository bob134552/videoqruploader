import os

from django.db import models
from django.dispatch import receiver
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import qrcode


class Videos(models.Model):
    class Meta:
        ordering = ('-order_number',)
        verbose_name_plural = 'Videos'

    video = models.FileField(upload_to='videos/', null=True, blank=True)
    order_number = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    keyword = models.CharField(max_length=20, null=False, blank=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return str(self.order_number)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.order_number)
        canvas = Image.new('RGB', (300, 300), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.order_number}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

@receiver(models.signals.post_delete, sender=Videos)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes files from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.qr_code:
        if os.path.isfile(instance.qr_code.path):
            os.remove(instance.qr_code.path)
    
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)
