context = {
    "sections": [
        {
            "name": "User",
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
                },
            ]
        },
        {
            "name": "Organization",
            "forms": [
                {
                    "name": "api:organization_create",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "name",
                            "type": "text",
                            "required": True
                        },
                    ]
                },
                {
                    "name": "api:organization_search",
                    "method": "GET",
                    "fields": [
                        {
                            "name": "organization_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:organization_update",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "organization_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:organization_delete",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "organization_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                }
            ]
        },
        {
            "name": "Event",
            "forms": [
                {
                    "name": "api:event_create",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "name",
                            "type": "text",
                            "required": True
                        },
                    ]
                },
                {
                    "name": "api:event_search",
                    "method": "GET",
                    "fields": [
                        {
                            "name": "event_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:event_update",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "event_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:event_delete",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "event_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                }
            ]
        }
    ]
}
