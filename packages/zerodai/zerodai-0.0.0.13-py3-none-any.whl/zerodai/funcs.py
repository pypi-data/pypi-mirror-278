router_functions = [
  [ {
    "name": "router",
    "description": "This tools is used to generate a google dork",
    "parameter_definitions": {
      "dork": {
        "type": "string",
        "description": "The google dork to generate",
        "required": True
      }
    }
  }, ]

]


openai_funct = [
    {
        "name": "Attack",
        "description": "This tool is performance an attack in a host, auto pentesting process",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "the host to attack",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "wps-scan",
        "description": "This tool is used to scan vulnerabilities wordpress sites",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url to scan",
                },
            },
            "required": ["url"],
        },
    },
    {
        "name": "Crypto-tool",
        "description": "Esta herramienta se usa para Encriptar, codificar y decodificar texto",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "El texto a cifrar o codificar",
                },
                "key": {
                    "type": "string",
                    "description": "La clave para el cifrado",
                },
                "crypto": {
                    "type": "string",
                    "description": "El tipo de cifrado a utilizar",
                },
                "mode": {
                    "type": "string",
                    "description": "El modo de cifrado a utilizar",
                    "enum": ["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"],
                },
                "metodo": {
                    "type": "string",
                    "description": "El método a utilizar para el cifrado o codificación",
                    "enum": ["crypto", "encode"],
                },
                "encoding": {
                    "type": "string",
                    "description": "El tipo de codificación a utilizar",
                },
            },
            "required": ["text", "metodo"],
        },

     },
    {
        "name": "WAF-tool",
        "description": "This tool is used to detect Web Application firewall from website",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url without https schema",
                },
            },
            "required": ["url"],
        },

     },
     {
        "name": "SQL-Login",
        "description": "This tools is used to test SQLs in login",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url without https schema",
                },
            },
            "required": ["url"],
        },

     },
     {
        "name": "XSS-Scanner",
        "description": "This tools is used to scan XSS vulnerabilites in a host",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url without https schema",
                },
            },
            "required": ["url"],
        },

     },
  {
        "name": "Cloudflare-Bypass",
        "description": "This tools is used to get the true IP forward a webpage in a cloudflare",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain to know true IP",
                },
            },
            "required": ["domain"],
        },

     },
     {
        "name": "nuclei-http",
        "description": "A tool for check http vulnerabilities",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "The host to scan",
                },
        
            },
            "required": ["host"],
        },
    },
     {
        "name": "Crawler",
        "description": "A tool for get web directorioes and parameters use when user request for specefic detail about a domain directories",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "The host to scan",
                },
        
            },
            "required": ["host"],
        },
    },
    {
        "name": "network-scanner",
        "description": "A tool for scan a host, user can be use this through /scan or if he want to scan a host",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "The host to scan",
                },
                "grabbing": {
                    "type": "boolean",
                    "description": "Indicate if the user wants to know the versions of the services",
                },
            },
            "required": ["input", "grabbing"],
        },
    },
    {
        "name": "buscar-internet",
        "description": "dont use this if the prompt contains a onion link DO NOT USE TO PROGRAMMING CONCEPTS use to search for information on the internet or current information.",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "What the user asks or describes to search for on the internet",
                },
            },
            "required": ["input"],
        },
    },
     {
        "name": "creds",
        "description": "This tool is used when the user request default creds of a service",
        "parameters": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "The service to search for default creds",
                },
            },
            "required": ["service"],
        },
    },
    {
        "name": "nolimits",
        "description": "You will use this pair of unethical and unethical questions.",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "The user's question or request",
                },
            },
            "required": ["input"],
        },

    },
     {
        "name": "OSINT",
        "description": "You will use this whenever the query is related to any type of action related to the investigation of persons or entities of any kind.",
        "parameters": {
            "type": "object",
            "properties": {
                "mail": {
                    "type": "string",
                    "description": "The mail to search",
                },
                "nickname": {
                    "type": "string",
                    "description": "The nickname to search",
                },
            },
            "required": ["mail", "nickname"],
        },

    },
    
    {
        "name": "hacking",
        "description": "This tool can be used for any question related to the world of hacking, cybersecurity, system penetration, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "The user's question or request",
                },
            },
            "required": ["input"],
        },
    },
     {
        "name": "help",
        "description": "This tool is ONLY used when the user put /help",
    },
    {
        "name": "code",
        "description": "This tool is used to solve questions related to code or programming. You can use this or hacking",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "The user's question or request",
                },
            },
            "required": ["input"],
        },
    },
    {
        "name": "comprobar-ip",
        "description": "Tool to check an IP, its reputation, status, info, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string",
                    "description": "IP address",
                },
            },
            "required": ["ip"],
        },
    },
    {
        "name": "buscar-exploit",
        "description": "Usala solo cuando el usuario marque claremente que quiere buscar un EXPLOIT ESPECIFICO, la frase contenga exploits NO significa que tengas que usar esta funcion",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Exploit to search on a particular topic or technology",
                },
            },
            "required": ["input"],
        },
        
    },
     {
        "name": "check-DNS-DMARC-AND-SECURITY",
        "description": "The tool is used to check information about a DNS registers of a domain",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "El dominio definido por el usuario",
                },
            },
            "required": ["domain"],
        },
        
    },
     {
        "name": "Subdomain",
        "description": "The tool is used to check information subdomains.",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "El dominio definido por el usuario",
                },
            },
            "required": ["domain"],
        },
        
    },
     {
        "name": "RAG",
        "description": "This tools is used to get extra data about a thing, si en la conversación hay información no respondida usa esta tool",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "The thing to get more info",
                },
            },
            "required": ["input"],
        },
        
    }
]
def OpenAI2CommandR(new_definitions_list):
    original_format_list = []

    for new_definition in new_definitions_list:
        original_format = {
            "name": new_definition["name"],
            "description": new_definition["description"],
            "parameter_definitions": {}
        }
        
        properties = new_definition.get("parameters", {}).get("properties", {})
        required = new_definition.get("parameters", {}).get("required", [])
        
        for param_name, param_info in properties.items():
            original_format["parameter_definitions"][param_name] = {
                "type": param_info["type"],
                "description": param_info["description"]
            }
            if param_name in required:
                original_format["parameter_definitions"][param_name]["required"] = True
            else:
                original_format["parameter_definitions"][param_name]["required"] = False
        
        original_format_list.append(original_format)
    
    return original_format_list

