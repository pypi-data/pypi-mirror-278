from nio import (AccountDataEvent, InviteMemberEvent,
                 KeyVerificationEvent, KeyVerificationCancel,
                 ToDeviceError, KeyVerificationStart,
                 KeyVerificationKey, KeyVerificationMac,
                 LocalProtocolError)
import nio.events.room_events
import nio.events.to_device

from .utils import info, error

class Callbacks:
    """
    A class for handling callbacks.
    """

    def __init__(self, async_client, bot, listener) -> None:
        self.async_client = async_client
        self.bot = bot
        self.listener = listener

    async def setup(self) -> None:
        """
        Add callbacks to async_client
        """
        if self.bot.config.join_on_invite:
            self.async_client.add_event_callback(self.invite_callback,
                                                     InviteMemberEvent)

        self.async_client.add_global_account_data_callback(
            self.custom_emotes_callback, AccountDataEvent
        )

        if self.bot.config.emoji_verify:
            self.async_client.add_to_device_callback(self.emoji_verification,
                                                     (KeyVerificationEvent, ))

        for event_listener in self.listener._registry:
            if issubclass(event_listener[1],
                          nio.events.to_device.ToDeviceEvent):
                self.async_client.add_to_device_callback(
                    event_listener[0], event_listener[1])
            else:
                self.async_client.add_event_callback(event_listener[0],
                                                     event_listener[1])

    async def custom_emotes_callback(self, event) -> None:
        """
        This callback receive AccountDataEvent
        Check type of event:
            - im.ponies.user_emotes: Bot user custom emojis
                Emojis dict will be saved to Api.user_emotes
            - im.ponies.emote_rooms: Custom emojis from a bot rooms
                We need to receive room_get_state event with 'im.ponies.room_emotes' event type
                and emoji pack name as state_key
                Then emojis dict from this room will be saved to Api.room_emotes[room_id][pack_name]
        """
        if hasattr(event, 'type'):
            if event.type == 'im.ponies.user_emotes':
                if not self.bot.emotes.user_emotes:
                    self.bot.emotes.load_user_emotes(event.content)
            elif event.type == 'im.ponies.emote_rooms':
                await self.bot.emotes.load_rooms_emotes(self.async_client, event.content)

    async def invite_callback(self, room, event, tries=1) -> None:
        """
        Callback for handling invites.

        Parameters
        ----------
        room : nio.rooms.MatrixRoom
        event : nio.events.room_events.InviteMemberEvent
        tries : int, optional
            Amount of times that this function has been called in a row for the same exact event.

        """
        if not event.membership == "invite":
            return

        try:
            await self.async_client.join(room.room_id)
            info(f"Joined {room.room_id}")
        except Exception as e:
            error(f"Error joining {room.room_id}: {e}")
            tries += 1
            if not tries == 3:
                info("Trying again...")
                await self.invite_callback(room, event, tries)
            else:
                error(f"Failed to join {room.room_id} after 3 tries")


    async def emoji_verification(self, event):
        """
        Callback for handling interactive verification using emoji.
        Copied from
        https://github.com/poljar/matrix-nio/blob/8ac48ed0fda5da129c008e129305a512e8619cde/examples/verify_with_emoji.py
        with explanation comments removed and miniscule changes

        Parameters
        ----------
        event : nio.events.to_device.KeyVerificationEvent

        """
        try:
            if isinstance(event, KeyVerificationStart
                          ):  # first step: receive m.key.verification.start
                if "emoji" not in event.short_authentication_string:
                    print("Other device does not support emoji verification "
                          f"{event.short_authentication_string}.")
                    return
                # send m.key.verification.accept
                resp = await self.async_client.accept_key_verification(
                    event.transaction_id)
                if isinstance(resp, ToDeviceError):
                    print(f"accept_key_verification failed with {resp}")

                sas = self.async_client.key_verifications[event.transaction_id]

                # send m.key.verification.key
                todevice_msg = sas.share_key()
                resp = await self.async_client.to_device(todevice_msg)
                if isinstance(resp, ToDeviceError):
                    print(f"to_device failed with {resp}")

            elif isinstance(event, KeyVerificationCancel):  # anytime
                # There is no need to issue a
                # self.async_client.cancel_key_verification(tx_id, reject=False)
                # here. The SAS flow is already cancelled.
                # We only need to inform the user.
                print(f"Verification has been cancelled by {event.sender} "
                      f"for reason \"{event.reason}\".")

            elif isinstance(event, KeyVerificationKey
                            ):  # second step: receive m.key.verification.key
                sas = self.async_client.key_verifications[event.transaction_id]

                print(f"{sas.get_emoji()}")

                yn = input("Do the emojis match? (Y/N) (C for Cancel) ")
                if yn.lower() == "y":
                    print("Match! The verification for this "
                          "device will be accepted.")
                    # send m.key.verification.mac
                    resp = await self.async_client.confirm_short_auth_string(
                        event.transaction_id)
                    if isinstance(resp, ToDeviceError):
                        print(f"confirm_short_auth_string failed with {resp}")
                elif yn.lower() == "n":  # no, don't match, reject
                    print("No match! Device will NOT be verified "
                          "by rejecting verification.")
                    resp = await self.async_client.cancel_key_verification(
                        event.transaction_id, reject=True)
                    if isinstance(resp, ToDeviceError):
                        print(f"cancel_key_verification failed with {resp}")
                else:  # C or anything for cancel
                    print("Cancelled by user! Verification will be "
                          "cancelled.")
                    resp = await self.async_client.cancel_key_verification(
                        event.transaction_id, reject=False)
                    if isinstance(resp, ToDeviceError):
                        print(f"cancel_key_verification failed with {resp}")

            elif isinstance(event, KeyVerificationMac
                            ):  # third step: receive m.key.verification.mac
                sas = self.async_client.key_verifications[event.transaction_id]
                try:
                    todevice_msg = sas.get_mac()
                except LocalProtocolError as e:
                    # e.g. it might have been cancelled by ourselves
                    print(f"Cancelled or protocol error: Reason: {e}.\n"
                          f"Verification with {event.sender} not concluded. "
                          "Try again?")
                else:
                    # send m.key.verification.mac
                    resp = await self.async_client.to_device(todevice_msg)
                    if isinstance(resp, ToDeviceError):
                        print(f"to_device failed with {resp}")
                    print(f"sas.we_started_it = {sas.we_started_it}\n"
                          f"sas.sas_accepted = {sas.sas_accepted}\n"
                          f"sas.canceled = {sas.canceled}\n"
                          f"sas.timed_out = {sas.timed_out}\n"
                          f"sas.verified = {sas.verified}\n"
                          f"sas.verified_devices = {sas.verified_devices}\n")
                    print("Emoji verification was successful!")
                    # TODO: share room keys(?) to formerly blacklisted devices
                    # Error: ** Unable to decrypt: decryption key withheld **
            else:
                print(f"Received unexpected event type {type(event)}. "
                      f"Event is {event}. Event will be ignored.")

        except BaseException:
            import traceback
            print(traceback.format_exc())


