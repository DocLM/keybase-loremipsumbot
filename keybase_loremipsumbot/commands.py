
lorem_ipsum_command = "lorem ipsum"
lorem_extended = f"""Send [n_messages] lorem ipsum phrases [after] a given time and with [delay] between messages.
Examples:
```!{lorem_ipsum_command} [n_messages] [after(ms)] [delay(ms)]```
"""

advertised_commands = {
    "method": "advertisecommands",
    "params": {
        "options": {
            "alias": "Lorem Ipsum Bot",
            "advertisements": [
                {
                    "type": "public",
                    "commands": [
                        {
                            "name": lorem_ipsum_command,
                            "description": "Send a lorem ipsum phrase.",
                            "extended_description": {
                                "title": f"*!{lorem_ipsum_command}*",
                                "desktop_body": lorem_extended,
                                "mobile_body": lorem_extended,
                            },
                        }
                    ],
                }
            ],
        }
    },
}
