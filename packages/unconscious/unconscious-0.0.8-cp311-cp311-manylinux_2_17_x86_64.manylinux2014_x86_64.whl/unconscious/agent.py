from .client import UnconsciousClient, BaseMessage
import threading
import time
import abc


class UnconsciousNpc(UnconsciousClient):
    def __init__(self, name, thread, message_types=[]):
        super().__init__(thread)
        self.name = name
        self.message_types = message_types

        self._set_on_message(
            lambda message: print(
                f"<{self.name} | len: {len(message)}\ttype: '{message.message_type}'>"
            )
        )

        self._set_on_call(lambda: print(f"{self.name} has been reborn!"))

    def awaken(self):
        unix_current_time = int(time.time() * 1000)
        self.connect(unix_current_time)
        threading.Thread(target=self.listen, args=(self.on_message,)).start()
        return self

    def _set_on_call(self, on_call):
        self.__call__ = on_call

    @abc.abstractmethod
    def on_message(self, message: BaseMessage, client_id: str):
        raise NotImplementedError

    def _set_on_message(self, on_message):
        self.on_message = on_message

    def send_message(self, message):
        self.add_message(message)

    def get_messages(self, start=None, end=None):
        return super().get_messages(start, end)


def npc(cls=None, default_name=None, thread=None):
    def get_default_thread():
        return getattr(npc, "default_thread", "main")

    if thread is None:
        thread = get_default_thread()

    def decorator(cls):
        class WrappedNpc(cls, UnconsciousNpc):
            def __init__(self, name=default_name, thread=thread):
                name = name or cls.__name__
                super().__init__(name=name, thread=thread, message_types=[])
                if hasattr(cls, "on_message"):
                    self._set_on_message(
                        lambda message, client_id: cls.on_message(
                            self, message, client_id
                        )
                    )

            def __call__(self):
                self.awaken()
                if hasattr(cls, "on_alive"):
                    self.on_alive()

        return WrappedNpc

    if cls is not None:
        # If @npc is used without parentheses
        return decorator(cls)
    return decorator


def set_default_thread(thread_name):
    setattr(npc, "default_thread", thread_name)


npc.set_default_thread = set_default_thread


class NpcManager:
    def __init__(self):
        self.agents = {}

    def register_npc(self, agent_class):
        agent = agent_class()
        self.agents[agent.name] = threading.Thread(target=agent)

    def alive(self):
        for agent in self.agents.values():
            agent.start()
