context = {
    "forms": [
        {
            "name": "api:user_create",
            "method": "POST",
            "fields": [
                {
                    "name": "first_name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "last_name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "username",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "password",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "organization_id",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "is_staff",
                    "type": "checkbox",
                    "required": False
                }
            ]
        },
        {
            "name": "api:user_search",
            "method": "GET",
            "fields": [
                {
                    "name": "user_id",
                    "type": "number",
                    "required": False
                },
                {
                    "name": "username",
                    "type": "text",
                    "required": False
                },
                {
                    "name": "organization_id",
                    "type": "number",
                    "required": False
                },
                {
                    "name": "is_staff",
                    "type": "checkbox",
                    "required": False
                }
            ]
        },
        {
            "name": "api:user_update",
            "method": "POST",
            "fields": [
                {
                    "name": "user_id",
                    "type": "number",
                    "required": True
                },
                {
                    "name": "username",
                    "type": "text",
                    "required": False
                },
                {
                    "name": "organization_id",
                    "type": "number",
                    "required": False
                },
                {
                    "name": "is_staff",
                    "type": "checkbox",
                    "required": False
                }
            ]
        },
        {
            "name": "api:user_delete",
            "method": "POST",
            "fields": [
                {
                    "name": "user_id",
                    "type": "number",
                    "required": True
                }
            ]
        }
    ]
}