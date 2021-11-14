TEMPLATE_INFORMATION = ''' 
    {% macro contact_information(information) -%}
        <br><big><span style="font-weight: bold;">Контактна інформація</span>:</big>
        {% for inf in information -%}
            <br>&nbsp;&nbsp; <span style="font-weight: bold;">{{inf.type}}:</span>{{inf.contact}}
        {% endfor %}
        <br>
    {%- endmacro %}
    <html>
    <head>
        <meta content="text/html; charset=utf-8"
        http-equiv="content-type">
        <title></title>
    </head>
    <body>
        <big><span style="font-weight: bold;">Назва:</span></big> {{message.name}}
        <br><big><span style="font-weight: bold;">Повна назва:</span></big> {{message.full_name}}
        <br><big><span style="font-weight: bold;">Менеджер контрагента:</span></big> {{message.manager}}
        {{ contact_information(message.contacts) }}

        <br>&nbsp;&nbsp; <big><span style="font-weight: bold;">Контакні особи:</span></big>
        {% for contact_person in message.contact_persons -%}
            <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span style="font-weight: bold;">{{contact_person['name']}}:</span> {{contact_person['post']}}
            {{ contact_information(contact_person['contacts']) }}
        {% endfor %}
    </body>
    </html>'''