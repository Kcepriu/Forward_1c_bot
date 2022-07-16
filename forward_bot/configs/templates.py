TEMPLATE_INFORMATION = ''' 
{% macro contact_information(information) -%}

{% for inf in information -%}
<strong>   {{inf.type}}:</strong>{{inf.contact}}
{% endfor %}

{%- endmacro %}
<strong>Назва:</strong> {{message.name}}
<strong>Повна назва:</strong> {{message.full_name}}
<strong>Менеджер контрагента:</strong> {{message.manager}}
<strong>Контактна інформація:</strong>
{{ contact_information(message.contacts) }}

<strong>Контакні особи:</strong>
{% for contact_person in message.contact_persons -%}
<strong>{{contact_person['name']}}:</strong> {{contact_person['post']}}
<strong>Контактна інформація:</strong>
   {{ contact_information(contact_person['contacts']) }}
{% endfor %}'''

TEMPLATE_EVENTS = ''' 
<strong>Дата:</strong> {{message.date}}
<strong>Менеджер контрагента:</strong> {{message.manager}}
<strong>Контакна особа:</strong> {{message.contact_name}}
<strong>Текст події:</strong>
{{message.text_event}}
'''

TEMPLATE_DIFFERENCE = ''' 
{% for inf in message -%}
<strong>   {{inf.name_prop}}:</strong>
<strong>В QR:</strong> {{inf.old_value}}
<strong>В 1с:</strong> {{inf.new_value}}
{% endfor %}
'''
