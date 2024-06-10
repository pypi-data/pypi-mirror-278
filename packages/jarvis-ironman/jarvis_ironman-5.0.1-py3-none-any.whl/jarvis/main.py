import string
import struct
import time
import traceback
from datetime import datetime

import pvporcupine
import pyaudio
import pywifi
from playsound import playsound

from jarvis.executors import (
    commander,
    controls,
    internet,
    listener_controls,
    location,
    process_map,
    processor,
)
from jarvis.modules.audio import listener, speaker
from jarvis.modules.exceptions import StopSignal
from jarvis.modules.logger import custom_handler, logger
from jarvis.modules.models import models
from jarvis.modules.peripherals import audio_engine
from jarvis.modules.utils import shared, support


def restart_checker() -> None:
    """Operations performed during internal/external request to restart."""
    if flag := support.check_restart():
        logger.info("Restart condition is set to %s by %s", flag[0], flag[1])
        if flag[1] == "OFFLINE":
            processor.stop_processes()
            logger.propagate = False
            for _handler in logger.handlers:
                logger.removeHandler(hdlr=_handler)
            handler = custom_handler()
            logger.info("Switching to %s", handler.baseFilename)
            logger.addHandler(hdlr=handler)
            controls.starter()
            shared.processes = processor.start_processes()
        else:
            processor.stop_processes(func_name=flag[1])
            shared.processes[flag[1]] = processor.start_processes(func_name=flag[1])


class Activator:
    """Awaits for the keyword ``Jarvis`` and triggers ``initiator`` when heard.

    >>> Activator

    See Also:
        - Creates an input audio stream from a microphone, monitors it, and detects the specified wake word.
        - Once detected, Jarvis triggers the ``listener.listen()`` function with an ``acknowledgement`` sound played.
        - After processing the phrase, the converted text is sent as response to ``initiator()`` with a ``return`` flag.
        - The ``should_return`` flag ensures, the user is not disturbed when accidentally woke up by wake work engine.
    """

    def __init__(self):
        """Initiates Porcupine object for hot word detection.

        See Also:
            - Instantiates an instance of Porcupine object and monitors audio stream for occurrences of keywords.
            - A higher sensitivity results in fewer misses at the cost of increasing the false alarm rate.
            - sensitivity: Tolerance/Sensitivity level. Takes argument or env var ``sensitivity`` or defaults to ``0.5``

        References:
            - `Audio Overflow <https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.read>`__ handling.
        """
        label = ", ".join(
            [
                f"{string.capwords(wake)!r}: {sens}"
                for wake, sens in zip(models.env.wake_words, models.env.sensitivity)
            ]
        )
        logger.info("Initiating hot-word detector with sensitivity: %s", label)
        keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in models.env.wake_words]

        arguments = {
            "library_path": pvporcupine.LIBRARY_PATH,
            "sensitivities": models.env.sensitivity,
        }
        if models.settings.legacy:
            arguments["keywords"] = models.env.wake_words
            arguments["model_file_path"] = pvporcupine.MODEL_PATH
            arguments["keyword_file_paths"] = keyword_paths
        else:
            arguments["model_path"] = pvporcupine.MODEL_PATH
            arguments["keyword_paths"] = keyword_paths

        self.detector = pvporcupine.create(**arguments)
        self.audio_stream = self.open_stream()
        if models.settings.limited:
            self.label = f"Awaiting: [{label}] - Limited Mode"
        else:
            self.label = f"Awaiting: [{label}]"

    def open_stream(self) -> pyaudio.Stream:
        """Initializes an audio stream.

        Returns:
            pyaudio.Stream:
            Audio stream from pyaudio.
        """
        return audio_engine.open(
            rate=self.detector.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.detector.frame_length,
            input_device_index=models.env.microphone_index,
        )

    def executor(self) -> None:
        """Calls the listener for actionable phrase and runs the speaker node for response."""
        logger.debug("Wake word detected at %s", datetime.now().strftime("%c"))
        if listener_controls.get_listener_state():
            playsound(sound=models.indicators.acknowledgement, block=False)
        audio_engine.close(stream=self.audio_stream)
        # No confidence during initiation since this will interrupt with listener state
        if phrase := listener.listen(sound=False, no_conf=True):
            try:
                commander.initiator(phrase=phrase)
            except Exception as error:
                logger.critical(error)
                logger.error(traceback.format_exc())
                speaker.speak(
                    text=f"I'm sorry {models.env.title}! I ran into an unknown error. "
                    "Please check the logs for more information."
                )
            speaker.speak(run=True)
        self.audio_stream = self.open_stream()
        support.write_screen(text=self.label)

    def start(self) -> None:
        """Runs ``audio_stream`` in a forever loop and calls ``initiator`` when the phrase ``Jarvis`` is heard."""
        try:
            wake_len = len(models.env.wake_words)
            support.write_screen(text=self.label)
            while True:
                result = self.detector.process(
                    pcm=struct.unpack_from(
                        "h" * self.detector.frame_length,
                        self.audio_stream.read(
                            num_frames=self.detector.frame_length,
                            exception_on_overflow=False,
                        ),
                    )
                )
                if models.settings.legacy:
                    if wake_len == 1 and result:
                        self.executor()
                    elif wake_len > 1 and result >= 0:
                        self.executor()
                else:
                    if result >= 0:
                        self.executor()
                if models.settings.limited:
                    continue
                restart_checker()
                if flag := support.check_stop():
                    logger.info(
                        "Stopper condition is set to %s by %s", flag[0], flag[1]
                    )
                    self.stop()
                    controls.terminator()
        except StopSignal:
            controls.exit_process()
            self.audio_stream = None
            self.stop()
            controls.terminator()

    def stop(self) -> None:
        """Invoked when the run loop is exited or manual interrupt.

        See Also:
            - Terminates/Kills all the background processes.
            - Releases resources held by porcupine.
            - Closes audio stream.
            - Releases port audio resources.
        """
        if not models.settings.limited:
            processor.stop_processes()
        processor.clear_db()
        logger.info("Releasing resources acquired by Porcupine.")
        self.detector.delete()
        if self.audio_stream and self.audio_stream.is_active():
            logger.info("Closing Audio Stream.")
            audio_engine.close(stream=self.audio_stream)
            self.audio_stream.close()
        logger.info("Releasing PortAudio resources.")
        audio_engine.terminate()