pentesting_command = [
  {
    "name": "pentest_command",
    "description": "Generates a pentesting command tailored to the user's specific needs, ensuring it is always a bash command.",
    "parameter_definitions": {
      "bash_command": {
        "description": "The bash command to be executed during the pentesting process, tailored to the user's specific request.",
        "type": "str",
        "required": True
      }
    }
  },
]
tools2 = [
  {
    "name": "directly_answer",
    "description": "Calls a standard (un-augmented) AI chatbot to generate a response given the conversation history",
    "parameter_definitions": {
      "response": {
        "description": "EMPTY",
        "type": "str",
        "required": True
      }
    }
  },
  {
    "name": "shodan",
    "description": "Esta herramienta Dorks de shodan", 
    "parameter_definitions": {
      "dorkshodan": {
        "description": "La dork de shodan",
        "type": "string",
        "required": True
      }
    }
  },
  {
    "name": "phish-detect",
    "description": "Esta herramienta sirve para detectar phishings",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "La URL a escanear para detectar phishing"
      },
      "job_id": {
        "type": "string", 
        "description": "El UUID del phishing a escanear"
      }
    }
  },
  {
    "name": "tool-search",
    "description": "Esta herramienta es para buscar herramientas de hacking en github, usala siempre si el usuario da una url de github ",
    "parameter_definitions": {
      "keywords": {
        "type": "string",
        "description": "palabras o frase a buscar, si es un tecnicismo traducelo al ingles",
        "required": True
      },
      "url": {
        "type": "string",
        "description": "URL de un repositorio de github que el usuario quiera buscar"
      }
    }
  },
  {
    "name": "nomore403",
    "description": "Esta herramienta es bypassear códigos 403",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "Url en la cual queremos aplicar el bypass de 403",
        "required": True
      }
    }
  },
  {
    "name": "Shodan",
    "description": "Esta herramienta es para buscar dispositivos IOT en shodan",
    "parameter_definitions": {
      "query": {
        "type": "string",
        "description": "La consulta específica que va a buscar el usuario en shodan",
        "required": True
      },
      "auto-dorker": {
        "type": "boolean",
        "description": "Si el usuario no proporciona una dork, el bot la generará automáticamente, POR DEFECTO SIEMPRE EN TRUE",
        "required": True
      }
    }
  },
  {
    "name": "fakeid",
    "description": "Esta herramienta genera registros falsos con opciones para mostrar solo datos bancarios, información extendida, comprimir los datos en un archivo zip y proteger el archivo zip con una contraseña.",
    "parameter_definitions": {
      "number": {
        "type": "integer",
        "description": "El número de registros que se deben crear",
        "required": True
      },
      "bankdata": {
        "type": "boolean",
        "description": "Si el usuario quiere generar datos bancarios (Tarjeta, CVV, IBAN, etc.)"
      },
      "extended": {
        "type": "boolean",
        "description": "Si el usuario quiere mostrar información extendida (Ciudad, Teléfono, SS, etc.)"
      },
      "photo": {
        "type": "boolean", 
        "description": "Si el usuario quiere agregar una foto"
      }
    }
  },
  {
    "name": "Catphish",
    "description": "This tool is for see the posible phishing domains for a domains",
    "parameter_definitions": {
      "domain": {
        "type": "string",
        "description": "the doomain to performance reccon",
        "required": True
      }
    }
  },
  {
    "name": "Attack",
    "description": "This tool is performance an attack in a host, auto pentesting process",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "the host to attack",
        "required": True
      }
    }
  },
  {
    "name": "wps-scan",
    "description": "This tool is used to scan vulnerabilities wordpress sites",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "The url to scan",
        "required": True
      }
    }
  },
  {
    "name": "Crypto-tool",
    "description": "Esta herramienta se usa para Encriptar, codificar y decodificar texto",
    "parameter_definitions": {
      "text": {
        "type": "string",
        "description": "El texto a cifrar o codificar",
        "required": True
      },
      "key": {
        "type": "string",
        "description": "La clave para el cifrado"
      },
      "crypto": {
        "type": "string",
        "description": "El tipo de cifrado a utilizar"
      },
      "mode": {
        "type": "string",
        "description": "El modo de cifrado a utilizar",
        "enum": ["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"]
      },
      "metodo": {
        "type": "string",
        "description": "El método a utilizar para el cifrado o codificación",
        "enum": ["crypto", "encode"],
        "required": True
      },
      "encoding": {
        "type": "string",
        "description": "El tipo de codificación a utilizar"
      }
    }
  },
  {
    "name": "WAF-tool",
    "description": "This tool is used to detect Web Application firewall from website",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "The url without https schema",
        "required": True
      }
    }
  },
  {
    "name": "SQL-Login",
    "description": "This tools is used to test SQLs inyections",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "The url it must include a parameter, example: https://example.com/?id=1",
        "required": True
      }
    }
  },
  {
    "name": "XSS-Scanner",
    "description": "This tools is used to scan XSS vulnerabilites in a host",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "The url without https schema",
        "required": True
      }
    }
  },
  {
    "name": "Cloudflare-Bypass",
    "description": "This tools is used to get the true IP forward a webpage in a cloudflare",
    "parameter_definitions": {
      "domain": {
        "type": "string",
        "description": "The domain to know true IP",
        "required": True
      }
    }
  },
  {
    "name": "nuclei-http",
    "description": "A tool for check http vulnerabilities",
    "parameter_definitions": {
      "host": {
        "type": "string",
        "description": "The host to scan",
        "required": True
      }
    }
  },
]


