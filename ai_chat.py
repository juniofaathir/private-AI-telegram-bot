from typing import List, Dict, Optional
from datetime import datetime
from collections import deque
from openai import OpenAI

import pytz, srsly, os


path_this = os.path.abspath(".")
prompts = srsly.read_json(os.path.join(path_this, "prompts.json"))

class AIChat:
    """
    A wrapper class for OpenAI's chat completion API with memory management
    and time awareness.
    
    Attributes:
        client (OpenAI): OpenAI client instance
        model (str): The model to use for chat completion
        system_prompt (str): The system prompt that defines AI behavior
        memory_size (int): Number of previous messages to remember
        conversation_history (deque): Stores the conversation history
        temperature (float): Controls randomness in the model's responses
        timezone (str): Timezone for time-aware responses
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        system_prompt: Optional[str] = None,
        memory_size: int = 10,
        timezone: str = "Asia/Jakarta"
    ):
        """
        Initialize the AIChat instance.
        
        Args:
            api_key (str): OpenAI API key
            system_prompt (str): System prompt to define AI behavior
            model (str, optional): Model to use. Defaults to "gpt-3.5-turbo"
            memory_size (int, optional): Number of messages to remember. Defaults to 10
            timezone (str, optional): Timezone for time awareness. Defaults to "Asia/Jakarta"
        """
        self.client = OpenAI(
            api_key = api_key,
            base_url = base_url
        )
        self.model = model
        if system_prompt == None:
            self.base_system_prompt = prompts["system_default"]
        else:
            self.base_system_prompt = system_prompt
        self.memory_size = memory_size
        self.timezone = pytz.timezone(timezone)
        self.conversation_history = deque(maxlen = memory_size)
        
        # Initialize conversation with time-aware system prompt
        self._update_system_prompt()

    def _get_current_time(self) -> str:
        """
        Get current time in the specified timezone.
        
        Returns:
            str: Formatted current time
        """
        current_time = datetime.now(self.timezone)
        return current_time.strftime("%A, %d %B %Y %H:%M:%S %Z")

    def _update_system_prompt(self) -> None:
        """
        Update system prompt with current time information.
        """
        current_time = self._get_current_time()
        time_aware_prompt = prompts["time_prompt"].format(
            current_time = current_time,
            base_system_prompt = self.base_system_prompt
        )

        # Update system prompt in history
        self._add_to_history("system", time_aware_prompt)

    def _add_to_history(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            role (str): Message role ("system", "user", or "assistant")
            content (str): Message content
        """
        current_time = datetime.now(self.timezone)
        message = {
            "role": role,
            "content": content,
            "timestamp": current_time.isoformat()
        }
        
        # If this is a new system message, remove the old one
        if role == "system":
            self.conversation_history = deque(
                [msg for msg in self.conversation_history if msg["role"] != "system"],
                maxlen = self.memory_size
            )
        
        self.conversation_history.append(message)

    def _prepare_messages(self) -> List[Dict[str, str]]:
        """
        Prepare messages for the API call.
        Always includes updated system prompt and maintains memory window.
        
        Returns:
            List[Dict[str, str]]: List of messages formatted for the API
        """
        # Update system prompt with current time
        self._update_system_prompt()
        
        # Prepare messages
        messages = []
        for msg in self.conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages

    def send_message(self, user_message: str) -> str:
        """
        Send a message to the AI and get a response.
        Automatically includes current time context.
        
        Args:
            user_message (str): The user's message
            
        Returns:
            str: The AI's response
            
        Raises:
            Exception: If the API call fails
        """
        # Add time context to user message if not present
        current_time = self._get_current_time()
        time_aware_message = f"{user_message}\n\nCurrent time: {current_time}"
        
        # Add user message to history
        self._add_to_history("user", time_aware_message)
        
        try:
            # Prepare messages for API call
            messages = self._prepare_messages()
            
            # Make API call
            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
            )
            
            # Extract and store assistant's response
            assistant_message = response.choices[0].message.content
            self._add_to_history("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            raise Exception(f"Error in sending message: {str(e)}")

    def get_conversation_history(self) -> List[Dict]:
        """
        Get the current conversation history.
        
        Returns:
            List[Dict]: List of conversation messages with timestamps
        """
        return list(self.conversation_history)

    def clear_history(self, keep_system_prompt: bool = True) -> None:
        """
        Clear the conversation history.
        
        Args:
            keep_system_prompt (bool): Whether to keep the system prompt
        """
        self.conversation_history.clear()
        if keep_system_prompt:
            self._update_system_prompt()