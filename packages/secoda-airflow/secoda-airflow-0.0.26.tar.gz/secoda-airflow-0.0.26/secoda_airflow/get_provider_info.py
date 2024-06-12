def get_provider_info():
    return {
        "name": "Secoda",
        "description": "`Secoda <https://www.secoda.com/>`__\n",
        "integrations": [
            {
                "integration-name": "Secoda",
                "external-doc-url": "https://www.secoda.com/",
                "tags": ["service"],
            }
        ],
        "connection-types": [
            {
                "hook-class-name": "secoda_airflow.hooks.SecodaHook",
                "connection-type": "secoda",
                "connection-name": "Secoda Connection",
                "connection-fields": [
                    {
                        "label": "Host",
                        "key": "host",
                        "type": "string",
                        "description": "Host for the Secoda service",
                    },
                    {
                        "label": "API Key",
                        "key": "api_key",
                        "type": "password",
                        "description": "API key for the Secoda service",
                    },
                    {
                        "label": "Integration ID",
                        "key": "extra__integration_id",
                        "type": "string",
                        "description": "Integration ID for the Secoda service",
                    },
                ],
            }
        ],
        "hooks": [
            {
                "integration-name": "Secoda",
                "python-modules": ["secoda_airflow.hooks"],
            }
        ],
        "package-name": "secoda-airflow",
    }