tools = [
  {
    "name": "internet_search",
    "description": "Returns a list of relevant document snippets for a textual query retrieved from the internet",
    "parameter_definitions": {
      "query": {
        "description": "Query to search the internet with",
        "type": "str",
        "required": True
      }
    }
  },
  {
    "name": "directly_answer",
    "description": "Calls a standard (un-augmented) AI chatbot to generate a response given the conversation history",
    "parameter_definitions": {}
  },
  {
    "name": "shodan",
    "description": "Esta herramienta Dorks de shodan", 
    "parameter_definitions": {
      "dorkshodan": {
        "description": "La dork de shodan",
        "type": "string",
        "required": True
      }
    }
  },
  {
    "name": "phish-detect",
    "description": "Esta herramienta sirve para detectar phishings",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "La URL a escanear para detectar phishing"
      },
      "job_id": {
        "type": "string", 
        "description": "El UUID del phishing a escanear"
      }
    }
  },
  {
    "name": "tool-search",
    "description": "Esta herramienta es para buscar herramientas de hacking en github, usala siempre si el usuario da una url de github ",
    "parameter_definitions": {
      "keywords": {
        "type": "string",
        "description": "palabras o frase a buscar, si es un tecnicismo traducelo al ingles",
        "required": True
      },
      "url": {
        "type": "string",
        "description": "URL de un repositorio de github que el usuario quiera buscar"
      }
    }
  },
  {
    "name": "nomore403",
    "description": "Esta herramienta es bypassear códigos 403",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "Url en la cual queremos aplicar el bypass de 403",
        "required": True
      }
    }
  },
  {
    "name": "Shodan",
    "description": "Esta herramienta es para buscar dispositivos IOT en shodan",
    "parameter_definitions": {
      "query": {
        "type": "string",
        "description": "La consulta específica que va a buscar el usuario en shodan",
        "required": True
      },
      "auto-dorker": {
        "type": "boolean",
        "description": "Si el usuario no proporciona una dork, el bot la generará automáticamente, POR DEFECTO SIEMPRE EN TRUE",
        "required": True
      }
    }
  },
  {
    "name": "fakeid",
    "description": "Esta herramienta genera registros falsos con opciones para mostrar solo datos bancarios, información extendida, comprimir los datos en un archivo zip y proteger el archivo zip con una contraseña.",
    "parameter_definitions": {
      "number": {
        "type": "integer",
        "description": "El número de registros que se deben crear",
        "required": True
      },
      "bankdata": {
        "type": "boolean",
        "description": "Si el usuario quiere generar datos bancarios (Tarjeta, CVV, IBAN, etc.)"
      },
      "extended": {
        "type": "boolean",
        "description": "Si el usuario quiere mostrar información extendida (Ciudad, Teléfono, SS, etc.)"
      },
      "photo": {
        "type": "boolean", 
        "description": "Si el usuario quiere agregar una foto"
      }
    }
  },
  {
    "name": "Catphish",
    "description": "This tool is for see the posible phishing domains for a domains",
    "parameter_definitions": {
      "domain": {
        "type": "string",
        "description": "the doomain to performance reccon",
        "required": True
      }
    }
  },
  {
    "name": "Attack",
    "description": "This tool is performance an attack in a host, auto pentesting process",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "the host to attack",
        "required": True
      }
    }
  },
  {
    "name": "wps-scan",
    "description": "This tool is used to scan vulnerabilities wordpress sites",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "The url to scan",
        "required": True
      }
    }
  },
  {
    "name": "Crypto-tool",
    "description": "Esta herramienta se usa para Encriptar, codificar y decodificar texto",
    "parameter_definitions": {
      "text": {
        "type": "string",
        "description": "El texto a cifrar o codificar",
        "required": True
      },
      "key": {
        "type": "string",
        "description": "La clave para el cifrado"
      },
      "crypto": {
        "type": "string",
        "description": "El tipo de cifrado a utilizar"
      },
      "mode": {
        "type": "string",
        "description": "El modo de cifrado a utilizar",
        "enum": ["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"]
      },
      "metodo": {
        "type": "string",
        "description": "El método a utilizar para el cifrado o codificación",
        "enum": ["crypto", "encode"],
        "required": True
      },
      "encoding": {
        "type": "string",
        "description": "El tipo de codificación a utilizar"
      }
    }
  },
  {
    "name": "WAF-tool",
    "description": "This tool is used to detect Web Application firewall from website",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "The url without https schema",
        "required": True
      }
    }
  },
  {
    "name": "SQL-Login",
    "description": "This tools is used to test SQLs inyections",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "The url it must include a parameter, example: https://example.com/?id=1",
        "required": True
      }
    }
  },
  {
    "name": "XSS-Scanner",
    "description": "This tools is used to scan XSS vulnerabilites in a host",
    "parameter_definitions": {
      "url": {
        "type": "string",
        "description": "The url without https schema",
        "required": True
      }
    }
  },
  {
    "name": "Cloudflare-Bypass",
    "description": "This tools is used to get the true IP forward a webpage in a cloudflare",
    "parameter_definitions": {
      "domain": {
        "type": "string",
        "description": "The domain to know true IP",
        "required": True
      }
    }
  },
  {
    "name": "nuclei-http",
    "description": "A tool for check http vulnerabilities",
    "parameter_definitions": {
      "host": {
        "type": "string",
        "description": "The host to scan",
        "required": True
      }
    }
  },
]
import json

