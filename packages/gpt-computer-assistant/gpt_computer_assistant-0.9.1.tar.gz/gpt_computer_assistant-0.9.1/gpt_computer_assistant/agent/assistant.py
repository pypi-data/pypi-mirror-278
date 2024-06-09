import base64
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from .chat_history import *
from .agent import *


try:
    from ..screen.shot import *
    from ..utils.db import load_model_settings, agents
    from ..llm import get_model
    from ..llm_settings import first_message
except ImportError:
    from screen.shot import *
    from utils.db import load_model_settings, agents
    from llm import get_model
    from llm_settings import first_message

config = {"configurable": {"thread_id": "abc123"}}


def agentic(
    llm_input, llm_history, client, screenshot_path=None, dont_save_image=False
):
    global agents
    from crewai import Task, Crew

    from crewai import Agent as crewai_Agent

    the_agents = []

    for each in agents:
        the_agents.append(
            crewai_Agent(
                role=each["role"],
                goal=each["goal"],
                backstory=each["backstory"],
                llm=get_model(),
            )
        )

    agents = the_agents

    print("LLM INPUT", llm_input)

    def image_explaination():
        the_message = [
            {"type": "text", "text": f"Explain the image"},
        ]

        if screenshot_path:
            base64_image = encode_image(screenshot_path)
            the_message.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            )
            print("LEN OF İMAGE", len(base64_image))

        the_message = HumanMessage(content=the_message)
        get_chat_message_history().add_message(the_message)

        the_model = load_model_settings()

        if the_model == "gpt-4o" or the_model == "gpt-3.5-turbo":
            msg = get_agent_executor().invoke(
                {"messages": llm_history + [the_message]}, config=config
            )

        elif the_model == "llava" or the_model == "bakllava":

            msg = get_agent_executor().invoke(
                {
                    "input": the_message,
                    "chat_history": llm_history,
                }
            )

        the_last_messages = msg["messages"]

        return the_last_messages[-1].content

    if screenshot_path:
        image_explain = image_explaination()
        llm_input += "User Sent Image and image content is: " + image_explain



    llm_input = llm_input + first_message


    task = Task(
        description=llm_input, expected_output="Answer", agent=agents[0], tools=tools
    )

    the_crew = Crew(
        llm=get_model(),
        agents=agents,
        tasks=[task],
        full_output=True,
        verbose=True,
    )

    result = the_crew.kickoff()["final_output"]

    get_chat_message_history().add_message(HumanMessage(content=[llm_input.replace(first_message, "")]))
    get_chat_message_history().add_message(AIMessage(content=[result]))

    return result


def assistant(
    llm_input, llm_history, client, screenshot_path=None, dont_save_image=False
):

    if len(agents) != 0:
        print("Moving to Agentic")
        return agentic(llm_input, llm_history, client, screenshot_path, dont_save_image)

    print("LLM INPUT", llm_input)

    llm_input = llm_input + first_message

    the_message = [
        {"type": "text", "text": f"{llm_input}"},
    ]

    if screenshot_path:
        base64_image = encode_image(screenshot_path)
        the_message.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        )
        print("LEN OF İMAGE", len(base64_image))



    the_message = HumanMessage(content=the_message)
    get_chat_message_history().add_message(the_message)

    the_model = load_model_settings()

    if the_model == "gpt-4o" or the_model == "gpt-3.5-turbo" or the_model == "mixtral-8x7b-groq":

        if the_model == "mixtral-8x7b-groq":
            the_history = []
            for message in llm_history:
                try:
                    # Seperate the system message and human message by class
                    print("EXAMPLE", message.content[0])
                    if isinstance(message, SystemMessage):
                        the_mes = SystemMessage(content=message.content[0]["text"])
                        the_history.append(the_mes)
                    elif isinstance(message, HumanMessage):
                        the_mes = HumanMessage(content=message.content[0]["text"])
                        the_history.append(the_mes)
                    else:
                        the_mes = AIMessage(content=message.content[0]["text"])
                        the_history.append(the_mes)
                except:
                    the_mes = AIMessage(content=message.content)
                    the_history.append(the_mes)

            llm_input += first_message

            the_last_message = HumanMessage(content=llm_input)
            msg = get_agent_executor().invoke(
                {"messages": the_history + [the_last_message]}, config=config
            )

        else:
            msg = get_agent_executor().invoke(
                {"messages": llm_history + [the_message]}, config=config
            )

    elif the_model == "llava" or the_model == "bakllava":

        msg = get_agent_executor().invoke(
            {
                "input": the_message,
                "chat_history": llm_history,
            }
        )

    the_last_messages = msg["messages"]



    if dont_save_image and screenshot_path != None:
        currently_messages = get_chat_message_history().messages
        if take_screenshot:
            last_message = currently_messages[-1].content[0]
            currently_messages.remove(currently_messages[-1])

            get_chat_message_history().clear()
            for message in currently_messages:
                get_chat_message_history().add_message(message)
            get_chat_message_history().add_message(HumanMessage(content=[last_message]))

    get_chat_message_history().add_message(the_last_messages[-1])




    # Replace first_message with empty string
    list_of_messages = get_chat_message_history().messages

    get_chat_message_history().clear()

    for message in list_of_messages:
        try:
            message.content[0]["text"] = message.content[0]["text"].replace(first_message, "")
            get_chat_message_history().add_message(message)
        except:
            get_chat_message_history().add_message(message)



    print("THE LAST MESSAGES",  get_chat_message_history().messages)

    return the_last_messages[-1].content