def start() -> None:
    """Starts main process to activate Jarvis after checking internet connection and initiating background processes."""
    logger.info("Current Process ID: %d", models.settings.pid)
    controls.starter()
    if internet.ip_address() and internet.public_ip_info():
        support.write_screen(
            text=f"INTERNET::Connected to {internet.get_connection_info() or 'the internet'}."
        )
    else:
        support.write_screen("Trying to toggle WiFi")
        pywifi.ControlPeripheral(logger=logger).enable()
        if models.env.wifi_ssid and models.env.wifi_password:
            time.sleep(5)
            support.write_screen(f"Trying to connect to {models.env.wifi_ssid!r}")
            if pywifi.ControlConnection(
                wifi_ssid=models.env.wifi_ssid,
                wifi_password=models.env.wifi_password,
                logger=logger,
            ).wifi_connector():
                support.write_screen(f"Connected to {models.env.wifi_ssid!r}")
            else:
                support.write_screen(text="BUMMER::Unable to connect to the Internet")
                speaker.speak(
                    text=f"I was unable to connect to the internet {models.env.title}! "
                    "Please check your connection.",
                    run=True,
                )
    support.write_screen(
        text=f"Current Process ID: {models.settings.pid}\tCurrent Volume: {models.env.volume}"
    )
    if models.settings.limited:
        # Write processes mapping file before calling start_processes with func_name flag,
        # as passing the flag will look for the file's presence
        process_map.add({"jarvis": {models.settings.pid: ["Main Process"]}})
        if models.settings.os != models.supported_platforms.macOS:
            shared.processes = processor.start_processes(
                func_name="speech_synthesis_api"
            )
            # Enable speech synthesis for speaker
            if not models.env.speech_synthesis_timeout:
                models.env.speech_synthesis_timeout = 10
    else:
        shared.processes = processor.start_processes()
    location.write_current_location()
    Activator().start()
