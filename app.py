# # from flask import Flask,request,render_template
# # from db import init_db
# # from routes.user import user_route
# # from routes.notification import notification_route
# # from flask import Flask, request, jsonify
# # from google import genai
# # from google.genai import types
# # import requests
# # from dotenv import load_dotenv
# # import os
# # load_dotenv()

# from flask import Flask, request, jsonify
# from db import init_db
# from routes.user import user_route
# from routes.notification import notification_route
# import google.generativeai as genai   # ✅ FIXED import
# from google.generativeai import types
# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()
# def create_app():
#     app=Flask(__name__,template_folder='templates')
#     init_db(app)
#     app.register_blueprint(user_route,url_prefix="/user")
#     app.register_blueprint(notification_route,url_prefix='/send')
    
#     @app.route('/')
#     def gett():
#         return "helo"
    
#     @app.route("/ask-llm", methods=["POST"])
#     def ask_llm():
#         data = request.json
#         user_prompt = data.get("prompt")

#         # Step 1: Ask Gemini
#         response = model.generate_content(user_prompt)

#         # Step 2: Check if Gemini wants to call a tool
#         if response.candidates[0].content.parts[0].function_call:
#             fn_call = response.candidates[0].content.parts[0].function_call
#             tool_name = fn_call.name
#             arguments = fn_call.args

#             if tool_name == "send_notification":
#                 result = call_notification_api(
#                     # user_id=arguments.get("user_id", "guest"),
#                     # type=arguments["type"],
#                     # title=arguments["title"],  
                  
#                     # carrier=arguments["carrier"],
#                     # message=arguments["message"],
#                     # sent_to=arguments["sent_to"]

#                     user_id=arguments.get("user_id", "guest"),
#                     type=arguments.get("type", "general"),
#                     title=arguments.get("title", "No Title"),
#                     carrier=arguments.get("carrier", "unknown"),
#                     message=arguments.get("message", ""),
#                     sent_to=arguments.get("sent_to", "unknown")
#                 )
#                 return jsonify({"tool": tool_name, "arguments": arguments, "result": result})

#         # Step 3: Just text reply
#         return jsonify({"response": response.text})
#     return app


# load_dotenv()
# # Configure Gemini API
# genai.configure(api_key="")

# # Define the tool schema
# send_notification_tool = types.Tool(
#     function_declarations=[
#         types.FunctionDeclaration(
#             name="send_notification",
#             description="Send a reminder notification via Notification Service API",
#             parameters={
#                 "type": "object",
#                 "properties": {
#                     # "user_id": {"type": "string", "description": "Unique ID of the user"},
#                     "type":{"type":"string","description":"Message Title"},
#                     "carrier": {"type": "string", "enum": ["sms", "email"], "description": "Type of notification"},
#                     "message": {"type": "string", "description": "Message content"},
#                     "sent_to": {"type": "string", "description": "Phone number or email address"}
#                 },
#                 "required": ["carrier", "message", "sent_to"]
#             },
#         )
#     ]
# )

# # Create the model with the tool
# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     tools=[send_notification_tool]
# )

# # Function to actually call your Notification Service API
# def call_notification_api(user_id, carrier, message, sent_to,title,type):
#     api_url = "http://localhost:5555/send/send"  # ✅ Your Notification Service API
#     payload = {
#         "user_id": "ed4ae60a-0985-4196-b924-9659c143cc51",
#         "carrier": carrier,
#         "message": message,
#         "sent_to": sent_to,
#         "title":title,
#         "type":type
#     }
#     try:
#         response = requests.post(api_url, json=payload)
#         return response.json()
#     except Exception as e:
#         return {"status": "error", "details": str(e)}

# # Flask app
# # app = Flask(__name__)

# # if __name__ == "__main__":
# #     app.run(debug=True, port=5000)

# #     return app

# if __name__=='__main__':
#     app=create_app()
#     app.run(host='0.0.0.0',port=5555,debug=True)

from flask import Flask, request, jsonify
from db import init_db
from routes.user import user_route
from routes.notification import notification_route
import google.generativeai as genai
from google.generativeai import types
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Define the tool schema for Gemini
send_notification_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="send_notification",
            description="Send a message notification via Notification Service API",
            parameters={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "Message type"},
                    "title": {"type": "string", "description": "Notification title"},
                    "carrier": {
                        "type": "string",
                        "enum": ["sms", "email"],
                        "description": "Type of notification"
                    },
                    "message": {"type": "string", "description": "Message content"},
                    "sent_to": {"type": "string", "description": "Phone number or email address"}
                },
                "required": ["carrier", "message", "sent_to"]
            },
        )
    ]
)