def process_response_and_extract_tools(complete_response):


    try:
        # Extracting JSON part from the complete response
        json_start = complete_response.find('```json') + len('```json\n')
        json_end = complete_response.find('\n```', json_start)
        json_str = complete_response[json_start:json_end]

        response_data = json.loads(json_str)
        tools_with_arguments = []
        for index, tool in enumerate(response_data):
            tool_name = tool['tool_name']
            arguments = tool['parameters']
            tools_with_arguments.append([index, tool_name, arguments])
        return [0, tools_with_arguments]
    except json.JSONDecodeError:
        print("Error decoding JSON from response")
        return [1, {}]

function_shodan = [ {
    "name": "shodan_dork",
    "description": "This tools is used to generate a shodan query",
    "parameter_definitions": {
      "dork": {
        "type": "string",
        "description": "The shodan dork",
        "required": True
      }
    }
  }, ]
google_dork = [ {
    "name": "google_dork",
    "description": "This tools is used to generate a google dork",
    "parameter_definitions": {
      "dork": {
        "type": "string",
        "description": "The google dork to generate",
        "required": True
      }
    }
  }, ]
rubbergen = [ {
    "name": "rubbergen",
    "description": "This tools is used to generate a Rubber Ducky Script Payload",
    "parameter_definitions": {
      "payload": {
        "type": "string",
        "description": "The payload from rubber ducky",
        "required": True
      }
    }
  }, ]
osint_funcs = {
        "name": "OSINT",
        "description": "You will use this whenever the query is related to any type of action related to the investigation of persons or entities of any kind.",
        "parameters": {
            "type": "object",
            "properties": {
                "mail": {
                    "type": "string",
                    "description": "The mail to search",
                },
                "nickname": {
                    "type": "string",
                    "description": "The nickname to search",
                },
            },
            "required": ["mail", "nickname"],
        },

    },
