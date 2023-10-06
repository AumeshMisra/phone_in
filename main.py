import logging
import os
import asyncio
from fastapi import FastAPI
from vocode.streaming.models.telephony import TwilioConfig
from pyngrok import ngrok
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.telephony.server.base import (
    TwilioInboundCallConfig,
    TelephonyServer,
)
from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizerConfig
from vocode.streaming.client_backend.conversation import TranscriptEventManager

from custom_agent_factory import CustomAgentFactory
from custom_event_manager import CustomEventsManager
import sys

# if running from python, this will load the local .env
# docker-compose will load the .env file by itself
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(docs_url=None)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config_manager = RedisConfigManager()

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    ngrok_auth = os.environ.get("NGROK_AUTH_TOKEN")
    if ngrok_auth is not None:
        ngrok.set_auth_token(ngrok_auth)
    port = sys.argv[sys.argv.index(
        "--port") + 1] if "--port" in sys.argv else 3000

    # Open a ngrok tunnel to the dev server
    BASE_URL = ngrok.connect(port).public_url.replace("https://", "")
    logger.info(
        'ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(BASE_URL, port))

if not BASE_URL:
    raise ValueError(
        "BASE_URL must be set in environment if not using pyngrok")


@app.get("/health")
async def health():
    return "healthy!"

telephony_server = TelephonyServer(
    base_url=BASE_URL,
    config_manager=config_manager,
    inbound_call_configs=[
        TwilioInboundCallConfig(
            url="/inbound_call",
            agent_config=ChatGPTAgentConfig(
                initial_message=BaseMessage(
                    text="Hi, I am here to learn more about your reason for calling, can you please spell your name?"),
                prompt_preamble="Conduct a medical intake. There are 7 things you must do in this order: 1. Collect patient's name and DOB. 2. They insurance payer 3. insurance ID. 4. If they have a referral and to who. 5. Collect chief medical complaint. 6. Address/ Location 7. Collect contact info (only phone number necessary). After collecting their info, recommend 2 doctors, each with ontimes for them. After they confirm an appointment time, say goodbye and please end the call",
                generate_responses=True,
                end_conversation_on_goodbye=True,
                allow_agent_to_be_cut_off=False,
                allowed_idle_time_seconds=10
            ),
            twilio_config=TwilioConfig(
                account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                auth_token=os.environ["TWILIO_AUTH_TOKEN"],
            ),
            synthesizer_config=ElevenLabsSynthesizerConfig.from_telephone_output_device()
        )
    ],
    agent_factory=CustomAgentFactory(),
    logger=logger,
    events_manager=CustomEventsManager()
)

app.include_router(telephony_server.get_router())
