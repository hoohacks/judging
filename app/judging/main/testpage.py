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
        }, {
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
        }, {
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
        }, {
            "name": "Team",
            "forms": [
                {
                    "name": "api:team_create",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "name",
                            "type": "text",
                            "required": True
                        },
                        {
                            "name": "link",
                            "type": "text",
                            "required": True
                        },
                        {
                            "name": "table",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "members",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "is_anchor",
                            "type": "checkbox",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:team_search",
                    "method": "GET",
                    "fields": [
                        {
                            "name": "team_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "link",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "table",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "members",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "is_anchor",
                            "type": "checkbox",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:team_update",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "team_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "link",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "table",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "members",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "is_anchor",
                            "type": "checkbox",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:team_delete",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "team_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                }
            ]
        }, {
            "name": "Category",
            "forms": [
                {
                    "name": "api:category_create",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "name",
                            "type": "text",
                            "required": True
                        },
                        {
                            "name": "description",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "organization_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "number_winners",
                            "type": "number",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:category_search",
                    "method": "GET",
                    "fields": [
                        {
                            "name": "category_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "description",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "organization_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "number_winners",
                            "type": "number",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:category_update",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "category_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "description",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "organization_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "number_winners",
                            "type": "number",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:category_add_team",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "category_id",
                            "type": "number",
                            "required": True
                        }, {
                            "name": "team_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                },
                {
                    "name": "api:category_remove_team",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "category_id",
                            "type": "number",
                            "required": True
                        }, {
                            "name": "team_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                },
                {
                    "name": "api:category_delete",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "category_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                }
            ]
        }, {
            "name": "Criteria",
            "forms": [
                {
                    "name": "api:criteria_create",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "name",
                            "type": "text",
                            "required": True
                        },
                        {
                            "name": "description",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "min_score",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "max_score",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "weight",
                            "type": "str",
                            "required": False
                        },
                    ]
                },
                {
                    "name": "api:criteria_search",
                    "method": "GET",
                    "fields": [
                        {
                            "name": "criteria_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "description",
                            "type": "text",
                            "required": False
                        },
                    ]
                },
                {
                    "name": "api:criteria_update",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "criteria_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "name",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "description",
                            "type": "text",
                            "required": False
                        },
                        {
                            "name": "min_score",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "max_score",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "weight",
                            "type": "str",
                            "required": False
                        },
                    ]
                },
                {
                    "name": "api:criteria_delete",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "criteria_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                }
            ]
        }, {
            "name": "CriteriaLabel",
            "forms": [
                {
                    "name": "api:criteria_label_create",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "criteria_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "score",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "label",
                            "type": "text",
                            "required": True
                        }
                    ]
                },
                {
                    "name": "api:criteria_label_search",
                    "method": "GET",
                    "fields": [
                        {
                            "name": "criteria_label_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "criteria_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "score",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "label",
                            "type": "text",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:criteria_label_update",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "criteria_label_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "criteria_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "score",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "label",
                            "type": "text",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:criteria_label_delete",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "criteria_label_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                }
            ]
        }, {
            "name": "Demo",
            "forms": [
                {
                    "name": "api:demo_create",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "judge_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "team_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                },
                {
                    "name": "api:demo_search",
                    "method": "GET",
                    "fields": [
                        {
                            "name": "demo_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "judge_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "team_id",
                            "type": "number",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:demo_update",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "demo_id",
                            "type": "number",
                            "required": True
                        },
                        {
                            "name": "judge_id",
                            "type": "number",
                            "required": False
                        },
                        {
                            "name": "team_id",
                            "type": "number",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "api:demo_delete",
                    "method": "POST",
                    "fields": [
                        {
                            "name": "demo_id",
                            "type": "number",
                            "required": True
                        }
                    ]
                }
            ]
        }
    ]
}
