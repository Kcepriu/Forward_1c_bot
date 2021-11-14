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