send_reminder_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="send_reminder",
            description="send or schedule a reminder notification as per prompt  via Notification Service API",
            parameters={
                "type": "object",
                "properties": {
                    # "type": {"type": "string", "description": "Message type"},
                    "title": {"type": "string", "description": "Notification title"},
                    "carrier": {
                        "type": "string",
                        "enum": ["sms", "email"],
                        "description": "Type of notification"
                    },
                    "message": {"type": "string", "description": "Message content"},
                    "sent_to": {"type": "string", "description": "Phone number or email address"},
                    "execute_at":{"type":"string","description": "time for the execution of reminder notification in ISO format"}
                },
                "required": ["carrier", "message", "sent_to","execute_at"]
            },
        )
    ]
)


    # "to":["+919322482793","+918983056865"],
    # "title":"reminder",
    # "message":"checking reminder with hook",
    # "carrier":"sms",
    # "executeAt":"2025-08-13T21:49:00"



# ✅ Create Gemini model with tools
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[send_notification_tool,send_reminder_tool]
)

# ✅ Function to call Notification Service API
def call_notification_api(user_id, carrier, message, sent_to, title, type):
    api_url = "http://localhost:5555/send/send"
    payload = {
        "user_id": "4b876ea4-8610-402f-864e-6a88a211896b",
        "carrier": carrier,
        "message": message,
        "sent_to": sent_to,
        "title": title,
        "type": type
    }
    try:
        response = requests.post(api_url, json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "details": str(e)}

def call_reminder_api(user_id, carrier, message, sent_to, title, execute_at):
    api_url = "http://localhost:5555/send/reminder"
    payload = {
        "user_id": "4b876ea4-8610-402f-864e-6a88a211896b",
        "carrier": carrier,
        "message": message,
        "sent_to": sent_to,
        "title": title,
        "execute_at": execute_at
    }
    try:
        response = requests.post(api_url, json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "details": str(e)}

# ✅ Create Flask app
def create_app():
    app = Flask(__name__, template_folder='templates')
    init_db(app)
    app.register_blueprint(user_route, url_prefix="/user")
    app.register_blueprint(notification_route, url_prefix="/send")

    @app.route('/')
    def home():
        return "Hello from Flask + Gemini"

    # @app.route("/ask-llm", methods=["POST"])
    # def ask_llm():
    #     data = request.json
    #     user_prompt = data.get("prompt")

    #     # Step 1: Ask Gemini
    #     response = model.generate_content(user_prompt)

    #     # Step 2: Check if Gemini wants to call a tool
    #     fc = response.candidates[0].content.parts[0].function_call
    #     if fc:
    #         tool_name = fc.name
    #         arguments = fc.args

    #         if tool_name == "send_notification":
    #             result = call_notification_api(
    #                 user_id=arguments.get("user_id", "guest"),
    #                 type=arguments.get("type", "general"),
    #                 title=arguments.get("title", "No Title"),
    #                 carrier=arguments.get("carrier", "unknown"),
    #                 message=arguments.get("message", ""),
    #                 sent_to=arguments.get("sent_to", "unknown")
    #             )
    #             return jsonify({"tool": tool_name, "arguments": arguments, "result": result})

    #     # Step 3: Just text reply
    #     return jsonify({"response": response.text})
    @app.route("/ask-llm", methods=["POST"])
    def ask_llm():
        data = request.json
        user_prompt = data.get("prompt")

        # Step 1: Ask Gemini
        response = model.generate_content(user_prompt)

        # Step 2: Check if Gemini wants to call a tool
        fc = response.candidates[0].content.parts[0].function_call
        if fc:
            tool_name = fc.name
            arguments = dict(fc.args)   # ✅ Convert MapComposite -> dict

            if tool_name == "send_notification":
                result = call_notification_api(
                    user_id="",
                    type=arguments.get("type", "general"),
                    title=arguments.get("title", "No Title"),
                    carrier=arguments.get("carrier", "unknown"),
                    message=arguments.get("message", ""),
                    sent_to=arguments.get("sent_to", "unknown")
                )
                return jsonify({
                    "tool": tool_name,
                    "arguments": arguments,  # ✅ Now JSON serializable
                    "result": result
                })
            

            if tool_name == "send_reminder":
                result = call_reminder_api(
                    user_id="",
                    execute_at=arguments.get("execute_at", "1pm"),
                    title=arguments.get("title", "No Title"),
                    carrier=arguments.get("carrier", "unknown"),
                    message=arguments.get("message", ""),
                    sent_to=arguments.get("sent_to", "unknown")
                )
                return jsonify({
                    "tool": tool_name,
                    "arguments": arguments,  # ✅ Now JSON serializable
                    "result": result
                })

        # Step 3: Just text reply
        return jsonify({"response": response.text})

    return app


# ✅ Run Flask App
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5555, debug=True)
