from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives


try:
    from herbs.models import Notification
except ImportError:
    from bgi.herbs.models import Notification

class Command(BaseCommand):
    args = ''
    help = 'Send notification messages'

    def handle(self, *args, **options):
        query = '''
        SELECT DISTINCT herbs_notification.herbitem_id 
        FROM herbs_notification INNER JOIN herbs_herbitem
        ON herbs_notification.herbitem_id = herbs_herbitem.id;
        WHERE status='Q'
        ORDER BY `created` DESC;
        '''
        cursor = connection.cursor()
        cursor.execute(query)

        messages = dict()
        for obj_id in cursor.fetchall():
            for item in Notification.objects.filter(id=obj_id):
                if item.emails:
                    for email in item.emails.split(','):
                        if email not in messages:
                            messages.update({email: []})
                        messages[email].append({
                            'id': obj_id,
                            'date': str(item.created),
                            'username': item.username
                        })
                        reason = '%s : %s'.format(item.field_name, item.field_value)
                        if 'reason' not in messages[email][-1]:
                            messages[email][-1].update({'reson': [reason]})
                        else:
                            messages[email][-1]['reason'].append(reason)

                        if 'note_ids' not in messages[email][-1]:
                            messages[email][-1].update({'note_ids': [item.id]})
                        else:
                            messages[email][-1]['note_ids'].append(item.id)

        for email in messages:
            html = self._generate_html_message(messages[email])
            try:
                mail_msg = EmailMultiAlternatives(u'Оповещение гербария от %s' % timezone.now(),
                                        '', 'herbarium@botsad.ru',
                                        [email], connection=get_connection(fail_silently=False))
                mail_msg.attach_alternative(html, 'text/html')
                mail_msg.send()
                Notification.objects.filter(id__in=messages[email]['note_ids']).update(status='S')
            except:
                pass

    @staticmethod
    def _generate_html_message(msg):
        html_email_temaple = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Demystifying Email Design</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="margin: 0; padding: 0;">
 <table align="center" border="1" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
  
  <tr>
   <td bgcolor="#ffffff" style="padding: 10px 10px 10px 10px;">
    <h2> Сводка по изменениям в гербарии от {{created}} </h2>
   </td>
  </tr>

  <tr>
      <td bgcolor="#ffffff" style="padding: 40px 40px 40px 40px;">
         <table border="1" cellpadding="0" cellspacing="0" width="100%">
          <tr>
           <td align="center">ID</td>
           <td align="center">USERNAME</td>
           <td align="center">DATE</td>
           <td align="center">REASON</td>
           <td align="center">LINK</td>
          </tr>
          
          {%for item in items %}
            {% if forloop.counter|divisibleby:2 %}
                <tr>
                   <td align="center">ID</td>
                   <td align="center">USERNAME</td>
                   <td align="center">DATE</td>
                   <td align="center">REASON</td>
                   <td align="center">LINK</td>
                </tr>
            {%else%}
                <tr>
                   <td align="center">ID</td>
                   <td align="center">USERNAME</td>
                   <td align="center">DATE</td>
                   <td align="center">REASON</td>
                   <td align="center">LINK</td>
                </tr>
            {%endif%}
          {%endfor%}
          
         </table>
      </td>
  </tr>
  
 </table>
</body>


</html>
        
        
        
        
                <html>
                  
                    <table width="600" style="border:1px solid #333">
                  <tr>
                   
                  </tr>
                  
                  <tr>
                    <td align="center">
                      body 
                      <table align="center" width="300" border="0" cellspacing="0" cellpadding="0" style="border:1px solid #ccc;">
                        <tr>
                          <td> data </td>
                          <td> info </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
                </html>
        '''















